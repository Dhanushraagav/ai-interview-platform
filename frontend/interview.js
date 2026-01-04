// API configuration - easy to change for different environments
const API_BASE_URL = 'http://localhost:8000';

// Get auth headers with token
function getAuthHeaders() {
    const token = localStorage.getItem('token');
    return {
        'Content-Type': 'application/json',
        ...(token && { 'Authorization': `Bearer ${token}` })
    };
}

// Load topics from backend
async function loadTopics() {
    try {
        const response = await fetch(`${API_BASE_URL}/topics`, {
            headers: getAuthHeaders()
        });

        if (!response.ok) {
            if (response.status === 401) {
                window.location.href = 'login.html';
                return;
            }
            throw new Error('Failed to load topics');
        }

        const data = await response.json();
        return data.topics;
    } catch (error) {
        console.error('Error loading topics:', error);
        showError('Failed to load topics. Please try again.');
        return [];
    }
}

// Generate questions for a topic
async function generateQuestions(topic, count = 5) {
    try {
        const response = await fetch(`${API_BASE_URL}/questions?topic=${encodeURIComponent(topic)}&count=${count}`, {
            headers: getAuthHeaders()
        });

        if (!response.ok) {
            if (response.status === 401) {
                window.location.href = 'login.html';
                return;
            }
            throw new Error('Failed to generate questions');
        }

        const data = await response.json();
        return data.questions;
    } catch (error) {
        console.error('Error generating questions:', error);
        showError('Failed to generate questions. Please try again.');
        return [];
    }
}

// Display topics in the UI
function displayTopics(topics) {
    const topicsContainer = document.getElementById('topics-container');
    if (!topicsContainer) return;

    topicsContainer.innerHTML = '';

    if (topics.length === 0) {
        topicsContainer.innerHTML = '<p class="no-topics">No topics available</p>';
        return;
    }

    topics.forEach(topic => {
        const topicCard = document.createElement('div');
        topicCard.className = 'topic-card';
        topicCard.innerHTML = `
            <h3>${topic}</h3>
            <button class="btn btn-primary" onclick="startInterview('${topic}')">Start Interview</button>
        `;
        topicsContainer.appendChild(topicCard);
    });
}

// Start interview for selected topic
async function startInterview(topic) {
    const loadingIndicator = document.getElementById('loading');
    const questionsContainer = document.getElementById('questions-container');
    const topicsSection = document.getElementById('topics-section');

    // Show loading
    if (loadingIndicator) loadingIndicator.style.display = 'block';
    if (questionsContainer) questionsContainer.innerHTML = '';
    if (topicsSection) topicsSection.style.display = 'none';

    // Generate questions
    const questions = await generateQuestions(topic);

    // Hide loading
    if (loadingIndicator) loadingIndicator.style.display = 'none';

    if (questions.length === 0) {
        showError('No questions available for this topic.');
        if (topicsSection) topicsSection.style.display = 'block';
        return;
    }

    // Display questions
    displayQuestions(topic, questions);
}

// Display questions
function displayQuestions(topic, questions) {
    const questionsContainer = document.getElementById('questions-container');
    const questionsSection = document.getElementById('questions-section');
    const topicsSection = document.getElementById('topics-section');

    if (!questionsContainer) return;

    if (topicsSection) topicsSection.style.display = 'none';
    if (questionsSection) questionsSection.style.display = 'block';

    questionsContainer.innerHTML = `
        <div class="questions-header">
            <h2>Interview Questions: ${topic}</h2>
            <button class="btn btn-secondary" onclick="goBackToTopics()">Back to Topics</button>
        </div>
        <div class="questions-list">
            ${questions.map((q, index) => `
                <div class="question-card">
                    <div class="question-number">Question ${index + 1}</div>
                    <div class="question-text">${q}</div>
                </div>
            `).join('')}
        </div>
    `;
}

// Go back to topics
function goBackToTopics() {
    const topicsSection = document.getElementById('topics-section');
    const questionsSection = document.getElementById('questions-section');

    if (topicsSection) topicsSection.style.display = 'block';
    if (questionsSection) questionsSection.style.display = 'none';
}

// Show error message
function showError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = message;
    document.body.insertBefore(errorDiv, document.body.firstChild);

    setTimeout(() => {
        errorDiv.remove();
    }, 5000);
}

// Initialize interview page
async function initInterviewPage() {
    // Check authentication
    const isAuthenticated = await requireAuth();
    if (!isAuthenticated) return;

    // Show loading indicator
    const loadingIndicator = document.getElementById('loading');
    if (loadingIndicator) loadingIndicator.style.display = 'block';

    // Load and display topics
    const topics = await loadTopics();
    
    // Hide loading indicator
    if (loadingIndicator) loadingIndicator.style.display = 'none';
    
    displayTopics(topics);
}

// Import requireAuth from auth.js (will be available if auth.js is loaded first)
async function requireAuth() {
    const token = localStorage.getItem('token');
    if (!token) {
        window.location.href = 'login.html';
        return false;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/me`, {
            headers: getAuthHeaders()
        });

        if (response.ok) {
            return true;
        } else {
            localStorage.removeItem('token');
            window.location.href = 'login.html';
            return false;
        }
    } catch (error) {
        console.error('Auth check failed:', error);
        localStorage.removeItem('token');
        window.location.href = 'login.html';
        return false;
    }
}

