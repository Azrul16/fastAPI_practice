from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import smtplib
from email.message import EmailMessage
import random
import string
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import redis

# Load environment variables
load_dotenv()

# Initialize FastAPI
app = FastAPI()

# Setup templates and static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Redis for OTP storage (in-memory for development)
redis_client = redis.Redis(host='localhost', port=6379, db=0)

# Email configuration
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

def generate_otp(length=6):
    """Generate a 6-digit numeric OTP"""
    return ''.join(random.choices(string.digits, k=length))

def send_email_otp(email: str, otp: str):
    """Send OTP via email"""
    try:
        msg = EmailMessage()
        msg.set_content(f"Your verification code is: {otp}\n\nThis code expires in 5 minutes.")
        msg["Subject"] = "Your One-Time Password (OTP)"
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = email
        
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"Email sending failed: {e}")
        return False

@app.post("/api/send-otp/")
async def send_otp(request: Request):
    data = await request.json()
    email = data.get("email")
    
    if not email:
        raise HTTPException(status_code=400, detail="Email is required")
    
    otp = generate_otp()
    expires_at = datetime.now() + timedelta(minutes=5)
    
    # Store OTP in Redis
    redis_client.setex(
        f"otp:{email}",
        timedelta(minutes=5).total_seconds(),
        f"{otp}:{expires_at.timestamp()}"
    )
    
    # Send email
    if send_email_otp(email, otp):
        return {"status": "success", "message": "OTP sent to email"}
    else:
        raise HTTPException(status_code=500, detail="Failed to send OTP email")

@app.post("/api/verify-otp/")
async def verify_otp(request: Request):
    data = await request.json()
    email = data.get("email")
    otp = data.get("otp")
    
    if not email or not otp:
        raise HTTPException(status_code=400, detail="Email and OTP are required")
    
    stored_data = redis_client.get(f"otp:{email}")
    
    if not stored_data:
        raise HTTPException(status_code=404, detail="OTP expired or not found")
    
    stored_otp, expiry_time = stored_data.decode().split(":")
    expiry_time = datetime.fromtimestamp(float(expiry_time))
    
    if datetime.now() > expiry_time:
        redis_client.delete(f"otp:{email}")
        raise HTTPException(status_code=400, detail="OTP has expired")
    
    if stored_otp != otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")
    
    # OTP is valid
    redis_client.delete(f"otp:{email}")
    return {"status": "success", "message": "OTP verified successfully"}

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)