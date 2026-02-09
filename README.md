## GenAI-Edu-Assistant

An AI-powered educational assistant that enables students to ask questions from PDF-based study materials and receive accurate, mode-based answers using Retrieval-Augmented Generation (RAG) and Generative AI.

## Overview

GenAI-Edu-Assistant is designed to simplify learning from large educational documents such as textbooks and notes. Instead of manually searching through PDFs, users can upload documents, ask natural language questions, and receive context-aware answers tailored to their learning needs.

The system combines document retrieval, prompt compression, and AI-based response generation to deliver efficient and accurate results.

## 🚀 Features

1. **PDF-based Question Answering**
Upload educational PDFs and ask questions directly from the content.

2. **Mode-based Responses**
Choose how answers are generated:

  a. Default – Standard explanation

  b. Exam – Structured, exam-oriented answers

  c. Summary – Concise responses

  d. ELI5 – Simple explanations

  e. Creative – Intuitive and creative answers

3. **Retrieval-Augmented Generation (RAG)**
Retrieves only the most relevant document chunks before generating answers.

4. **Context Compression (ScaleDown API)**
Reduces prompt size while preserving meaning, improving performance and lowering costs.

5. **Question History Tracking**
View previously asked questions for better learning continuity.

6. **Clean Web Interface**
Simple UI built with HTML, CSS, and JavaScript.

## 🧠 Tech Stack

1. Backend: Python, FastAPI

2. Frontend: HTML, CSS, JavaScript

3. AI & NLP: OpenAI API, LangChain

4. Vector Store: FAISS

5. Embeddings: Sentence Transformers

6. Prompt Compression: ScaleDown API

≫ Working Methodology:

--User uploads a PDF document

--Text is extracted and chunked

--Relevant chunks are retrieved using vector similarity

--Context is compressed using ScaleDown

--AI generates an answer based on selected mode

--Answer is displayed on the UI and stored in history

## 🏗️ Project Architecture

GenAI-Edu-Assistant/
│
├── backend/
│   ├── __pycache__/              # Python cache files
│   ├── venv/                     # Backend virtual environment (ignored in git)
│   ├── __init__.py               # Marks backend as a Python package
│   ├── app.py                    # Main FastAPI application (API entry point)
│   ├── modes.py                  # Logic for response modes (Default, Exam, Summary, ELI5, Creative)
│   ├── pdf_loader.py             # Handles PDF upload and text extraction
│   ├── rag_pipeline.py           # Retrieval-Augmented Generation pipeline
│   ├── vector_store.py           # Embedding creation and vector database handling
│   ├── scaledown_client.py       # Context compression using ScaleDown API
│   ├── requirements.txt          # Backend dependencies
│   ├── start.ps1                 # Script to start backend server
│   └── test.txt                  # Temporary testing file
│
├── frontend/
│   ├── app.js                    # Frontend logic and API communication
│   ├── index.html                # Main UI layout
│   ├── styles.css                # Styling for the UI
│   └── test_upload_simple.html   # PDF upload testing page
│
├── uploads/                      # Uploaded PDF files (ignored in git)
│
├── .env                          # Environment variables (API keys) – ignored
├── .env.example                  # Sample environment variable template
├── .gitignore                    # Files and folders excluded from git
├── README.md                     # Project documentation
└── test_upload.html              # Standalone upload test page

## Setup Instructions:

1. Clone the repository

2. git clone https://github.com/your-username/GenAI-Edu-Assistant.git

3. Create and activate a virtual environment
4. python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

5. Install dependencies

6. pip install -r requirements.txt


7. Set environment variables

OPENAI_API_KEY=your_openai_key
SCALEDOWN_API_KEY=your_scaledown_key

7. Run the application

uvicorn app.api.main:app --reload


8. Open browser and visit

http://127.0.0.1:8000/docs

Endpoint

POST /ask

Request Body

{
  "question": "What happens after death?"
}

Response

"Generated answer from the AI model"

## Unique Aspect:

The project uniquely combines RAG, prompt compression, and mode-based learning, making it both cost-efficient and adaptable to different educational needs.

## Future Enhancements:

--Multi-PDF support

--User authentication

--Personalized learning insights

--Cloud deployment

⚠️ Known Issues / Limitations

ScaleDown API may occasionally timeout (504).

OpenAI API key must be valid and active.

Large document sets require optimized chunking.

(Planned fixes coming soon 👇)

🛠️ Upcoming Improvements

✅ Retry + fallback logic for ScaleDown failures

🔁 Caching compressed prompts

📡 Streaming responses

🧪 Better error handling (no more 500s)

🌐 Frontend UI (Gen Z friendly 😄)

🤝 Contributing

Pull requests are welcome!

Fork the repo

Create a new branch

Make your changes

Open a PR 🚀

🧑‍💻 Author

Sam
Building GenAI tools for education 🚀
Feel free to connect & collaborate.

⭐ Support

If you found this project helpful, please give it a ⭐ on GitHub!
