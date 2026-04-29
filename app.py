import os
import smtplib
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from email.mime.text import MIMEText
from database import init_db, save_message 

# Load credentials
load_dotenv()

app = FastAPI()

# 1. PERMISSIONS (CORS) - Only need this once
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://blaizeian.github.io", "http://localhost:5500"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Database
init_db()

# 2. THE DATA MODEL
class ContactForm(BaseModel):
    name: str
    email: str
    message: str

# 3. THE SINGLE ENDPOINT
@app.post("/send-email")
async def send_contact_email(form: ContactForm):
    # A. SAVE TO DATABASE
    try:
        save_message(form.name, form.email, form.message)
    except Exception as db_err:
        print(f"Database Error: {db_err}")

    # B. PREPARE EMAIL
    sender_email = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASS")

    if not sender_email or not password:
        print("Error: EMAIL_USER or EMAIL_PASS not set in environment variables.")
        raise HTTPException(status_code=500, detail="Server missing credentials")

    msg = MIMEText(f"Name: {form.name}\nEmail: {form.email}\n\n{form.message}")
    msg['Subject'] = f"New Portfolio Contact from {form.name}"
    msg['From'] = sender_email
    msg['To'] = sender_email

    # C. SEND EMAIL
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, sender_email, msg.as_string())
        return {"status": "success", "message": "Message saved and email sent!"}
    except Exception as e:
        print(f"Email Error: {e}")
        # We still return success if the DB part worked, or 500 if everything failed
        raise HTTPException(status_code=500, detail="Failed to send email")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)