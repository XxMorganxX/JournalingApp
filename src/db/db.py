from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    """
    User model - simplified for MVP with single user
    """
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    created_dt = db.Column(db.DateTime, nullable=False)
    
    journal_entries = db.relationship("JournalEntry", back_populates="user")

    def __init__(self, **kwargs):
        self.created_dt = datetime.now()
        self.name = kwargs.get("name")
        self.email = kwargs.get("email")
        self.password = kwargs.get("password")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "created_at": self.created_dt
        }
        
class JournalEntry(db.Model):
    """
    Journal Entry model
    Has a one-to-many relationship with users
    """
    __tablename__ = "journal_entries"
    __table_args__ = {'sqlite_autoincrement': True}
    
    
    entry_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    dt_created = db.Column(db.DateTime, nullable=False)
    recording_url = db.Column(db.String, nullable=False)
    
    # Add after analysis
    title = db.Column(db.String, nullable=True, default="N/A")
    summary = db.Column(db.String, nullable=True, default="N/A")
    transcription = db.Column(db.String, nullable=True, default="N/A")
    key_insights = db.Column(db.String, nullable=True, default="N/A")
    
    # Add relationship to user
    user = db.relationship("User", back_populates="journal_entries")
    
    def __init__(self, **kwargs):
        self.user_id = kwargs.get("user_id")
        self.entry_id = kwargs.get("entry_id")
        self.datetime_created = kwargs.get("datetime_created")
        self.title = kwargs.get("title", "N/A")
        self.summary = kwargs.get("summary", "N/A")
        self.transcription = kwargs.get("transcription", "N/A")
        self.key_insights = kwargs.get("key_insights", "N/A")

    def serialize(self):
        return {
            "entry_id": self.entry_id,
            "user_id": self.user_id,
            "title": self.title,
            "datetime_created": self.datetime_created,
            "transcription": self.transcription,
            "summary": self.summary,
            "key_insights": self.key_insights,
        }
    
    
    
    

    
            
        