from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from backend import auth
from backend import interview_engine

app = FastAPI(title="AI Interview Platform API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request/Response models
class SignupRequest(BaseModel):
    username: str
    email: str
    password: str


class LoginRequest(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    username: str
    email: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TopicsResponse(BaseModel):
    topics: list


class QuestionsResponse(BaseModel):
    topic: str
    questions: list


# Dependency to verify token
async def verify_token_dependency(authorization: Optional[str] = Header(None)):
    """Verify JWT token from Authorization header."""
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Invalid authentication scheme")
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid authorization header format")
    
    payload = auth.verify_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    return payload


@app.get("/")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "message": "AI Interview Platform API is running"}


@app.post("/signup", response_model=dict)
async def signup(request: SignupRequest):
    """Register a new user."""
    result = auth.register_user(
        username=request.username,
        email=request.email,
        password=request.password
    )
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return result


@app.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest):
    """Login and get JWT token."""
    user = auth.authenticate_user(request.username, request.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    access_token = auth.create_access_token(data={"sub": user["username"]})
    return TokenResponse(access_token=access_token, token_type="bearer")


@app.get("/me", response_model=UserResponse)
async def get_current_user(payload: dict = Depends(verify_token_dependency)):
    """Get current user information."""
    username = payload.get("sub")
    if not username or username not in auth.users_db:
        raise HTTPException(status_code=401, detail="User not found")
    
    user = auth.users_db[username]
    return UserResponse(username=user["username"], email=user["email"])


@app.get("/topics", response_model=TopicsResponse)
async def get_topics(payload: dict = Depends(verify_token_dependency)):
    """Get list of available interview topics."""
    topics = interview_engine.get_topics()
    return TopicsResponse(topics=topics)


@app.get("/questions", response_model=QuestionsResponse)
async def get_questions(
    topic: str,
    count: int = 5,
    payload: dict = Depends(verify_token_dependency)
):
    """Get interview questions for a specific topic."""
    if not topic:
        raise HTTPException(status_code=400, detail="Topic parameter is required")
    
    questions = interview_engine.generate_questions(topic, count)
    if not questions:
        raise HTTPException(status_code=404, detail=f"Topic '{topic}' not found")
    
    return QuestionsResponse(topic=topic, questions=questions)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

