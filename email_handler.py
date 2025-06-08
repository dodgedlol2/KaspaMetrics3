import streamlit as st
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os

class EmailHandler:
    def __init__(self):
        try:
            self.api_key = st.secrets["default"]["SENDGRID_API_KEY"]
            self.from_email = st.secrets["default"]["RESET_EMAIL_FROM"]
            self.subject = st.secrets["default"]["RESET_EMAIL_SUBJECT"]
            self.domain = st.secrets["default"]["DOMAIN"]
            self.sg = SendGridAPIClient(api_key=self.api_key)
            st.write("Debug: Email handler initialized successfully!")
        except Exception as e:
            st.write(f"Debug: Error initializing email handler: {e}")
            self.sg = None
    
    def send_password_reset_email(self, to_email, reset_token, username):
        """Send password reset email with reset link"""
        try:
            if not self.sg:
                st.write("Debug: SendGrid not configured, simulating email...")
                return self.simulate_email(to_email, reset_token, username)
            
            # Create reset URL
            reset_url = f"{self.domain}/?reset_token={reset_token}"
            
            # HTML email template
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                    .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                    .button {{ display: inline-block; background: #667eea; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
                    .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 12px; }}
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
                        
                        <a href="{reset_url}" class="button">🔑 Reset My Password</a>
                        
                        <p>Or copy and paste this link into your browser:</p>
                        <p style="background: #eee; padding: 10px; border-radius: 5px; word-break: break-all;">
                            {reset_url}
                        </p>
                        
                        <p><strong>⏰ This link will expire in 1 hour for security reasons.</strong></p>
                        
                        <p>If you didn't request this password reset, please ignore this email. Your password will remain unchanged.</p>
                        
                        <hr style="margin: 30px 0;">
                        
                        <p>Need help? Contact our support team:</p>
                        <p>📧 support@kaspaanalytics.com</p>
                    </div>
                    <div class="footer">
                        <p>© 2025 Kaspa Analytics. All rights reserved.</p>
                        <p>This is an automated message, please do not reply to this email.</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            # Create email message
            message = Mail(
                from_email=self.from_email,
                to_emails=to_email,
                subject=self.subject,
                html_content=html_content
            )
            
            # Send email
            response = self.sg.send(message)
            st.write(f"Debug: Email sent successfully! Status: {response.status_code}")
            return True
            
        except Exception as e:
            st.write(f"Debug: Error sending email: {e}")
            return self.simulate_email(to_email, reset_token, username)
    
    def simulate_email(self, to_email, reset_token, username):
        """Simulate email sending for testing (when SendGrid not configured)"""
        st.write("Debug: Simulating email send...")
        
        # Create reset URL
        reset_url = f"{self.domain}/?reset_token={reset_token}"
        
        st.info(f"""
        📧 **Password Reset Email Simulated**
        
        **To:** {to_email}  
        **Subject:** Kaspa Analytics - Password Reset
        
        **Content:**
        Hello {username},
        
        We received a request to reset your password.
        
        **Reset Link:** {reset_url}
        
        This link expires in 1 hour.
        
        *Note: This is a simulated email for testing. In production, this would be sent via SendGrid.*
        """)
        
        return True
