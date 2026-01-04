"""
Main FastAPI application for AI Interview Platform.
"""
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import timedelta
import os
from pathlib import Path

from .auth import (
    register_user, authenticate_user, create_access_token, 
    verify_token, get_user_by_username, ACCESS_TOKEN_EXPIRE_MINUTES
)
from .interview_engine import get_questions_for_topic, get_available_topics
from .scoring import evaluate_answer
from .session_manager import session_manager

# Initialize FastAPI app
app = FastAPI(
    title="AI Interview Platform API",
    description="Production-ready AI-powered interview and skill evaluation platform",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://ai-interview-platform-50c3.onrender.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security scheme
security = HTTPBearer()


# Pydantic models
class SignupRequest(BaseModel):
    username: str
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    username: str
    password: str


class AnswerRequest(BaseModel):
    session_id: str
    answer: str


class StartInterviewRequest(BaseModel):
    topic: str


# Dependency to get current user from JWT token
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """Verify JWT token and return current user."""
    token = credentials.credentials
    payload = verify_token(token)
    
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    username = payload.get("sub")
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )
    
    user = get_user_by_username(username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    return user


# Authentication endpoints
@app.post("/signup")
async def signup(request: SignupRequest):
    """
    Register a new user.
    """
    # Validate input
    if len(request.username) < 3:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username must be at least 3 characters long"
        )
    
    if len(request.password) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 6 characters long"
        )
    
    success, message = register_user(request.username, request.email, request.password)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message
        )
    
    return {
        "success": True,
        "message": message,
        "username": request.username
    }


@app.post("/login")
async def login(request: LoginRequest):
    """
    Login and receive JWT token.
    """
    user = authenticate_user(request.username, request.password)
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }


@app.get("/me")
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """
    Get current logged-in user information.
    Protected endpoint - requires authentication.
    """
    return current_user


# Interview endpoints (protected)
@app.get("/topics")
async def get_topics(current_user: dict = Depends(get_current_user)):
    """
    Get list of available interview topics.
    Protected endpoint.
    """
    return {
        "topics": get_available_topics()
    }


@app.post("/start-interview/{topic}")
async def start_interview(
    topic: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Start a new interview session for the given topic.
    Protected endpoint - requires authentication.
    """
    try:
        # Get questions for the topic
        questions = get_questions_for_topic(topic)
        
        # Create new session
        session = session_manager.create_session(
            username=current_user["username"],
            topic=topic,
            questions=questions
        )
        
        # Get first question
        first_question = questions[0]
        
        return {
            "success": True,
            "session_id": session.session_id,
            "question": first_question["question"],
            "question_number": 1,
            "total_questions": len(questions),
            "topic": topic
        }
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@app.post("/answer")
async def submit_answer(
    request: AnswerRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Submit an answer for the current question.
    Protected endpoint - requires authentication.
    """
    # Get session
    session = session_manager.get_session(request.session_id)
    
    if session is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview session not found"
        )
    
    # Verify session belongs to current user
    if session.username != current_user["username"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this session"
        )
    
    # Check if interview is already completed
    if session.completed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Interview already completed"
        )
    
    # Get current question
    current_question = session.get_current_question()
    if current_question is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No more questions available"
        )
    
    # Evaluate answer
    score, feedback = evaluate_answer(
        question=current_question["question"],
        answer=request.answer,
        keywords=current_question["keywords"]
    )
    
    # Submit answer to session
    session.submit_answer(request.answer, score, feedback)
    
    # Prepare response
    response = {
        "success": True,
        "score": score,
        "feedback": feedback,
        "question_number": session.current_question_index,
        "total_questions": len(session.questions),
        "is_complete": session.completed
    }
    
    # If interview is complete, add final score
    if session.completed:
        response["total_score"] = session.get_average_score()
        response["message"] = "Interview completed! Great job!"
    else:
        # Get next question
        next_question = session.get_current_question()
        response["next_question"] = next_question["question"]
    
    return response


@app.get("/interview/{session_id}/report")
async def get_interview_report(
    session_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Get the final report for a completed interview.
    Protected endpoint - requires authentication.
    """
    session = session_manager.get_session(session_id)
    
    if session is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview session not found"
        )
    
    # Verify session belongs to current user
    if session.username != current_user["username"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this session"
        )
    
    if not session.completed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Interview not yet completed"
        )
    
    # Build report
    report = {
        "session_id": session.session_id,
        "topic": session.topic,
        "total_score": session.get_average_score(),
        "max_score": 10.0,
        "created_at": session.created_at,
        "questions": []
    }
    
    # Add question-answer pairs
    for i, question_data in enumerate(session.questions):
        report["questions"].append({
            "question_number": i + 1,
            "question": question_data["question"],
            "answer": session.answers[i],
            "score": session.scores[i],
            "feedback": session.feedbacks[i]
        })
    
    return report


@app.get("/interview/{session_id}/status")
async def get_interview_status(
    session_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Get the current status of an interview session.
    Protected endpoint.
    """
    session = session_manager.get_session(session_id)
    
    if session is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview session not found"
        )
    
    # Verify session belongs to current user
    if session.username != current_user["username"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this session"
        )
    
    return {
        "session_id": session.session_id,
        "topic": session.topic,
        "current_question": session.current_question_index + 1,
        "total_questions": len(session.questions),
        "completed": session.completed,
        "average_score": session.get_average_score() if session.completed else None
    }


# Serve frontend files
frontend_path = Path(__file__).parent.parent / "frontend"
if frontend_path.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_path)), name="static")
    
    @app.get("/")
    async def serve_landing():
        return FileResponse(str(frontend_path / "index.html"))
    
    @app.get("/login.html")
    async def serve_login():
        return FileResponse(str(frontend_path / "login.html"))
    
    @app.get("/signup.html")
    async def serve_signup():
        return FileResponse(str(frontend_path / "signup.html"))
    
    @app.get("/interview.html")
    async def serve_interview():
        return FileResponse(str(frontend_path / "interview.html"))


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

