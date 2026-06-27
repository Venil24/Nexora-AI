"""
backend/app/services/email_service.py
Email service using SMTP for password reset emails.
"""
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import current_app


RESET_EMAIL_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    body {{ font-family: Arial, sans-serif; background: #f9fafb; margin: 0; padding: 0; }}
    .container {{ max-width: 600px; margin: 40px auto; background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 20px rgba(0,0,0,0.1); }}
    .header {{ background: linear-gradient(135deg, #7C3AED, #4F46E5); padding: 40px 30px; text-align: center; }}
    .header h1 {{ color: white; margin: 0; font-size: 28px; }}
    .header p {{ color: #DDD6FE; margin: 8px 0 0; }}
    .body {{ padding: 40px 30px; }}
    .body p {{ color: #374151; line-height: 1.6; }}
    .button {{ display: inline-block; background: linear-gradient(135deg, #7C3AED, #4F46E5); color: white; padding: 14px 32px; border-radius: 8px; text-decoration: none; font-weight: bold; font-size: 16px; margin: 20px 0; }}
    .footer {{ background: #f9fafb; padding: 20px 30px; text-align: center; color: #9CA3AF; font-size: 12px; }}
    .divider {{ border: none; border-top: 1px solid #E5E7EB; margin: 20px 0; }}
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>🧠 Nexora AI</h1>
      <p>AI Resume Analyzer & Career Roadmap</p>
    </div>
    <div class="body">
      <p>Hi <strong>{name}</strong>,</p>
      <p>We received a request to reset the password for your Nexora AI account associated with this email address.</p>
      <p>Click the button below to reset your password. This link will expire in <strong>1 hour</strong>.</p>
      <div style="text-align: center;">
        <a href="{reset_url}" class="button">Reset My Password</a>
      </div>
      <hr class="divider">
      <p style="font-size: 13px; color: #6B7280;">
        If you didn't request a password reset, you can safely ignore this email. 
        Your password will not be changed.
      </p>
      <p style="font-size: 13px; color: #6B7280;">
        Or copy and paste this URL into your browser:<br>
        <a href="{reset_url}" style="color: #7C3AED;">{reset_url}</a>
      </p>
    </div>
    <div class="footer">
      <p>© 2024 Nexora AI. All rights reserved.</p>
      <p>This is an automated email. Please do not reply.</p>
    </div>
  </div>
</body>
</html>
"""


def send_password_reset_email(to_email: str, name: str, token: str):
    """Send password reset email with a token link."""
    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")
    reset_url = f"{frontend_url}/reset-password?token={token}"

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Reset Your Nexora AI Password"
    msg["From"] = current_app.config.get("MAIL_DEFAULT_SENDER", "Nexora AI <noreply@nexora.ai>")
    msg["To"] = to_email

    html_content = RESET_EMAIL_TEMPLATE.format(name=name, reset_url=reset_url)
    msg.attach(MIMEText(html_content, "html"))

    with smtplib.SMTP(
        current_app.config["MAIL_SERVER"],
        current_app.config["MAIL_PORT"]
    ) as server:
        if current_app.config.get("MAIL_USE_TLS"):
            server.starttls()
        if current_app.config.get("MAIL_USERNAME"):
            server.login(
                current_app.config["MAIL_USERNAME"],
                current_app.config["MAIL_PASSWORD"]
            )
        server.sendmail(msg["From"], [to_email], msg.as_string())
