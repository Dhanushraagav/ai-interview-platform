from datetime import datetime, timedelta
from typing import Optional
import jwt
from passlib.context import CryptContext

# Secret key for JWT (in production, use environment variable)
SECRET_KEY = "your-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# In-memory user storage
users_db = {}


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password."""
    return pwd_context.hash(password)


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
    except jwt.JWTError:
        return None


def register_user(username: str, email: str, password: str) -> dict:
    """Register a new user."""
    if username in users_db:
        return {"error": "Username already exists"}
    if any(user["email"] == email for user in users_db.values()):
        return {"error": "Email already exists"}
    
    hashed_password = get_password_hash(password)
    users_db[username] = {
        "username": username,
        "email": email,
        "hashed_password": hashed_password
    }
    return {"message": "User registered successfully"}


def authenticate_user(username: str, password: str) -> Optional[dict]:
    """Authenticate a user and return user info if successful."""
    user = users_db.get(username)
    if not user:
        return None
    if not verify_password(password, user["hashed_password"]):
        return None
    return {"username": user["username"], "email": user["email"]}

