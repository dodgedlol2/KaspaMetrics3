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
            
            # Create reset URL - point to dedicated reset page
            reset_url = f"{self.domain}/C_🔄_Reset_Password?reset_token={reset_token}"
            
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
            
            return self._send_email(to_email, username, "🔑 Reset Your Kaspa Analytics Password", html_content, text_content)
            
        except Exception as e:
            st.write(f"Debug: Error sending password reset email: {e}")
            return self.simulate_email(to_email, reset_token, username, "password_reset")
    
    def send_welcome_email(self, to_email, username):
        """Send welcome email to new users"""
        try:
            if not self.mailjet:
                st.write("Debug: Mailjet not configured, simulating welcome email...")
                return self.simulate_email(to_email, None, username, "welcome")
            
            # HTML welcome email template
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
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
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
                        
                        <div class="feature-box">
                            <h3>👑 Want More? Upgrade to Premium!</h3>
                            <ul>
                                <li><strong>🤖 AI-Powered Insights</strong> - Machine learning predictions</li>
                                <li><strong>🐋 Whale Tracking</strong> - Monitor large transactions</li>
                                <li><strong>🔔 Custom Alerts</strong> - Get notified of important events</li>
                                <li><strong>📈 Advanced Charts</strong> - Professional trading tools</li>
                                <li><strong>📧 Priority Support</strong> - Get help when you need it</li>
                            </ul>
                            <p><strong>Plans starting at just $9.99/month</strong></p>
                        </div>
                        
                        <hr style="margin: 30px 0;">
                        
                        <h3>📚 Getting Started Tips:</h3>
                        <ol>
                            <li><strong>Explore the Dashboard</strong> - Check out our real-time metrics</li>
                            <li><strong>Browse Mining Data</strong> - Understand network health</li>
                            <li><strong>Monitor Price Trends</strong> - Track market movements</li>
                            <li><strong>Consider Premium</strong> - Unlock advanced features</li>
                        </ol>
                        
                        <p>If you have any questions, our support team is here to help at <strong>support@kaspaanalytics.com</strong></p>
                        
                        <p>Thank you for choosing Kaspa Analytics!</p>
                        
                        <p>Best regards,<br>
                        <strong>The Kaspa Analytics Team</strong></p>
                    </div>
                    <div class="footer">
                        <p><strong>© 2025 Kaspa Analytics</strong></p>
                        <p>Advanced Cryptocurrency Analytics Platform</p>
                        <p style="margin-top: 16px; opacity: 0.7;">You received this email because you created an account with us.</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            # Text version
            text_content = f"""
            Welcome to Kaspa Analytics!
            
            Hello {username},
            
            Welcome to Kaspa Analytics! We're excited to have you join our community.
            
            What you can do now:
            • Mining Analytics - Track network hashrate and difficulty
            • Market Data - Real-time price, volume, and market cap  
            • Social Insights - Community sentiment and trends
            • Interactive Charts - Beautiful data visualizations
            
            Start exploring: {self.domain}
            
            Want more? Upgrade to Premium for:
            • AI-Powered Insights
            • Whale Tracking
            • Custom Alerts
            • Advanced Charts
            • Priority Support
            
            Plans starting at just $9.99/month
            
            Questions? Contact us at support@kaspaanalytics.com
            
            Best regards,
            The Kaspa Analytics Team
            
            © 2025 Kaspa Analytics
            """
            
            return self._send_email(to_email, username, "🎉 Welcome to Kaspa Analytics!", html_content, text_content)
            
        except Exception as e:
            st.write(f"Debug: Error sending welcome email: {e}")
            return self.simulate_email(to_email, None, username, "welcome")
    
    def send_cancellation_email(self, to_email, username):
        """Send subscription cancellation confirmation email"""
        try:
            if not self.mailjet:
                st.write("Debug: Mailjet not configured, simulating cancellation email...")
                return self.simulate_email(to_email, None, username, "cancellation")
            
            # HTML cancellation email template
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <title>Subscription Cancelled - Kaspa Analytics</title>
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
                        background: linear-gradient(135deg, #dc3545 0%, #c82333 100%); 
                        color: white; 
                        padding: 30px; 
                        text-align: center; 
                    }}
                    .content {{ 
                        padding: 40px 30px; 
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
                    .info-box {{
                        background: #e9ecef;
                        border: 1px solid #ced4da;
                        padding: 20px;
                        margin: 20px 0;
                        border-radius: 8px;
                    }}
                    .highlight-box {{
                        background: #fff3cd;
                        border: 1px solid #ffeaa7;
                        color: #856404;
                        padding: 20px;
                        margin: 20px 0;
                        border-radius: 8px;
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
                        <h1>📋 Subscription Cancelled</h1>
                        <p>Kaspa Analytics Premium</p>
                    </div>
                    <div class="content">
                        <p>Hello <strong>{username}</strong>,</p>
                        
                        <p>We've successfully processed your premium subscription cancellation request.</p>
                        
                        <div class="info-box">
                            <h3>📅 What happens now:</h3>
                            <ul>
                                <li><strong>✅ Immediate:</strong> No future charges will be made</li>
                                <li><strong>📊 Current Period:</strong> You'll keep premium access until your current billing period ends</li>
                                <li><strong>🔄 After Expiry:</strong> Your account will automatically switch to free tier</li>
                                <li><strong>💾 Data Saved:</strong> All your account data and preferences are preserved</li>
                            </ul>
                        </div>
                        
                        <div class="highlight-box">
                            <h3>🎯 You'll still have access to:</h3>
                            <ul>
                                <li><strong>⛏️ Mining Analytics</strong> - Network hashrate and difficulty tracking</li>
                                <li><strong>💰 Market Data</strong> - Real-time price, volume, and market cap</li>
                                <li><strong>📱 Social Insights</strong> - Community sentiment and trends</li>
                                <li><strong>📊 Basic Charts</strong> - Essential data visualizations</li>
                            </ul>
                        </div>
                        
                        <h3>💔 We're sorry to see you go!</h3>
                        <p>We'd love to understand how we can improve. If you have a moment, please let us know why you cancelled:</p>
                        
                        <ul>
                            <li>📧 Email us at <strong>feedback@kaspaanalytics.com</strong></li>
                            <li>💬 Or reply to this email with your thoughts</li>
                        </ul>
                        
                        <div style="text-align: center; margin: 30px 0;">
                            <a href="{self.domain}" class="button">🔙 Continue Using Free Features</a>
                        </div>
                        
                        <h3>🔄 Want to reactivate later?</h3>
                        <p>You can upgrade to premium again anytime from your account dashboard. Your preferences and settings will be waiting for you!</p>
                        
                        <hr style="margin: 30px 0;">
                        
                        <p>Thank you for being part of the Kaspa Analytics community. We hope to see you back soon!</p>
                        
                        <p>Best regards,<br>
                        <strong>The Kaspa Analytics Team</strong></p>
                    </div>
                    <div class="footer">
                        <p><strong>© 2025 Kaspa Analytics</strong></p>
                        <p>Advanced Cryptocurrency Analytics Platform</p>
                        <p style="margin-top: 16px; opacity: 0.7;">You received this email to confirm your subscription cancellation.</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            # Text version
            text_content = f"""
            Subscription Cancelled - Kaspa Analytics
            
            Hello {username},
            
            We've successfully processed your premium subscription cancellation request.
            
            What happens now:
            • No future charges will be made
            • You'll keep premium access until your current billing period ends
            • After expiry, your account switches to free tier
            • All your data and preferences are preserved
            
            You'll still have access to:
            • Mining Analytics
            • Market Data  
            • Social Insights
            • Basic Charts
            
            We're sorry to see you go! Please share feedback at feedback@kaspaanalytics.com
            
            Want to reactivate later? You can upgrade anytime from your dashboard.
            
            Continue using free features: {self.domain}
            
            Thank you for being part of our community!
            
            Best regards,
            The Kaspa Analytics Team
            
            © 2025 Kaspa Analytics
            """
            
            return self._send_email(to_email, username, "📋 Subscription Cancelled - Kaspa Analytics", html_content, text_content)
            
        except Exception as e:
            st.write(f"Debug: Error sending cancellation email: {e}")
            return self.simulate_email(to_email, None, username, "cancellation")
    
    def _send_email(self, to_email, username, subject, html_content, text_content):
        """Helper method to send email via Mailjet"""
        try:
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
                        "Subject": subject,
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
            **Subject:** 🔑 Reset Your Kaspa Analytics Password
            
            Hello {username}, we received a request to reset your password.
            **Reset Link:** {reset_url}
            """)
            st.markdown(f"**[🔄 CLICK HERE TO RESET PASSWORD]({reset_url})**")
            
        elif email_type == "welcome":
            st.info(f"""
            📧 **Welcome Email Simulated**
            
            **To:** {to_email}  
            **Subject:** 🎉 Welcome to Kaspa Analytics!
            
            Hello {username}, welcome to Kaspa Analytics! 
            Start exploring our features and consider upgrading to premium.
            """)
            st.markdown(f"**[🔥 Start Exploring Analytics]({self.domain})**")
            
        elif email_type == "cancellation":
            st.info(f"""
            📧 **Cancellation Email Simulated**
            
            **To:** {to_email}  
            **Subject:** 📋 Subscription Cancelled - Kaspa Analytics
            
            Hello {username}, your premium subscription has been cancelled.
            You'll keep access until your billing period ends.
            """)
            st.markdown(f"**[🔙 Continue Using Free Features]({self.domain})**")
        
        return True
