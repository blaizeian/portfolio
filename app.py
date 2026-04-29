import os
import smtplib
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from email.mime.text import MIMEText
from database import init_db, save_message 
import resend # type: ignore
resend.api_key = os.getenv("RESEND_API_KEY")
MY_EMAIL = os.getenv("MY_EMAIL")
#resend.api_key = "re_FTBFD9g5_JiUexa7bZj9gn9pNpiFEZqua"

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
# Add this to your imports at the top

# Set your API Key


@app.post("/send-email")
async def send_contact_email(form: ContactForm):
    # 1. SAVE TO DATABASE
    try:
        save_message(form.name, form.email, form.message)
    except Exception as db_err:
        print(f"Database Error: {db_err}")

    # 2. SEND VIA RESEND API
    try:
        params = {
            "from": "onboarding@resend.dev",
            "to": MY_EMAIL,  # This now uses the secret from Render
            "subject": f"New Portfolio Message from {form.name}",
            "html": f"<p><strong>Name:</strong> {form.name}</p><p>{form.message}</p>"
        }
        resend.Emails.send(params)
        return {"status": "success", "message": "Email sent!"}
    except Exception as e:
        print(f"Resend Error: {e}")
        return {"status": "success", "message": "Saved to DB, but email failed."}
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)