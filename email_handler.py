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
                        background: linear-gradient(135deg, #28a745 0%, #20c997 100%); 
                        color: white; 
                        padding: 40px 30px; 
                        text-align: center; 
                    }}
                    .content {{ 
                        padding: 40px 30px; 
                    }}
                    .button {{ 
                        display: inline-block; 
                        background: #667eea;
                        color: white; 
                        padding: 15px 30px; 
                        text-decoration: none; 
                        border-radius: 8px; 
                        margin: 20px 0;
                        font-weight: bold;
                    }}
                    .feature-box {{
                        background: #f8f9fa;
                        border-left: 4px solid #28a745;
                        padding: 20px;
                        margin: 20px 0;
                        border-radius: 5px;
                    }}
                    .footer {{ 
                        background: #f8f9fa;
                        text-align: center; 
                        padding: 30px; 
                        color: #666; 
                        font-size: 14px; 
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>🎉 Welcome to Kaspa Analytics!</h1>
                        <p>Your gateway to advanced Kaspa blockchain insights</p>
                    </div>
                    <div class="content">
                        <p>Hello <strong>{username}</strong>,</p>
                        
                        <p>Welcome to Kaspa Analytics! We're excited to have you join our community of crypto enthusiasts and analysts.</p>
                        
                        <div class="feature-box">
                            <h3>🚀 What you can do now:</h3>
                            <ul>
                                <li><strong>⛏️ Mining Analytics</strong> - Track network hashrate and difficulty</li>
                                <li><strong>💰 Market Data</strong> - Real-time price, volume, and market cap</li>
                                <li><strong>📱 Social Insights</strong> - Community sentiment and trends</li>
                                <li><strong>📊 Interactive Charts</strong> - Beautiful data visualizations</li>
                            </ul>
                        </div>
                        
                        <div style="text-align: center; margin: 30px 0;">
                            <a href="{self.domain}" class="button">🔥 Start Exploring Analytics</a>
                        </div>
                        
                        <p>Thank you for choosing Kaspa Analytics!</p>
                        
                        <p>Best regards,<br>
                        <strong>The Kaspa Analytics Team</strong></p>
                    </div>
                    <div class="footer">
                        <p><strong>© 2025 Kaspa Analytics</strong></p>
                        <p>Advanced Cryptocurrency Analytics Platform</p>
                    </div>
                </div>
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
                        background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%); 
                        color: #333; 
                        padding: 40px 30px; 
                        text-align: center; 
                    }}
                    .content {{ 
                        padding: 40px 30px; 
                    }}
                    .button {{ 
                        display: inline-block; 
                        background: #667eea;
                        color: white; 
                        padding: 15px 30px; 
                        text-decoration: none; 
                        border-radius: 8px; 
                        margin: 20px 0;
                        font-weight: bold;
                    }}
                    .feature-box {{
                        background: #fff3cd;
                        border: 1px solid #ffeaa7;
                        padding: 20px;
                        margin: 20px 0;
                        border-radius: 8px;
                        border-left: 4px solid #ffd700;
                    }}
                    .footer {{ 
                        background: #f8f9fa;
                        text-align: center; 
                        padding: 30px; 
                        color: #666; 
                        font-size: 14px; 
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>👑 Welcome to Premium!</h1>
                        <h2>Kaspa Analytics Premium Activated</h2>
                        <p style="font-size: 18px; margin: 0;">Thank you for upgrading, {username}!</p>
                    </div>
                    <div class="content">
                        <p>Hello <strong>{username}</strong>,</p>
                        
                        <p>🎉 <strong>Congratulations!</strong> Your {plan_type} subscription has been successfully activated.</p>
                        
                        <div class="feature-box">
                            <h3>🚀 Your Premium Features Are Now Active:</h3>
                            <ul>
                                <li><strong>🤖 AI-Powered Insights</strong> - Machine learning market predictions</li>
                                <li><strong>🐋 Whale Tracking</strong> - Monitor large holder transactions</li>
                                <li><strong>🔔 Custom Alerts</strong> - Get notified of important events</li>
                                <li><strong>📈 Advanced Charts</strong> - Professional trading tools</li>
                                <li><strong>📊 Data Export</strong> - Download data in CSV/PDF format</li>
                                <li><strong>💎 Priority Support</strong> - Get help when you need it most</li>
                            </ul>
                        </div>
                        
                        <div style="text-align: center; margin: 30px 0;">
                            <a href="{self.domain}" class="button">🔬 Explore Premium Analytics</a>
                        </div>
                        
                        <p>Thank you for choosing Kaspa Analytics Premium!</p>
                        
                        <p>Best regards,<br>
                        <strong>The Kaspa Analytics Team</strong></p>
                    </div>
                    <div class="footer">
                        <p><strong>© 2025 Kaspa Analytics</strong></p>
                        <p>Advanced Cryptocurrency Analytics Platform</p>
                    </div>
                </div>
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
                        background: linear-gradient(135deg, #28a745 0%, #20c997 100%); 
                        color: white; 
                        padding: 40px 30px; 
                        text-align: center; 
                    }}
                    .content {{ 
                        padding: 40px 30px; 
                    }}
                    .button {{ 
                        display: inline-block; 
                        background: #667eea;
                        color: white; 
                        padding: 15px 30px; 
                        text-decoration: none; 
                        border-radius: 8px; 
                        margin: 20px 0;
                        font-weight: bold;
                    }}
                    .success-box {{
                        background: #d4edda;
                        border: 1px solid #c3e6cb;
                        color: #155724;
                        padding: 20px;
                        margin: 20px 0;
                        border-radius: 8px;
                        border-left: 4px solid #28a745;
                    }}
                    .info-box {{
                        background: #e9ecef;
                        border: 1px solid #ced4da;
                        padding: 20px;
                        margin: 20px 0;
                        border-radius: 8px;
                    }}
                    .footer {{ 
                        background: #f8f9fa;
                        text-align: center; 
                        padding: 30px; 
                        color: #666; 
                        font-size: 14px; 
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>🎉 Subscription Renewed!</h1>
                        <h2>Kaspa Analytics Premium</h2>
                        <p style="font-size: 18px; margin: 0;">Your premium access continues seamlessly</p>
                    </div>
                    <div class="content">
                        <p>Hello <strong>{username}</strong>,</p>
                        
                        <div class="success-box">
                            <h3>✅ Your {plan_type} subscription has been automatically renewed!</h3>
                            <p><strong>🗓️ Your premium access is now extended until: {new_expiry_date}</strong></p>
                        </div>
                        
                        <p>Great news! We've successfully processed your subscription renewal. You can continue enjoying all premium features without any interruption.</p>
                        
                        <div class="info-box">
                            <h3>📊 Your Premium Features Continue:</h3>
                            <ul>
                                <li><strong>🤖 AI-Powered Insights</strong> - Advanced market predictions</li>
                                <li><strong>🐋 Whale Tracking</strong> - Monitor large transactions</li>
                                <li><strong>🔔 Custom Alerts</strong> - Real-time notifications</li>
                                <li><strong>📈 Advanced Charts</strong> - Professional trading tools</li>
                                <li><strong>📊 Data Export</strong> - Download your analytics</li>
                                <li><strong>💎 Priority Support</strong> - Get help when needed</li>
                            </ul>
                        </div>
                        
                        <div style="text-align: center; margin: 30px 0;">
                            <a href="{self.domain}" class="button">🚀 Continue Using Premium</a>
                        </div>
                        
                        <h3>💳 Billing Information:</h3>
                        <ul>
                            <li><strong>Plan:</strong> {plan_type}</li>
                            <li><strong>Status:</strong> Active & Auto-Renewing</li>
                            <li><strong>Next Renewal:</strong> {new_expiry_date}</li>
                            <li><strong>Billing:</strong> Automatic</li>
                        </ul>
                        
                        <hr style="margin: 30px 0;">
                        
                        <h3>🔧 Need to Make Changes?</h3>
                        <p>You can manage your subscription, update payment methods, or cancel anytime from your account dashboard.</p>
                        
                        <div style="text-align: center; margin: 20px 0;">
                            <a href="{self.domain}/A_👤_Account" class="button" style="background: #6c757d;">⚙️ Manage Subscription</a>
                        </div>
                        
                        <p>Thank you for being a valued Kaspa Analytics Premium member!</p>
                        
                        <p>Best regards,<br>
                        <strong>The Kaspa Analytics Team</strong></p>
                    </div>
                    <div class="footer">
                        <p><strong>© 2025 Kaspa Analytics</strong></p>
                        <p>Advanced Cryptocurrency Analytics Platform</p>
                        <p style="margin-top: 16px; opacity: 0.7;">You received this email because your subscription was automatically renewed.</p>
                    </div>
                </div>
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
