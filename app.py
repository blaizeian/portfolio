import os
import smtplib
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from email.mime.text import MIMEText
from database import init_db, save_message # <--- IMPORTING YOUR NEW FILE

# Load credentials
load_dotenv()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://blaizeian.github.io"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#@app.post("/send-email")
#async def send_email(data: dict):
    # your existing email code here
 #   return {"status": "success"}
@app.post("/send-email")
async def send_email(data: dict):
    try:
        # 1. This part does the actual work (saving to DB)
        # Make sure 'save_message' is imported from your database.py
        from database import save_message 
        
        save_message(
            data.get("name"), 
            data.get("email"), 
            data.get("message")
        )

        # 2. This part sends the 'Success' signal back to your website
        return {"status": "success", "message": "Message saved to database!"}

    except Exception as e:
        # If something breaks (like the DB connection), this tells you why
        print(f"Error: {e}")
        return {"status": "error", "message": str(e)}, 500

# Initialize Database
init_db()

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ContactForm(BaseModel):
    name: str
    email: str
    message: str

@app.post("/send-email")
async def send_contact_email(form: ContactForm):
    # 1. SAVE TO DATABASE (The new part)
    try:
        save_message(form.name, form.email, form.message)
    except Exception as db_err:
        print(f"Database Error: {db_err}")
        # We continue even if DB fails, so the email might still send

    # 2. PREPARE EMAIL
    sender_email = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASS")

    if not sender_email or not password:
        raise HTTPException(status_code=500, detail="Server missing credentials")

    msg = MIMEText(f"Name: {form.name}\nEmail: {form.email}\n\n{form.message}")
    msg['Subject'] = "Portfolio Contact"
    msg['From'] = sender_email
    msg['To'] = sender_email

    # 3. SEND EMAIL
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, sender_email, msg.as_string())
        return {"status": "success"}
    except Exception as e:
        print(f"\n!!! EMAIL ERROR !!!\n{e}\n")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)