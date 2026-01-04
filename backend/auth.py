"""
Authentication module for JWT-based user authentication and password hashing.
"""
from datetime import datetime, timedelta
from typing import Optional
import jwt
import bcrypt
import json
import os
from pathlib import Path

# JWT Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production-12345")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours

# User data storage (JSON file)
USERS_FILE = Path(__file__).parent / "users.json"


def get_users_db() -> dict:
    """Load users from JSON file."""
    if USERS_FILE.exists():
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return {}


def save_users_db(users: dict):
    """Save users to JSON file."""
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> Optional[dict]:
    """Verify and decode a JWT token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def register_user(username: str, email: str, password: str) -> tuple[bool, str]:
    """
    Register a new user.
    Returns (success: bool, message: str)
    """
    users = get_users_db()
    
    # Check if username already exists
    if username in users:
        return False, "Username already exists"
    
    # Check if email already exists
    for user_data in users.values():
        if user_data.get("email") == email:
            return False, "Email already registered"
    
    # Create new user
    users[username] = {
        "username": username,
        "email": email,
        "password_hash": hash_password(password),
        "created_at": datetime.utcnow().isoformat()
    }
    
    save_users_db(users)
    return True, "User registered successfully"


def authenticate_user(username: str, password: str) -> Optional[dict]:
    """
    Authenticate a user and return user data if successful.
    Returns None if authentication fails.
    """
    users = get_users_db()
    
    if username not in users:
        return None
    
    user_data = users[username]
    
    if not verify_password(password, user_data["password_hash"]):
        return None
    
    # Return user data without password hash
    return {
        "username": user_data["username"],
        "email": user_data["email"]
    }


def get_user_by_username(username: str) -> Optional[dict]:
    """Get user data by username."""
    users = get_users_db()
    if username in users:
        user_data = users[username].copy()
        user_data.pop("password_hash", None)
        return user_data
    return None

