// API configuration - easy to change for different environments
const API_BASE_URL = 'http://localhost:8000';

// Token management
function getToken() {
    return localStorage.getItem('token');
}

function setToken(token) {
    localStorage.setItem('token', token);
}

function clearToken() {
    localStorage.removeItem('token');
}

function getAuthHeaders() {
    const token = getToken();
    return {
        'Content-Type': 'application/json',
        ...(token && { 'Authorization': `Bearer ${token}` })
    };
}

// Check if user is authenticated
async function checkAuth() {
    const token = getToken();
    if (!token) {
        return false;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/me`, {
            headers: getAuthHeaders()
        });

        if (response.ok) {
            return true;
        } else {
            clearToken();
            return false;
        }
    } catch (error) {
        console.error('Auth check failed:', error);
        clearToken();
        return false;
    }
}

// Redirect to login if not authenticated
async function requireAuth() {
    const isAuthenticated = await checkAuth();
    if (!isAuthenticated) {
        window.location.href = 'login.html';
        return false;
    }
    return true;
}

// Signup function
async function signup(username, email, password) {
    try {
        const response = await fetch(`${API_BASE_URL}/signup`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, email, password })
        });

        const data = await response.json();

        if (response.ok) {
            return { success: true, message: data.message || 'Signup successful' };
        } else {
            return { success: false, error: data.detail || 'Signup failed' };
        }
    } catch (error) {
        return { success: false, error: 'Network error. Please try again.' };
    }
}

// Login function
async function login(username, password) {
    try {
        const response = await fetch(`${API_BASE_URL}/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password })
        });

        const data = await response.json();

        if (response.ok) {
            setToken(data.access_token);
            return { success: true, token: data.access_token };
        } else {
            return { success: false, error: data.detail || 'Login failed' };
        }
    } catch (error) {
        return { success: false, error: 'Network error. Please try again.' };
    }
}

// Logout function
function logout() {
    clearToken();
    window.location.href = 'login.html';
}

