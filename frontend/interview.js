/**
 * Interview functionality
 */

let currentSessionId = null;
let currentQuestionNumber = 1;
let totalQuestions = 5;
let currentTopic = null;

// DOM Elements (will be set when page loads)
let chatMessages, answerInput, submitBtn, questionCounter, progressFill;
let dashboardView, interviewView, reportView;

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    chatMessages = document.getElementById('chat-messages');
    answerInput = document.getElementById('answer-input');
    submitBtn = document.getElementById('submit-btn');
    questionCounter = document.getElementById('question-counter');
    progressFill = document.getElementById('progress-fill');
    
    dashboardView = document.getElementById('dashboard-view');
    interviewView = document.getElementById('interview-view');
    reportView = document.getElementById('report-view');
    
    // Load available topics
    loadTopics();
    
    // Check authentication
    if (!requireAuth()) {
        return;
    }
    
    // Load user info
    const user = getUser();
    if (user) {
        const userDisplay = document.getElementById('user-display');
        if (userDisplay) {
            userDisplay.textContent = user.username;
        }
    }
});

// Show different views
function showView(viewName) {
    [dashboardView, interviewView, reportView].forEach(view => {
        if (view) view.classList.add('hidden');
    });
    
    const view = document.getElementById(`${viewName}-view`);
    if (view) view.classList.remove('hidden');
}

// Load available topics
async function loadTopics() {
    try {
        const response = await apiRequest('/topics');
        const data = await response.json();
        
        const topicsContainer = document.getElementById('topics-container');
        if (topicsContainer) {
            topicsContainer.innerHTML = '';
            
            data.topics.forEach(topic => {
                const topicCard = document.createElement('div');
                topicCard.className = 'topic-card glass-card';
                topicCard.innerHTML = `
                    <div class="topic-icon">${getTopicIcon(topic)}</div>
                    <h3>${topic}</h3>
                    <button class="btn" onclick="startInterview('${topic}')">Start Interview</button>
                `;
                topicsContainer.appendChild(topicCard);
            });
        }
    } catch (error) {
        console.error('Failed to load topics:', error);
        showAlert('Failed to load topics. Please refresh the page.', 'error');
    }
}

function getTopicIcon(topic) {
    const icons = {
        'Python': '🐍',
        'DBMS': '🗄️',
        'DSA': '📊',
        'Java': '☕'
    };
    return icons[topic] || '📝';
}

// Start interview
async function startInterview(topic) {
    showLoading(true);
    
    try {
        const response = await apiRequest(`/start-interview/${topic}`, {
            method: 'POST'
        });
        
        if (!response.ok) {
            throw new Error('Failed to start interview');
        }
        
        const data = await response.json();
        
        currentSessionId = data.session_id;
        currentQuestionNumber = 1;
        totalQuestions = data.total_questions;
        currentTopic = topic;
        
        // Clear chat
        if (chatMessages) {
            chatMessages.innerHTML = '';
        }
        
        // Add first question
        addMessage(data.question, 'question');
        
        // Enable input
        if (answerInput) {
            answerInput.disabled = false;
            answerInput.focus();
        }
        if (submitBtn) {
            submitBtn.disabled = false;
        }
        
        // Update progress
        updateProgress();
        
        // Show interview view
        showView('interview');
        
    } catch (error) {
        showAlert(error.message || 'Failed to start interview', 'error');
        console.error(error);
    } finally {
        showLoading(false);
    }
}

// Submit answer
async function submitAnswer() {
    const answer = answerInput ? answerInput.value.trim() : '';
    
    if (!answer) {
        showAlert('Please enter an answer', 'error');
        return;
    }
    
    if (!currentSessionId) {
        showAlert('No active interview session', 'error');
        return;
    }
    
    // Disable input
    if (answerInput) answerInput.disabled = true;
    if (submitBtn) submitBtn.disabled = true;
    showLoading(true);
    
    // Add user's answer to chat
    addMessage(answer, 'answer');
    
    try {
        const response = await apiRequest('/answer', {
            method: 'POST',
            body: JSON.stringify({
                session_id: currentSessionId,
                answer: answer
            })
        });
        
        if (!response.ok) {
            throw new Error('Failed to submit answer');
        }
        
        const data = await response.json();
        
        // Add score and feedback
        addMessage(`Score: ${data.score}/10`, 'score');
        addMessage(`Feedback: ${data.feedback}`, 'feedback');
        
        // Clear input
        if (answerInput) answerInput.value = '';
        
        if (data.is_complete) {
            // Interview completed
            setTimeout(() => {
                showReport();
            }, 2000);
        } else {
            // Show next question
            currentQuestionNumber = data.question_number;
            updateProgress();
            
            setTimeout(() => {
                addMessage(data.next_question, 'question');
                if (answerInput) {
                    answerInput.disabled = false;
                    answerInput.focus();
                }
                if (submitBtn) submitBtn.disabled = false;
            }, 1000);
        }
    } catch (error) {
        showAlert(error.message || 'Failed to submit answer', 'error');
        console.error(error);
        if (answerInput) answerInput.disabled = false;
        if (submitBtn) submitBtn.disabled = false;
    } finally {
        showLoading(false);
    }
}

// Add message to chat
function addMessage(text, type) {
    if (!chatMessages) return;
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `message message-${type}`;
    messageDiv.textContent = text;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Update progress bar
function updateProgress() {
    if (!questionCounter || !progressFill) return;
    
    const percentage = (currentQuestionNumber / totalQuestions) * 100;
    progressFill.style.width = `${percentage}%`;
    questionCounter.textContent = `Question ${currentQuestionNumber} of ${totalQuestions}`;
}

// Show report
async function showReport() {
    showLoading(true);
    
    try {
        const response = await apiRequest(`/interview/${currentSessionId}/report`);
        
        if (!response.ok) {
            throw new Error('Failed to fetch report');
        }
        
        const report = await response.json();
        
        // Update report view
        const finalScoreEl = document.getElementById('final-score');
        const reportTopicEl = document.getElementById('report-topic');
        const questionsListEl = document.getElementById('questions-list');
        
        if (finalScoreEl) {
            finalScoreEl.textContent = report.total_score;
        }
        
        if (reportTopicEl) {
            reportTopicEl.textContent = `Topic: ${report.topic}`;
        }
        
        if (questionsListEl) {
            questionsListEl.innerHTML = '';
            
            report.questions.forEach((q, index) => {
                const questionItem = document.createElement('div');
                questionItem.className = 'question-item glass-card';
                questionItem.innerHTML = `
                    <div class="question-header">
                        <h4>Question ${q.question_number}</h4>
                        <span class="score-badge">${q.score}/10</span>
                    </div>
                    <p class="question-text">${q.question}</p>
                    <div class="answer-section">
                        <strong>Your Answer:</strong>
                        <p class="answer-text">${q.answer}</p>
                    </div>
                    <div class="feedback-section">
                        <strong>Feedback:</strong>
                        <p class="feedback-text">${q.feedback}</p>
                    </div>
                `;
                questionsListEl.appendChild(questionItem);
            });
        }
        
        showView('report');
        
    } catch (error) {
        showAlert(error.message || 'Failed to load report', 'error');
        console.error(error);
    } finally {
        showLoading(false);
    }
}

// Reset and go back to dashboard
function resetInterview() {
    currentSessionId = null;
    currentQuestionNumber = 1;
    totalQuestions = 5;
    currentTopic = null;
    
    if (chatMessages) chatMessages.innerHTML = '';
    if (answerInput) {
        answerInput.value = '';
        answerInput.disabled = false;
    }
    if (submitBtn) submitBtn.disabled = false;
    
    updateProgress();
    showView('dashboard');
}

// Logout
function handleLogout() {
    if (confirm('Are you sure you want to logout?')) {
        logout();
        window.location.href = '/login.html';
    }
}

// Handle Enter key in answer input (set up after DOM is ready)
document.addEventListener('DOMContentLoaded', () => {
    const answerInputEl = document.getElementById('answer-input');
    const submitBtnEl = document.getElementById('submit-btn');
    
    if (answerInputEl && submitBtnEl) {
        answerInputEl.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && e.ctrlKey && !submitBtnEl.disabled) {
                submitAnswer();
            }
        });
    }
});

// Make functions globally available
window.startInterview = startInterview;
window.submitAnswer = submitAnswer;
window.resetInterview = resetInterview;
window.handleLogout = handleLogout;

