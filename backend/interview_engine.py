"""
Interview engine for generating questions based on topics.
"""
from typing import List, Dict

# Question templates for different topics
QUESTION_BANK = {
    "Python": [
        {
            "question": "What is the difference between a list and a tuple in Python? Explain with examples.",
            "keywords": ["mutable", "immutable", "list", "tuple", "modification", "performance", "syntax"]
        },
        {
            "question": "Explain the concept of decorators in Python. Provide a practical example of how you would use one.",
            "keywords": ["decorator", "function", "wrapper", "@", "syntax", "example", "closure"]
        },
        {
            "question": "What is the difference between __str__ and __repr__ methods? When would you use each?",
            "keywords": ["__str__", "__repr__", "string", "representation", "debugging", "user-friendly", "developer"]
        },
        {
            "question": "How does Python handle memory management? Explain garbage collection and reference counting.",
            "keywords": ["memory", "garbage collection", "reference counting", "cyclic", "gc module", "automatic"]
        },
        {
            "question": "What are Python generators and how do they differ from regular functions? When would you use a generator?",
            "keywords": ["generator", "yield", "iterator", "lazy evaluation", "memory efficient", "iterable"]
        }
    ],
    "DBMS": [
        {
            "question": "Explain ACID properties in database transactions. Why are they important?",
            "keywords": ["ACID", "atomicity", "consistency", "isolation", "durability", "transaction", "integrity"]
        },
        {
            "question": "What is the difference between primary key and foreign key? Provide examples of their usage.",
            "keywords": ["primary key", "foreign key", "unique", "reference", "relationship", "constraint", "integrity"]
        },
        {
            "question": "Explain database normalization and its different forms (1NF, 2NF, 3NF). What problems does it solve?",
            "keywords": ["normalization", "1NF", "2NF", "3NF", "redundancy", "dependency", "anomaly"]
        },
        {
            "question": "What is the difference between INNER JOIN and LEFT JOIN? When would you use each?",
            "keywords": ["INNER JOIN", "LEFT JOIN", "RIGHT JOIN", "matching", "NULL", "rows", "outer"]
        },
        {
            "question": "Explain database indexing and its benefits and drawbacks. What types of indexes exist?",
            "keywords": ["index", "B-tree", "performance", "query", "storage", "maintenance", "clustered"]
        }
    ],
    "DSA": [
        {
            "question": "Explain the time complexity of binary search and when it can be used. What are its requirements?",
            "keywords": ["binary search", "O(log n)", "sorted", "divide", "conquer", "efficiency", "array"]
        },
        {
            "question": "What is the difference between a stack and a queue? Provide real-world use cases for each.",
            "keywords": ["stack", "queue", "LIFO", "FIFO", "push", "pop", "enqueue", "dequeue", "operations"]
        },
        {
            "question": "Explain dynamic programming and provide an example problem. What are its key characteristics?",
            "keywords": ["dynamic programming", "memoization", "overlapping", "subproblems", "optimization", "recursion"]
        },
        {
            "question": "What is the difference between BFS and DFS? When would you use each algorithm?",
            "keywords": ["BFS", "DFS", "breadth-first", "depth-first", "graph", "traversal", "queue", "stack"]
        },
        {
            "question": "Explain hash tables and how they achieve O(1) average time complexity. What is collision handling?",
            "keywords": ["hash table", "hash function", "collision", "O(1)", "bucket", "chaining", "open addressing"]
        }
    ],
    "Java": [
        {
            "question": "What is the difference between abstract classes and interfaces in Java? When would you use each?",
            "keywords": ["abstract class", "interface", "inheritance", "multiple", "implementation", "contract"]
        },
        {
            "question": "Explain the concept of polymorphism in Java. Provide examples of compile-time and runtime polymorphism.",
            "keywords": ["polymorphism", "overloading", "overriding", "compile-time", "runtime", "method"]
        },
        {
            "question": "What is the difference between checked and unchecked exceptions in Java? How do you handle them?",
            "keywords": ["checked exception", "unchecked exception", "try-catch", "throws", "error", "runtime"]
        },
        {
            "question": "Explain the Java memory model. What are the heap and stack? How does garbage collection work?",
            "keywords": ["heap", "stack", "memory", "garbage collection", "JVM", "allocation", "reference"]
        },
        {
            "question": "What are Java generics and why are they used? Explain type erasure and its implications.",
            "keywords": ["generics", "type safety", "type erasure", "wildcard", "parameterized", "compile-time"]
        }
    ]
}


def get_questions_for_topic(topic: str) -> List[Dict]:
    """
    Get all questions for a given topic.
    Returns a list of question dictionaries.
    """
    topic = topic.capitalize()
    
    if topic not in QUESTION_BANK:
        raise ValueError(f"Topic '{topic}' not supported. Available: {list(QUESTION_BANK.keys())}")
    
    return QUESTION_BANK[topic].copy()


def get_available_topics() -> List[str]:
    """Get list of available interview topics."""
    return list(QUESTION_BANK.keys())

