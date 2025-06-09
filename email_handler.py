# Add this new method to your email_handler.py file

def send_renewal_notification_email(self, to_email, username, plan_type, new_expiry_date):
    """Send automatic renewal notification email"""
    try:
        if not self.mailjet:
            st.write("Debug: Mailjet not configured, simulating renewal notification email...")
            return self.simulate_email(to_email, None, username, "renewal_notification")
        
        # HTML renewal notification email template
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
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
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
        
        # Text version
        text_content = f"""
        Subscription Renewed - Kaspa Analytics!
        
        Hello {username},
        
        Great news! Your {plan_type} subscription has been automatically renewed.
        
        Your premium access is now extended until: {new_expiry_date}
        
        Your Premium Features Continue:
        • AI-Powered Insights - Advanced market predictions
        • Whale Tracking - Monitor large transactions  
        • Custom Alerts - Real-time notifications
        • Advanced Charts - Professional trading tools
        • Data Export - Download your analytics
        • Priority Support - Get help when needed
        
        Billing Information:
        • Plan: {plan_type}
        • Status: Active & Auto-Renewing
        • Next Renewal: {new_expiry_date}
        • Billing: Automatic
        
        Continue using premium: {self.domain}
        Manage subscription: {self.domain}/A_👤_Account
        
        Thank you for being a valued Premium member!
        
        Best regards,
        The Kaspa Analytics Team
        
        © 2025 Kaspa Analytics
        """
        
        return self._send_email(to_email, username, "🎉 Subscription Renewed - Kaspa Analytics", html_content, text_content)
        
    except Exception as e:
        st.write(f"Debug: Error sending renewal notification email: {e}")
        return self.simulate_email(to_email, None, username, "renewal_notification")

# Also update the simulate_email method to handle renewal notifications
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
        
    elif email_type == "premium_subscription":
        st.success(f"""
        📧 **Premium Subscription Email Simulated**
        
        **To:** {to_email}  
        **Subject:** 👑 Welcome to Premium - Kaspa Analytics!
        
        Hello {username}, congratulations! Your premium subscription is now active.
        All premium features are now available to you.
        """)
        st.markdown(f"**[🔬 Explore Premium Analytics]({self.domain}/8_👑_Premium_Analytics)**")
        
    elif email_type == "cancellation":
        st.info(f"""
        📧 **Cancellation Email Simulated**
        
        **To:** {to_email}  
        **Subject:** 📋 Subscription Cancelled - Kaspa Analytics
        
        Hello {username}, your premium subscription has been cancelled.
        You'll keep access until your billing period ends.
        """)
        st.markdown(f"**[🔙 Continue Using Free Features]({self.domain})**")
    
    elif email_type == "renewal_notification":
        st.success(f"""
        📧 **Renewal Notification Email Simulated**
        
        **To:** {to_email}  
        **Subject:** 🎉 Subscription Renewed - Kaspa Analytics
        
        Hello {username}, great news! Your subscription has been automatically renewed.
        Your premium access continues without interruption.
        """)
        st.markdown(f"**[🚀 Continue Using Premium]({self.domain})**")
    
    return True
