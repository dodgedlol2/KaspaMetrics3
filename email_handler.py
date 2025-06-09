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
                return self.simulate_email(to_email, reset_token, username, "password_reset")
            
            reset_url = f"{self.domain}/C_🔄_Reset_Password?reset_token={reset_token}"
            
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <title>Password Reset - Kaspa Analytics</title>
            </head>
            <body>
                <h1>Password Reset Request</h1>
                <p>Hello {username},</p>
                <p>Click the link below to reset your password:</p>
                <a href="{reset_url}">Reset My Password</a>
                <p>This link will expire in 1 hour.</p>
            </body>
            </html>
            """
            
            text_content = f"""
            Hello {username},
            
            Click this link to reset your password: {reset_url}
            
            This link will expire in 1 hour.
            
            © 2025 Kaspa Analytics
            """
            
            return self._send_email(to_email, username, "Reset Your Kaspa Analytics Password", html_content, text_content)
            
        except Exception as e:
            st.write(f"Debug: Error sending password reset email: {e}")
            return self.simulate_email(to_email, reset_token, username, "password_reset")
    
    def send_welcome_email(self, to_email, username):
        """Send welcome email to new users"""
        try:
            if not self.mailjet:
                st.write("Debug: Mailjet not configured, simulating welcome email...")
                return self.simulate_email(to_email, None, username, "welcome")
            
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <title>Welcome to Kaspa Analytics</title>
            </head>
            <body>
                <h1>Welcome to Kaspa Analytics!</h1>
                <p>Hello {username},</p>
                <p>Welcome to Kaspa Analytics! We're excited to have you join our community.</p>
                <p><a href="{self.domain}">Start Exploring Analytics</a></p>
            </body>
            </html>
            """
            
            text_content = f"""
            Welcome to Kaspa Analytics!
            
            Hello {username},
            
            Welcome to Kaspa Analytics! We're excited to have you join our community.
            
            Start exploring: {self.domain}
            
            © 2025 Kaspa Analytics
            """
            
            return self._send_email(to_email, username, "Welcome to Kaspa Analytics!", html_content, text_content)
            
        except Exception as e:
            st.write(f"Debug: Error sending welcome email: {e}")
            return self.simulate_email(to_email, None, username, "welcome")
    
    def send_cancellation_email(self, to_email, username):
        """Send subscription cancellation confirmation email"""
        try:
            if not self.mailjet:
                st.write("Debug: Mailjet not configured, simulating cancellation email...")
                return self.simulate_email(to_email, None, username, "cancellation")
            
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <title>Subscription Cancelled - Kaspa Analytics</title>
            </head>
            <body>
                <h1>Subscription Cancelled</h1>
                <p>Hello {username},</p>
                <p>We've successfully processed your premium subscription cancellation request.</p>
                <p>You'll keep premium access until your current billing period ends.</p>
                <p><a href="{self.domain}">Continue Using Free Features</a></p>
            </body>
            </html>
            """
            
            text_content = f"""
            Subscription Cancelled - Kaspa Analytics
            
            Hello {username},
            
            We've successfully processed your premium subscription cancellation request.
            You'll keep premium access until your current billing period ends.
            
            Continue using: {self.domain}
            
            © 2025 Kaspa Analytics
            """
            
            return self._send_email(to_email, username, "Subscription Cancelled - Kaspa Analytics", html_content, text_content)
            
        except Exception as e:
            st.write(f"Debug: Error sending cancellation email: {e}")
            return self.simulate_email(to_email, None, username, "cancellation")
    
    def send_premium_subscription_email(self, to_email, username, plan_type="Premium"):
        """Send premium subscription confirmation email"""
        try:
            if not self.mailjet:
                st.write("Debug: Mailjet not configured, simulating premium subscription email...")
                return self.simulate_email(to_email, None, username, "premium_subscription")
            
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <title>Welcome to Premium - Kaspa Analytics</title>
            </head>
            <body>
                <h1>Welcome to Premium!</h1>
                <p>Hello {username},</p>
                <p>Congratulations! Your {plan_type} subscription has been successfully activated.</p>
                <p>All premium features are now available to you.</p>
                <p><a href="{self.domain}">Explore Premium Analytics</a></p>
            </body>
            </html>
            """
            
            text_content = f"""
            Welcome to Premium - Kaspa Analytics!
            
            Hello {username},
            
            Congratulations! Your {plan_type} subscription has been successfully activated.
            All premium features are now available to you.
            
            Start exploring: {self.domain}
            
            © 2025 Kaspa Analytics
            """
            
            return self._send_email(to_email, username, "Welcome to Premium - Kaspa Analytics!", html_content, text_content)
            
        except Exception as e:
            st.write(f"Debug: Error sending premium subscription email: {e}")
            return self.simulate_email(to_email, None, username, "premium_subscription")

    def send_renewal_notification_email(self, to_email, username, plan_type, new_expiry_date):
        """Send automatic renewal notification email"""
        try:
            if not self.mailjet:
                st.write("Debug: Mailjet not configured, simulating renewal notification email...")
                return self.simulate_email(to_email, None, username, "renewal_notification")
            
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <title>Subscription Renewed - Kaspa Analytics</title>
            </head>
            <body>
                <h1>Subscription Renewed!</h1>
                <p>Hello {username},</p>
                <p>Great news! Your {plan_type} subscription has been automatically renewed.</p>
                <p>Your premium access is now extended until: {new_expiry_date}</p>
                <p>You can continue enjoying all premium features without any interruption.</p>
                <p><a href="{self.domain}">Continue Using Premium</a></p>
                <p><a href="{self.domain}/A_👤_Account">Manage Subscription</a></p>
            </body>
            </html>
            """
            
            text_content = f"""
            Subscription Renewed - Kaspa Analytics!
            
            Hello {username},
            
            Great news! Your {plan_type} subscription has been automatically renewed.
            Your premium access is now extended until: {new_expiry_date}
            
            Continue using premium: {self.domain}
            Manage subscription: {self.domain}/A_👤_Account
            
            © 2025 Kaspa Analytics
            """
            
            return self._send_email(to_email, username, "Subscription Renewed - Kaspa Analytics", html_content, text_content)
            
        except Exception as e:
            st.write(f"Debug: Error sending renewal notification email: {e}")
            return self.simulate_email(to_email, None, username, "renewal_notification")
    
    def _send_email(self, to_email, username, subject, html_content, text_content):
        """Helper method to send email via Mailjet"""
        try:
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
                        "Subject": subject,
                        "TextPart": text_content,
                        "HTMLPart": html_content
                    }
                ]
            }
            
            result = self.mailjet.send.create(data=data)
            
            if result.status_code == 200:
                st.write(f"Debug: Email sent successfully via Mailjet! Status: {result.status_code}")
                return True
            else:
                st.write(f"Debug: Mailjet API error: {result.status_code}")
                return False
            
        except Exception as e:
            st.write(f"Debug: Error in _send_email: {e}")
            return False
    
    def simulate_email(self, to_email, reset_token, username, email_type):
        """Simulate email sending for testing"""
        st.write(f"Debug: Simulating {email_type} email send...")
        
        if email_type == "password_reset":
            reset_url = f"{self.domain}/C_🔄_Reset_Password?reset_token={reset_token}"
            st.info(f"""
            📧 **Password Reset Email Simulated**
            
            **To:** {to_email}  
            **Subject:** Reset Your Kaspa Analytics Password
            
            Hello {username}, we received a request to reset your password.
            **Reset Link:** {reset_url}
            """)
            
        elif email_type == "welcome":
            st.info(f"""
            📧 **Welcome Email Simulated**
            
            **To:** {to_email}  
            **Subject:** Welcome to Kaspa Analytics!
            
            Hello {username}, welcome to Kaspa Analytics! 
            Start exploring our features and consider upgrading to premium.
            """)
            
        elif email_type == "premium_subscription":
            st.success(f"""
            📧 **Premium Subscription Email Simulated**
            
            **To:** {to_email}  
            **Subject:** Welcome to Premium - Kaspa Analytics!
            
            Hello {username}, congratulations! Your premium subscription is now active.
            All premium features are now available to you.
            """)
            
        elif email_type == "cancellation":
            st.info(f"""
            📧 **Cancellation Email Simulated**
            
            **To:** {to_email}  
            **Subject:** Subscription Cancelled - Kaspa Analytics
            
            Hello {username}, your premium subscription has been cancelled.
            You'll keep access until your billing period ends.
            """)
        
        elif email_type == "renewal_notification":
            st.success(f"""
            📧 **Renewal Notification Email Simulated**
            
            **To:** {to_email}  
            **Subject:** Subscription Renewed - Kaspa Analytics
            
            Hello {username}, great news! Your subscription has been automatically renewed.
            Your premium access continues without interruption.
            """)
        
        return True
