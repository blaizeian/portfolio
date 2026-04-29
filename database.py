import os
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# --- SMART PATH LOGIC ---
# 1. Get the folder where THIS file (database.py) lives
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# 2. Create the full path to the database file in that same folder
db_path = os.path.join(BASE_DIR, "portfolio.db")
# 3. Format it for SQLAlchemy (3 slashes for SQLite)
DATABASE_URL = f"sqlite:///{db_path}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class MessageEntry(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(100))
    message = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

def init_db():
    Base.metadata.create_all(bind=engine)
    print(f"🚀 Database initialized at: {db_path}")

def save_message(name, email, message):
    db = SessionLocal()
    try:
        new_entry = MessageEntry(name=name, email=email, message=message)
        db.add(new_entry)
        db.commit()
        print(f"✅ Data saved to: {db_path}")
    except Exception as e:
        print(f"❌ Database error: {e}")
    finally:
        db.close()