# AI Interview Platform

A production-ready full-stack web application for conducting AI-powered technical interviews with automatic question generation, real-time answer evaluation, and comprehensive performance reports.

## 🌟 Features

- **🔐 User Authentication**: Secure JWT-based login and signup with password hashing
- **🎯 Multiple Topics**: Interview topics include Python, DBMS, DSA, and Java
- **🤖 AI-Powered Evaluation**: Automatic answer scoring and detailed feedback
- **💬 Chat-Style Interface**: Interactive question-answer flow with real-time feedback
- **📊 Detailed Reports**: Comprehensive performance analysis with question-wise breakdown
- **🎨 Modern UI**: Beautiful glassmorphism design with animated gradients
- **📱 Mobile Responsive**: Fully responsive design for all devices
- **🔒 Protected Endpoints**: Secure API with authentication requirements

## 🛠️ Technology Stack

- **Backend**: Python FastAPI
- **Frontend**: HTML, CSS, JavaScript (Vanilla JS)
- **Authentication**: JWT tokens with bcrypt password hashing
- **Storage**: JSON file-based storage (easily replaceable with database)
- **Deployment**: Render.com ready

## 📁 Project Structure

```
ai-interview-platform/
├── backend/
│   ├── main.py              # FastAPI application and routes
│   ├── auth.py              # Authentication and JWT handling
│   ├── interview_engine.py  # Question generation logic
│   ├── scoring.py           # Answer evaluation and scoring
│   ├── session_manager.py   # Interview session management
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── index.html          # Landing page
│   ├── login.html          # Login page
│   ├── signup.html         # Signup page
│   ├── interview.html      # Dashboard, interview, and report views
│   ├── styles.css          # Global styles with glassmorphism
│   ├── auth.js             # Authentication utilities
│   └── interview.js        # Interview functionality
├── Procfile                # Render deployment configuration
└── README.md               # This file
```

## 🚀 Setup Instructions

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git (for cloning)

### Local Development

1. **Clone or navigate to the project directory**
   ```bash
   cd ai-interview-platform
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   
   **On Windows:**
   ```bash
   venv\Scripts\activate
   ```
   
   **On macOS/Linux:**
   ```bash
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

5. **Set environment variable (optional)**
   ```bash
   # For production, set a strong secret key
   export SECRET_KEY="your-very-secure-secret-key-here"
   ```

6. **Run the application**
   ```bash
   # From the project root
   uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
   ```

7. **Open your browser**
   - Frontend: `http://localhost:8000`
   - API Documentation: `http://localhost:8000/docs`
   - Alternative API docs: `http://localhost:8000/redoc`

## 📡 API Endpoints

### Public Endpoints

#### 1. Sign Up
- **Endpoint**: `POST /signup`
- **Description**: Register a new user account
- **Request Body**:
  ```json
  {
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securepassword123"
  }
  ```
- **Response**: Success message and username

#### 2. Login
- **Endpoint**: `POST /login`
- **Description**: Authenticate and receive JWT token
- **Request Body**:
  ```json
  {
    "username": "john_doe",
    "password": "securepassword123"
  }
  ```
- **Response**: JWT access token and user information

### Protected Endpoints (Require Authentication)

All protected endpoints require a Bearer token in the Authorization header:
```
Authorization: Bearer <your-jwt-token>
```

#### 3. Get Current User
- **Endpoint**: `GET /me`
- **Description**: Get information about the currently logged-in user
- **Headers**: `Authorization: Bearer <token>`
- **Response**: User information (username, email)

#### 4. Get Available Topics
- **Endpoint**: `GET /topics`
- **Description**: Get list of available interview topics
- **Response**: List of topics (Python, DBMS, DSA, Java)

#### 5. Start Interview
- **Endpoint**: `POST /start-interview/{topic}`
- **Description**: Start a new interview session
- **Path Parameter**: `topic` (Python, DBMS, DSA, or Java)
- **Response**: Session ID and first question

#### 6. Submit Answer
- **Endpoint**: `POST /answer`
- **Description**: Submit an answer for the current question
- **Request Body**:
  ```json
  {
    "session_id": "uuid-here",
    "answer": "Your answer text here"
  }
  ```
- **Response**: Score, feedback, and next question (if available)

#### 7. Get Interview Report
- **Endpoint**: `GET /interview/{session_id}/report`
- **Description**: Get final report for a completed interview
- **Response**: Complete report with all questions, answers, scores, and feedback

#### 8. Get Interview Status
- **Endpoint**: `GET /interview/{session_id}/status`
- **Description**: Get current status of an interview session
- **Response**: Session status, progress, and current score

## 🚢 Deployment on Render

### Step 1: Prepare Your Repository

1. **Push your code to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: AI Interview Platform"
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

### Step 2: Deploy on Render

1. **Create a Render account** at [render.com](https://render.com)

2. **Create a new Web Service**
   - Click "New" → "Web Service"
   - Connect your GitHub repository
   - Select the repository containing this project

3. **Configure the service**
   - **Name**: `ai-interview-platform` (or your preferred name)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
   - Render will automatically detect the `Procfile` if present

4. **Set Environment Variables** (Optional but recommended)
   - Go to "Environment" tab
   - Add `SECRET_KEY` with a strong random string
   - You can generate one using:
     ```python
     import secrets
     print(secrets.token_urlsafe(32))
     ```

5. **Deploy**
   - Click "Create Web Service"
   - Render will automatically build and deploy your application
   - Your app will be available at `https://your-app-name.onrender.com`

### Step 3: Verify Deployment

- Visit your Render URL
- Test the signup and login functionality
- Try starting an interview
- Check API documentation at `/docs`

## 🔒 Security Features

- **Password Hashing**: All passwords are hashed using bcrypt before storage
- **JWT Authentication**: Secure token-based authentication
- **Protected Routes**: Interview endpoints require valid authentication
- **CORS Configuration**: Configured for secure cross-origin requests
- **Input Validation**: All inputs are validated using Pydantic models

## 🎨 UI Features

- **Glassmorphism Design**: Modern frosted glass effect cards
- **Animated Gradients**: Smooth gradient animations in the background
- **Responsive Layout**: Mobile-first design that works on all devices
- **Smooth Animations**: Fade-in, slide-in, and hover effects
- **Real-time Feedback**: Instant visual feedback for user actions

## 📊 Scoring System

Each answer is evaluated based on:
- **Keyword Matching (70%)**: Checks if key concepts are mentioned
- **Answer Depth (20%)**: Encourages detailed, comprehensive answers
- **Relevance (10%)**: Ensures answer addresses the question topic

Scores range from 0-10, with detailed feedback provided after each answer.

## 🧪 Testing the Application

1. **Create an account** at the signup page
2. **Login** with your credentials
3. **Select a topic** from the dashboard
4. **Answer questions** in the chat interface
5. **View your report** after completing all questions

## 📝 Notes

- User data is stored in `backend/users.json` (file-based storage)
- Interview sessions are stored in memory (reset on server restart)
- For production, consider using a database (PostgreSQL, MongoDB, etc.)
- JWT tokens expire after 24 hours (configurable in `auth.py`)
- The frontend automatically handles token storage and refresh

## 🐛 Troubleshooting

### Issue: "Module not found" errors
**Solution**: Make sure you've installed all requirements:
```bash
pip install -r backend/requirements.txt
```

### Issue: CORS errors in browser
**Solution**: The backend is configured to allow all origins. For production, update `allow_origins` in `main.py` with your frontend domain.

### Issue: Port already in use
**Solution**: Use a different port:
```bash
uvicorn backend.main:app --reload --port 8001
```

### Issue: Authentication fails
**Solution**: 
- Check that you're including the Bearer token in requests
- Verify token hasn't expired (24-hour default)
- Ensure password is correct

## 🔄 Future Enhancements

- Database integration (PostgreSQL/MongoDB)
- User profile management
- Interview history and analytics
- Multiple interview attempts per topic
- Export reports as PDF
- Email notifications
- Admin dashboard
- Real-time collaboration features

## 📄 License

This project is open source and available for educational and commercial purposes.

## 👥 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For issues or questions:
1. Check the API documentation at `/docs` when the server is running
2. Review the code comments for implementation details
3. Open an issue on GitHub

---

**Built with ❤️ using FastAPI and modern web technologies**

