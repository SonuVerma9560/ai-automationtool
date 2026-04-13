import pandas as pd
import os
from groq import Groq
import smtplib
from email.mime.text import MIMEText

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# 📊 READ FILE (CSV / TXT)
def read_file(uploaded_file):
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith(".txt"):
        df = pd.read_csv(uploaded_file, delimiter=",")
    else:
        return None

    return df


# 🤖 GENERATE SUMMARY (AI)
def generate_summary(data):
    prompt = f"""
    Analyze the following business data and provide insights:

    {data}

    Give:
    - Summary
    - Key insights
    - Recommendations
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


# 📧 GENERATE EMAIL CONTENT
def generate_email(summary):
    email_text = f"""
Subject: AI Generated Business Report

Dear Sir/Madam,

Please find below the AI-generated business insights:

{summary}

Best regards,
AI Automation Tool
"""
    return email_text


# 📨 SEND EMAIL
def send_email(receiver_email, email_body):
    sender_email = os.getenv("EMAIL")
    sender_password = os.getenv("EMAIL_PASSWORD")

    msg = MIMEText(email_body)
    msg["Subject"] = "AI Business Report"
    msg["From"] = sender_email
    msg["To"] = receiver_email

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(e)
        return False