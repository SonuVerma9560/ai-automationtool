import pandas as pd
from groq import Groq
import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

# Load env
load_dotenv()

# Keys from .env
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
EMAIL = os.getenv("EMAIL")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# Groq client


api_key = os.getenv("GROQ_API_KEY")

def load_file(uploaded_file):
    if uploaded_file.name.endswith(".csv"):
        return pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith(".xlsx"):
        return pd.read_excel(uploaded_file)
    elif uploaded_file.name.endswith(".txt"):
        return uploaded_file.read().decode("utf-8")
    return None


def generate_summary(data):
    if isinstance(data, pd.DataFrame):
        text = data.to_string()
    else:
        text = data

    prompt = f"""
    Analyze this business data and provide:
    - Summary
    - Insights
    - Recommendations

    Data:
    {text}
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


def send_email(receiver_email, subject, body):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL
    msg["To"] = receiver_email

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL, EMAIL_PASSWORD)
        server.sendmail(EMAIL, receiver_email, msg.as_string())
        server.quit()
        return "✅ Email sent successfully!"
    except Exception as e:
        return f"❌ Error: {str(e)}"