from firebase_db import db
from datetime import datetime


def log_login(user_id, email, display_name):
    """Log user login event"""

    db.collection("activity_logs").add({
        "user_id": user_id,
        "email": email,
        "display_name": display_name,
        "action": "login",
        "timestamp": datetime.utcnow()
    })


def log_action(user_id, action, metadata=None):
    """Log any user activity (ask question, logout, etc.)"""

    db.collection("activity_logs").add({
        "user_id": user_id,
        "action": action,
        "metadata": metadata or {},
        "timestamp": datetime.utcnow()
    })