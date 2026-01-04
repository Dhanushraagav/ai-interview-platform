"""
Interview engine for generating questions based on topics.
"""

# Available interview topics
TOPICS = [
    "Python",
    "JavaScript",
    "Data Structures",
    "Algorithms",
    "System Design",
    "Database",
    "Web Development",
    "Machine Learning",
    "DevOps",
    "Security"
]

# Question templates for each topic
QUESTION_TEMPLATES = {
    "Python": [
        "Explain the difference between a list and a tuple in Python.",
        "What is a decorator in Python? Provide an example.",
        "How does Python handle memory management?",
        "Explain the Global Interpreter Lock (GIL) in Python.",
        "What are generators and how do they differ from regular functions?"
    ],
    "JavaScript": [
        "Explain the difference between var, let, and const.",
        "What is closure in JavaScript? Provide an example.",
        "Explain the event loop in JavaScript.",
        "What is the difference between == and === in JavaScript?",
        "How does async/await work in JavaScript?"
    ],
    "Data Structures": [
        "Explain the time complexity of common operations in a hash table.",
        "What is the difference between a stack and a queue?",
        "Explain how a binary search tree works.",
        "What are the advantages and disadvantages of linked lists?",
        "Explain the concept of a heap data structure."
    ],
    "Algorithms": [
        "Explain the difference between BFS and DFS.",
        "What is dynamic programming? Provide an example.",
        "Explain the time complexity of quicksort.",
        "What is the difference between greedy and divide-and-conquer algorithms?",
        "Explain how binary search works and its time complexity."
    ],
    "System Design": [
        "How would you design a URL shortener like bit.ly?",
        "Explain the CAP theorem and its implications.",
        "How would you design a distributed caching system?",
        "What are the key considerations when designing a scalable web application?",
        "Explain load balancing strategies."
    ],
    "Database": [
        "Explain the difference between SQL and NoSQL databases.",
        "What is database normalization and why is it important?",
        "Explain ACID properties in database transactions.",
        "What is indexing and how does it improve query performance?",
        "Explain the difference between inner join and outer join."
    ],
    "Web Development": [
        "Explain the difference between REST and GraphQL.",
        "What is CORS and why is it needed?",
        "Explain the difference between authentication and authorization.",
        "What are the key principles of responsive web design?",
        "Explain how HTTP/2 differs from HTTP/1.1."
    ],
    "Machine Learning": [
        "Explain the difference between supervised and unsupervised learning.",
        "What is overfitting and how can it be prevented?",
        "Explain the bias-variance tradeoff.",
        "What is cross-validation and why is it important?",
        "Explain the difference between classification and regression."
    ],
    "DevOps": [
        "Explain the difference between continuous integration and continuous deployment.",
        "What is containerization and how does it differ from virtualization?",
        "Explain the concept of infrastructure as code.",
        "What are the benefits of using a CI/CD pipeline?",
        "Explain the difference between Docker and Kubernetes."
    ],
    "Security": [
        "Explain the difference between symmetric and asymmetric encryption.",
        "What is SQL injection and how can it be prevented?",
        "Explain the OWASP Top 10 security risks.",
        "What is XSS (Cross-Site Scripting) and how can it be prevented?",
        "Explain the principle of least privilege."
    ]
}


def get_topics() -> list:
    """Get list of available interview topics."""
    return TOPICS


def generate_questions(topic: str, count: int = 5) -> list:
    """Generate interview questions for a given topic."""
    if topic not in QUESTION_TEMPLATES:
        return []
    
    questions = QUESTION_TEMPLATES.get(topic, [])
    # Return up to 'count' questions, or all if less than count
    return questions[:count] if len(questions) > count else questions

