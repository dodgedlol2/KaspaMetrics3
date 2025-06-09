import streamlit as st
from mailjet_rest import Client
import os

class EmailHandler:
    def __init__(self):
        try:
            self.api_key = st.secrets["default"]["MAILJET_API_KEY"]
            self.api_secret = st.secrets["default"]["MAILJET_API_SECRET"]
            self.from_email = st.secrets["default"]["RESET_EMAIL_FROM"]
            self.from_name = st.secrets["default"].get("RESET_EMAIL_FROM_NAME", "Kaspa Analytics")
            self.domain = st.secrets["default"]["DOMAIN"]
            self.mailjet = Client(auth=(self.api_key, self.api_secret), version='v3.1')
            st.write("Debug: Mailjet email handler initialized successfully!")
        except Exception as e:
            st.write(f"Debug: Error initializing Mailjet handler: {e}")
            self.mailjet = None
    
    def send_password_reset_email(self, to_email, reset_token, username):
        """Send password reset email with reset link via Mailjet"""
        try:
            if not self.mailjet:
                st.write("Debug: Mailjet not configured, simulating email...")
                return self.simulate_email(to_email, reset_token, username)
            
            # Create reset URL - point to dedicated reset page
            reset_url = f"{self.domain}/Reset_Password?reset_token={reset_token}"
            
            # HTML email template
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <title>Password Reset - Kaspa Analytics</title>
                <style>
                    body {{ 
                        font-family: Arial, sans-serif; 
                        line-height: 1.6; 
                        color: #333; 
                        margin: 0;
                        padding: 20px;
                        background-color: #f4f4f4;
                    }}
                    .container {{ 
                        max-width: 600px; 
                        margin: 0 auto; 
                        background: white;
                        border-radius: 10px;
                        overflow: hidden;
                        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                    }}
                    .header {{ 
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        color: white; 
                        padding: 30px; 
                        text-align: center; 
                    }}
                    .content {{ 
                        padding: 30px; 
                    }}
                    .button {{ 
                        display: inline-block; 
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        color: white; 
                        padding: 15px 30px; 
                        text-decoration: none; 
                        border-radius: 8px; 
                        margin: 20px 0;
                        font-weight: bold;
                    }}
                    .footer {{ 
                        background: #f8f9fa;
                        text-align: center; 
                        padding: 20px; 
                        color: #666; 
                        font-size: 14px; 
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>🔑 Kaspa Analytics</h1>
                        <h2>Password Reset Request</h2>
                    </div>
                    <div class="content">
                        <p>Hello <strong>{username}</strong>,</p>
                        
                        <p>We received a request to reset your password for your Kaspa Analytics account.</p>
                        
                        <p>Click the button below to reset your password:</p>
                        
                        <div style="text-align: center;">
                            <a href="{reset_url}" class="button">🔄 Reset My Password</a>
                        </div>
                        
                        <p>Or copy and paste this link into your browser:</p>
                        <p style="background: #f0f0f0; padding: 10px; border-radius: 5px; word-break: break-all; font-family: monospace;">
                            {reset_url}
                        </p>
                        
                        <p><strong>⏰ This link will expire in 1 hour for security reasons.</strong></p>
                        
                        <p>If you didn't request this password reset, please ignore this email.</p>
                        
                        <hr style="margin: 30px 0;">
                        
                        <p>Need help? Contact support@kaspaanalytics.com</p>
                    </div>
                    <div class="footer">
                        <p>© 2025 Kaspa Analytics. All rights reserved.</p>
                        <p>This is an automated message, please do not reply to this email.</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            # Text version
            text_content = f"""
            Kaspa Analytics - Password Reset
            
            Hello {username},
            
            We received a request to reset your password for your Kaspa Analytics account.
            
            To reset your password, visit this link:
            {reset_url}
            
            This link will expire in 1 hour for security reasons.
            
            If you didn't request this password reset, please ignore this email.
            
            Need help? Contact support@kaspaanalytics.com
            
            © 2025 Kaspa Analytics
            """
            
            # Prepare email data for Mailjet - FIXED VERSION
            data = {
                'Messages': [
                    {
                        "From": {
                            "Email": self.from_email,
                            "Name": self.from_name
                        },
                        "To": [
                            {
                                "Email": to_email,
                                "Name": username
                            }
                        ],
                        "Subject": "🔑 Reset Your Kaspa Analytics Password",
                        "TextPart": text_content,
                        "HTMLPart": html_content
                    }
                ]
            }
            
            # Send email via Mailjet
            result = self.mailjet.send.create(data=data)
            
            if result.status_code == 200:
                st.write(f"Debug: Email sent successfully via Mailjet! Status: {result.status_code}")
                return True
            else:
                st.write(f"Debug: Mailjet API error: {result.status_code}")
                return self.simulate_email(to_email, reset_token, username)
            
        except Exception as e:
            st.write(f"Debug: Error sending email via Mailjet: {e}")
            return self.simulate_email(to_email, reset_token, username)
    
    def simulate_email(self, to_email, reset_token, username):
        """Simulate email sending for testing"""
        st.write("Debug: Simulating email send...")
        
        # Create reset URL - point to dedicated reset page
        reset_url = f"{self.domain}/Reset_Password?reset_token={reset_token}"
        
        st.info(f"""
        📧 **Password Reset Email Simulated**
        
        **To:** {to_email}  
        **Subject:** 🔑 Reset Your Kaspa Analytics Password
        
        **Message:**
        Hello {username},
        
        We received a request to reset your password.
        
        **🔄 Reset Link:** 
        {reset_url}
        
        ⏰ **This link expires in 1 hour.**
        
        If you didn't request this, please ignore this email.
        
        ---
        
        *Note: This is a simulated email for testing. In production, this would be sent via Mailjet.*
        
        **📋 Test Instructions:**
        1. Copy the reset link above
        2. Open it in a new tab 
        3. Set your new password
        4. Login with the new credentials
        """)
        
        # Add a clickable link for easier testing
        st.markdown(f"**[🔄 CLICK HERE TO RESET PASSWORD]({reset_url})**")
        
        return True
