"""
Session manager for tracking interview sessions.
"""
from typing import Dict, Optional
from datetime import datetime
import uuid


class InterviewSession:
    """Represents an interview session."""
    
    def __init__(self, session_id: str, username: str, topic: str, questions: list):
        self.session_id = session_id
        self.username = username
        self.topic = topic
        self.questions = questions
        self.current_question_index = 0
        self.answers = []
        self.scores = []
        self.feedbacks = []
        self.total_score = 0.0
        self.created_at = datetime.utcnow().isoformat()
        self.completed = False
    
    def submit_answer(self, answer: str, score: float, feedback: str):
        """Submit an answer for the current question."""
        self.answers.append(answer)
        self.scores.append(score)
        self.feedbacks.append(feedback)
        self.total_score += score
        self.current_question_index += 1
        
        if self.current_question_index >= len(self.questions):
            self.completed = True
    
    def get_current_question(self) -> Optional[dict]:
        """Get the current question data."""
        if self.current_question_index < len(self.questions):
            return self.questions[self.current_question_index]
        return None
    
    def get_average_score(self) -> float:
        """Calculate and return the average score."""
        if len(self.scores) == 0:
            return 0.0
        return round(self.total_score / len(self.scores), 2)
    
    def to_dict(self) -> dict:
        """Convert session to dictionary for JSON serialization."""
        return {
            "session_id": self.session_id,
            "username": self.username,
            "topic": self.topic,
            "current_question_index": self.current_question_index,
            "total_questions": len(self.questions),
            "answers": self.answers,
            "scores": self.scores,
            "feedbacks": self.feedbacks,
            "total_score": self.total_score,
            "average_score": self.get_average_score(),
            "created_at": self.created_at,
            "completed": self.completed
        }


class SessionManager:
    """Manages interview sessions."""
    
    def __init__(self):
        self.sessions: Dict[str, InterviewSession] = {}
    
    def create_session(self, username: str, topic: str, questions: list) -> InterviewSession:
        """Create a new interview session."""
        session_id = str(uuid.uuid4())
        session = InterviewSession(session_id, username, topic, questions)
        self.sessions[session_id] = session
        return session
    
    def get_session(self, session_id: str) -> Optional[InterviewSession]:
        """Get a session by ID."""
        return self.sessions.get(session_id)
    
    def get_user_sessions(self, username: str) -> list:
        """Get all sessions for a user."""
        return [s for s in self.sessions.values() if s.username == username]
    
    def delete_session(self, session_id: str) -> bool:
        """Delete a session."""
        if session_id in self.sessions:
            del self.sessions[session_id]
            return True
        return False


# Global session manager instance
session_manager = SessionManager()

