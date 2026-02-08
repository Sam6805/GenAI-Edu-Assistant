// API Base URL
const API_URL = 'http://localhost:8001';

// State
let isPdfUploaded = false;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    const pdfUpload = document.getElementById('pdfUpload');
    const questionInput = document.getElementById('question');
    
    pdfUpload.addEventListener('change', handleFileUpload);
    
    // Enable "Enter" key to send question
    questionInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !questionInput.disabled) {
            ask();
        }
    });
    
    // Check system status on load
    checkStatus();
});

// Check system status
async function checkStatus() {
    try {
        const response = await fetch(`${API_URL}/status`);
        const data = await response.json();
        
        if (data.pdf_loaded) {
            isPdfUploaded = true;
            updateUploadStatus(`✅ PDF loaded: ${data.current_pdf}`, 'success');
            enableQuestionInput();
        }
    } catch (error) {
        console.error('Status check failed:', error);
    }
}

// Handle file upload
async function handleFileUpload(event) {
    const file = event.target.files[0];
    
    if (!file) return;
    
    if (!file.name.endsWith('.pdf')) {
        updateUploadStatus('❌ Please upload a PDF file', 'error');
        return;
    }
    
    // Show loading with animation
    updateUploadStatus('📤 Uploading PDF...', 'loading');
    
    // Add visual feedback to chat with processing class
    const chat = document.getElementById('chat');
    chat.innerHTML = '<div class="info-message processing">📤 Uploading and processing your PDF...<br>This may take 30-60 seconds depending on file size.<br><br>Please wait...</div>';
    
    const formData = new FormData();
    formData.append('file', file);
    
    try {
        updateUploadStatus('🔄 Processing PDF (this may take 30-60 seconds)...', 'loading');
        
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 120000); // 2 minute timeout
        
        const response = await fetch(`${API_URL}/upload-pdf`, {
            method: 'POST',
            body: formData,
            signal: controller.signal
        });
        
        clearTimeout(timeoutId);
        
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({ detail: 'Upload failed' }));
            throw new Error(errorData.detail || 'Upload failed');
        }
        
        const data = await response.json();
        
        isPdfUploaded = true;
        updateUploadStatus(
            `✅ ${data.filename} uploaded (${data.pages} pages)`, 
            'success'
        );
        
        // Clear welcome message
        const chat = document.getElementById('chat');
        chat.innerHTML = '<div class="info-message">PDF loaded! Ask your first question below.</div>';
        
        // Enable question input
        enableQuestionInput();
        
    } catch (error) {
        let errorMsg = '❌ Upload failed: ';
        if (error.name === 'AbortError') {
            errorMsg += 'Request timed out. PDF might be too large.';
        } else if (error.message.includes('Failed to fetch')) {
            errorMsg += 'Cannot connect to server. Make sure server is running on port 8001.';
        } else {
            errorMsg += error.message;
        }
        updateUploadStatus(errorMsg, 'error');
        console.error('Upload error:', error);
        
        // Reset chat to welcome state
        const chat = document.getElementById('chat');
        chat.innerHTML = '<div class="welcome-message"><h2>👋 Welcome!</h2><p>Upload a PDF to get started. Then ask any questions about the content.</p></div>';
    }
}

// Update upload status
function updateUploadStatus(message, type) {
    const statusEl = document.getElementById('uploadStatus');
    const uploadText = document.getElementById('uploadText');
    
    statusEl.textContent = message;
    statusEl.className = `upload-status ${type}`;
    
    if (type === 'success') {
        uploadText.textContent = 'Change PDF';
    }
}

// Enable question input
function enableQuestionInput() {
    const questionInput = document.getElementById('question');
    const sendBtn = document.getElementById('sendBtn');
    
    questionInput.disabled = false;
    sendBtn.disabled = false;
    questionInput.focus();
}

// Ask question
async function ask() {
    const questionInput = document.getElementById('question');
    const question = questionInput.value.trim();
    const mode = document.getElementById('mode').value;
    
    if (!question) {
        alert('Please enter a question');
        return;
    }
    
    if (!isPdfUploaded) {
        alert('Please upload a PDF first');
        return;
    }
    
    // Add user question to chat
    addMessageToChat(question, 'user');
    
    // Clear input
    questionInput.value = '';
    
    // Show loading
    const loadingId = addLoadingMessage();
    
    try {
        const response = await fetch(`${API_URL}/ask`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ question, mode })
        });
        
        if (!response.ok) {
            throw new Error('Failed to get answer');
        }
        
        const data = await response.json();
        
        // Remove loading message
        removeLoadingMessage(loadingId);
        
        // Add answer to chat
        addMessageToChat(data.answer, 'assistant', data.mode);
        
    } catch (error) {
        removeLoadingMessage(loadingId);
        addMessageToChat(
            '❌ Sorry, an error occurred. Please try again.', 
            'error'
        );
        console.error('Question error:', error);
    }
}

// Add message to chat
function addMessageToChat(message, type, mode = '') {
    const chat = document.getElementById('chat');
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}-message`;
    
    if (mode && type === 'assistant') {
        const modeLabel = document.createElement('div');
        modeLabel.className = 'mode-label';
        modeLabel.textContent = getModeIcon(mode) + ' ' + mode.replace('_', ' ').toUpperCase();
        messageDiv.appendChild(modeLabel);
    }
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.textContent = message;
    
    messageDiv.appendChild(contentDiv);
    chat.appendChild(messageDiv);
    
    // Scroll to bottom
    chat.scrollTop = chat.scrollHeight;
}

// Get mode icon
function getModeIcon(mode) {
    const icons = {
        'default': '💬',
        'exam': '📝',
        'summary': '⚡',
        'explain_like_5': '👶',
        'creative': '🎨'
    };
    return icons[mode] || '💬';
}

// Add loading message
function addLoadingMessage() {
    const chat = document.getElementById('chat');
    const loadingDiv = document.createElement('div');
    const id = 'loading-' + Date.now();
    
    loadingDiv.id = id;
    loadingDiv.className = 'message assistant-message loading';
    loadingDiv.innerHTML = '<div class="message-content">Thinking<span class="dots"></span></div>';
    
    chat.appendChild(loadingDiv);
    chat.scrollTop = chat.scrollHeight;
    
    return id;
}

// Remove loading message
function removeLoadingMessage(id) {
    const loadingDiv = document.getElementById(id);
    if (loadingDiv) {
        loadingDiv.remove();
    }
}

// Toggle history panel
function toggleHistory() {
    const panel = document.getElementById('historyPanel');
    const toggle = document.getElementById('historyToggle');
    
    if (panel.classList.contains('hidden')) {
        loadHistory();
        panel.classList.remove('hidden');
        toggle.textContent = '📜 Hide History';
    } else {
        panel.classList.add('hidden');
        toggle.textContent = '📜 View History';
    }
}

// Load history
async function loadHistory() {
    try {
        const response = await fetch(`${API_URL}/history`);
        const data = await response.json();
        
        const historyContent = document.getElementById('historyContent');
        
        if (data.history.length === 0) {
            historyContent.innerHTML = '<p class="empty-history">No questions asked yet</p>';
            return;
        }
        
        historyContent.innerHTML = data.history.map((item, index) => `
            <div class="history-item">
                <div class="history-number">#${index + 1}</div>
                <div class="history-question"><strong>Q:</strong> ${item.question}</div>
                <div class="history-answer"><strong>A:</strong> ${item.answer.substring(0, 150)}${item.answer.length > 150 ? '...' : ''}</div>
                <div class="history-meta">
                    <span class="history-mode">${getModeIcon(item.mode)} ${item.mode}</span>
                    <span class="history-time">${new Date(item.timestamp).toLocaleTimeString()}</span>
                </div>
            </div>
        `).join('');
        
    } catch (error) {
        console.error('Failed to load history:', error);
    }
}

// Clear history
async function clearHistory() {
    if (!confirm('Are you sure you want to clear the conversation history?')) {
        return;
    }
    
    try {
        await fetch(`${API_URL}/history`, {
            method: 'DELETE'
        });
        
        loadHistory();
        alert('History cleared');
        
    } catch (error) {
        console.error('Failed to clear history:', error);
        alert('Failed to clear history');
    }
}
