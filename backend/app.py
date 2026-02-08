"""
FastAPI Backend Application
Main application for the Educational Content Assistant.
"""

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import shutil
import os
from datetime import datetime
from typing import List, Optional
from pathlib import Path

from pdf_loader import load_pdf
from vector_store import create_vector_store, search_vector_store
from rag_pipeline import build_query, format_context
from modes import get_available_modes
from scaledown_client import generate_answer, get_api_key
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="Educational Content Assistant")

# Create uploads directory
UPLOAD_DIR = Path(__file__).parent.parent / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files (optional, comment out if not serving from backend)
# app.mount("/static", StaticFiles(directory="../frontend"), name="static")

# Global state
vector_store = None
current_pdf = None
conversation_history = []


# Pydantic models
class QuestionRequest(BaseModel):
    question: str
    mode: str = "default"


class HistoryItem(BaseModel):
    question: str
    answer: str
    mode: str
    timestamp: str


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Educational Content Assistant API", "status": "running"}


@app.get("/modes")
async def get_modes():
    """Get available response modes."""
    return {"modes": get_available_modes()}


@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    """
    Upload and process a PDF file.
    
    Args:
        file: PDF file to upload
        
    Returns:
        dict: Upload status and metadata
    """
    global vector_store, current_pdf
    
    print(f"\n{'='*50}")
    print(f"📥 UPLOAD REQUEST RECEIVED")
    print(f"{'='*50}")
    print(f"File: {file.filename}")
    print(f"Content Type: {file.content_type}")
    print(f"Size: {file.size if hasattr(file, 'size') else 'unknown'}")
    
    try:
        # Validate file type
        if not file.filename.endswith('.pdf'):
            print("❌ Invalid file type")
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")
        
        print("✓ File type validated")
        
        # Save uploaded file
        file_path = UPLOAD_DIR / file.filename
        print(f"💾 Saving to: {file_path}")
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        print("✓ File saved")
        print("📖 Loading PDF...")
        
        # Load and process PDF
        documents = load_pdf(str(file_path))
        print(f"✓ Loaded {len(documents)} pages")
        
        print("🔤 Creating embeddings (this may take a minute)...")
        
        # Create vector store
        vector_store = create_vector_store(documents)
        current_pdf = file.filename
        
        print("✓ Vector store created")
        
        # Clear history when new PDF is uploaded
        conversation_history.clear()
        
        print(f"✅ Upload complete: {file.filename}")
        
        return {
            "status": "uploaded",
            "filename": file.filename,
            "pages": len(documents),
            "message": "PDF processed successfully"
        }
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")


@app.post("/ask")
async def ask_question(request: QuestionRequest):
    """
    Ask a question about the uploaded PDF.
    
    Args:
        request: Question and mode
        
    Returns:
        dict: Answer and metadata
    """
    global vector_store, conversation_history
    
    try:
        # Check if PDF is uploaded
        if vector_store is None:
            raise HTTPException(
                status_code=400,
                detail="No PDF uploaded. Please upload a PDF first."
            )
        
        # Validate mode
        if request.mode not in get_available_modes():
            raise HTTPException(
                status_code=400,
                detail=f"Invalid mode. Available modes: {get_available_modes()}"
            )
        
        # Search vector store for relevant context
        relevant_docs = search_vector_store(vector_store, request.question, k=4)
        
        # Format context
        context = format_context(relevant_docs)
        
        # Build query
        full_query = build_query(context, request.question, request.mode)
        
        # Get ScaleDown API key
        api_key = get_api_key()
        
        # Call answer generation with mode
        answer = generate_answer(
            api_key=api_key,
            context=context,
            prompt=full_query,
            model="gpt-4o",
            mode=request.mode
        )
        
        # Check if there was an error
        if isinstance(answer, dict) and "error" in answer:
            raise HTTPException(status_code=500, detail=f"ScaleDown API error: {answer['error']}")
        
        # answer is now a string containing the generated response
        
        # Save to history
        history_item = {
            "question": request.question,
            "answer": answer,
            "mode": request.mode,
            "timestamp": datetime.now().isoformat()
        }
        conversation_history.append(history_item)
        
        return {
            "answer": answer,
            "mode": request.mode,
            "sources": len(relevant_docs)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing question: {str(e)}")


@app.get("/history")
async def get_history():
    """
    Get conversation history.
    
    Returns:
        dict: List of conversation history items
    """
    return {
        "history": conversation_history,
        "pdf": current_pdf,
        "total": len(conversation_history)
    }


@app.delete("/history")
async def clear_history():
    """Clear conversation history."""
    global conversation_history
    conversation_history.clear()
    return {"status": "history cleared"}


@app.get("/status")
async def get_status():
    """Get current system status."""
    return {
        "pdf_loaded": current_pdf is not None,
        "current_pdf": current_pdf,
        "vector_store_ready": vector_store is not None,
        "history_count": len(conversation_history)
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
