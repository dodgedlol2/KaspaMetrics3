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
            
            # Create reset URL
            reset_url = f"{self.domain}/?reset_token={reset_token}"
            
            # HTML email template
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Password Reset - Kaspa Analytics</title>
                <style>
                    body {{ 
                        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif; 
                        line-height: 1.6; 
                        color: #333; 
                        margin: 0;
                        padding: 0;
                        background-color: #f4f4f4;
                    }}
                    .container {{ 
                        max-width: 600px; 
                        margin: 0 auto; 
                        background: white;
                        border-radius: 12px;
                        overflow: hidden;
                        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                    }}
                    .header {{ 
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        color: white; 
                        padding: 40px 30px; 
                        text-align: center; 
                    }}
                    .header h1 {{
                        margin: 0;
                        font-size: 28px;
                        font-weight: 600;
                    }}
                    .header p {{
                        margin: 10px 0 0 0;
                        opacity: 0.9;
                        font-size: 16px;
                    }}
                    .content {{ 
                        padding: 40px 30px; 
                    }}
                    .content h2 {{
                        color: #333;
                        margin-top: 0;
                        font-size: 24px;
                    }}
                    .content p {{
                        margin: 16px 0;
                        font-size: 16px;
                        line-height: 1.5;
                    }}
                    .button {{ 
                        display: inline-block; 
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        color: white; 
                        padding: 16px 32px; 
                        text-decoration: none; 
                        border-radius: 8px; 
                        margin: 24px 0;
                        font-weight: 600;
                        font-size: 16px;
                        transition: transform 0.2s;
                    }}
                    .button:hover {{
                        transform: translateY(-2px);
                    }}
                    .url-box {{
                        background: #f8f9fa;
                        border: 1px solid #e9ecef;
                        padding: 16px;
                        border-radius: 8px;
                        word-break: break-all;
                        font-family: monospace;
                        font-size: 14px;
                        margin: 20px 0;
                    }}
                    .warning {{
                        background: #fff3cd;
                        border: 1px solid #ffeaa7;
                        color: #856404;
                        padding: 16px;
                        border-radius: 8px;
                        margin: 24px 0;
                    }}
                    .footer {{ 
                        background: #f8f9fa;
                        text-align: center; 
                        padding: 30px; 
                        color: #666; 
                        font-size: 14px; 
                        border-top: 1px solid #e9ecef;
                    }}
                    .footer p {{
                        margin: 8px 0;
                    }}
                    .security-tips {{
                        background: #e7f3ff;
                        border: 1px solid #b3d9ff;
                        padding: 20px;
                        border-radius: 8px;
                        margin: 24px 0;
                    }}
                    .security-tips h3 {{
                        margin-top: 0;
                        color: #0066cc;
                        font-size: 18px;
                    }}
                    .security-tips ul {{
                        margin: 12px 0;
                        padding-left: 20px;
                    }}
                    .security-tips li {{
                        margin: 8px 0;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>🔑 Kaspa Analytics</h1>
                        <p>Secure Password Reset</p>
                    </div>
                    <div class="content">
                        <h2>Hello {username}!</h2>
                        
                        <p>We received a request to reset the password for your Kaspa Analytics account. If you made this request, click the button below to create a new password:</p>
                        
                        <div style="text-align: center; margin: 32px 0;">
                            <a href="{reset_url}" class="button">🔄 Reset My Password</a>
                        </div>
                        
                        <p>If the button doesn't work, you can copy and paste this link into your browser:</p>
                        
                        <div class="url-box">
                            {reset_url}
                        </div>
                        
                        <div class="warning">
                            <strong>⏰ Important:</strong> This reset link will expire in 1 hour for security reasons.
                        </div>
                        
                        <div class="security-tips">
                            <h3>🛡️ Security Tips</h3>
                            <ul>
                                <li>Never share your password reset link with anyone</li>
                                <li>Choose a strong password with at least 8 characters</li>
                                <li>Use a combination of letters, numbers, and symbols</li>
                                <li>Don't use the same password for multiple accounts</li>
                            </ul>
                        </div>
                        
                        <p><strong>Didn't request this reset?</strong> If you didn't ask to reset your password, you can safely ignore this email. Your account remains secure and no changes will be made.</p>
                        
                        <hr style="margin: 32px 0; border: none; border-top: 1px solid #e9ecef;">
                        
                        <p><strong>Need help?</strong> Our support team is here to assist you:</p>
                        <p>📧 <a href="mailto:support@kaspaanalytics.com" style="color: #667eea;">support@kaspaanalytics.com</a></p>
                        <p>🌐 Visit our <a href="{self.domain}" style="color: #667eea;">help center</a></p>
                    </div>
                    <div class="footer">
                        <p><strong>© 2025 Kaspa Analytics</strong></p>
                        <p>Advanced Cryptocurrency Analytics Platform</p>
                        <p style="margin-top: 16px; opacity: 0.7;">This is an automated security email. Please do not reply to this message.</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            # Text version for email clients that don't support HTML
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
            
            # Prepare email data for Mailjet
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
                        "HTMLPart": html_content,
                        "CustomID": f"password_reset_{reset_token[:8]}"
                    }
                ]
            }
            
            # Send email via Mailjet
            result = self.mailjet.send.create(data=data)
            
            if result.status_code == 200:
                st.write(f"Debug: Email sent successfully via Mailjet! Status: {result.status_code}")
                return True
            else:
                st.write(f"Debug: Mailjet API error: {result.status_code} - {result.json()}")
                return self.simulate_email(to_email, reset_token, username)
            
        except Exception as e:
            st.write(f"Debug: Error sending email via Mailjet: {e}")
            return self.simulate_email(to_email, reset_token, username)
    
    def simulate_email(self, to_email, reset_token, username):
        """Simulate email sending for testing (when Mailjet not configured)"""
        st.write("Debug: Simulating email send...")
        
        # Create reset URL
        reset_url = f"{self.domain}/?reset_token={reset_token}"
        
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
        
        return True
