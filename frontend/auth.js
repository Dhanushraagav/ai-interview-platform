/**
 * Authentication utility functions
 */


const API_BASE_URL = "https://ai-interview-platform-50c3.onrender.com";

// Token management
function getToken() {
    return localStorage.getItem('auth_token');
}

function setToken(token) {
    localStorage.setItem('auth_token', token);
}

function removeToken() {
    localStorage.removeItem('auth_token');
}

function getUser() {
    const userStr = localStorage.getItem('user');
    return userStr ? JSON.parse(userStr) : null;
}

function setUser(user) {
    localStorage.setItem('user', JSON.stringify(user));
}

function removeUser() {
    localStorage.removeItem('user');
}

// Check if user is authenticated
function isAuthenticated() {
    return getToken() !== null;
}

// Get auth headers for API requests
function getAuthHeaders() {
    const token = getToken();
    return {
        'Content-Type': 'application/json',
        ...(token && { 'Authorization': `Bearer ${token}` })
    };
}

// Make authenticated API request
async function apiRequest(url, options = {}) {
    const headers = getAuthHeaders();
    
    const response = await fetch(`${API_BASE_URL}${url}`, {
        ...options,
        headers: {
            ...headers,
            ...options.headers
        }
    });
    
    if (response.status === 401) {
        // Token expired or invalid
        logout();
        window.location.href = '/login.html';
        throw new Error('Authentication required');
    }
    
    return response;
}

// Signup
async function signup(username, email, password) {
    const response = await fetch(`${API_BASE_URL}/signup`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, email, password })
    });
    
    const data = await response.json();
    
    if (!response.ok) {
        throw new Error(data.detail || 'Signup failed');
    }
    
    return data;
}

// Login
async function login(username, password) {
    const response = await fetch(`${API_BASE_URL}/login`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, password })
    });
    
    const data = await response.json();
    
    if (!response.ok) {
        throw new Error(data.detail || 'Login failed');
    }
    
    // Store token and user
    setToken(data.access_token);
    setUser(data.user);
    window.location.href = "/interview.html";
    return data;
}


// Logout
function logout() {
    removeToken();
    removeUser();
}

// Get current user info
async function getCurrentUser() {
    const response = await apiRequest('/me');
    
    if (!response.ok) {
        throw new Error('Failed to get user info');
    }
    
    const user = await response.json();
    setUser(user);
    return user;
}

// Show alert message
function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.textContent = message;
    
    // Insert at the top of the container
    const container = document.querySelector('.container');
    if (container) {
        container.insertBefore(alertDiv, container.firstChild);
        
        // Remove after 5 seconds
        setTimeout(() => {
            alertDiv.remove();
        }, 5000);
    }
}

// Show loading overlay
function showLoading(show = true) {
    let overlay = document.getElementById('loading-overlay');
    
    if (!overlay) {
        overlay = document.createElement('div');
        overlay.id = 'loading-overlay';
        overlay.className = 'loading-overlay';
        overlay.innerHTML = '<div class="spinner"></div><p>Loading...</p>';
        document.body.appendChild(overlay);
    }
    
    if (show) {
        overlay.classList.add('active');
    } else {
        overlay.classList.remove('active');
    }
}

// Redirect if not authenticated
function requireAuth() {
    if (!isAuthenticated()) {
        window.location.href = '/login.html';
        return false;
    }
    return true;
}

