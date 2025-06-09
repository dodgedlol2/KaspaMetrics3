import bcrypt
import secrets
import streamlit as st
from database import Database
from datetime import datetime, timedelta
import json
import base64

class AuthHandler:
    def __init__(self, database):
        self.db = database
        # DON'T initialize cookie controller here - that causes caching issues
        self.cookie_name = "kaspa_auth_token"
        self.cookie_expiry_days = 30
    
    def authenticate(self, username, password):
        """Authenticate user with username and password"""
        user = self.db.get_user(username)
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            return True
        return False
    
    def is_premium_user(self, username):
        """Check if user has premium access"""
        user = self.db.get_user(username)
        return user['is_premium'] if user else False
    
    def upgrade_to_premium(self, username):
        """Upgrade user to premium status"""
        self.db.update_premium_status(username, True)
    
    def get_user_info(self, username):
        """Get user information"""
        return self.db.get_user(username)
    
    def create_auth_token(self, username):
        """Create a secure authentication token for persistent login"""
        try:
            # Create token data
            token_data = {
                'username': username,
                'created_at': datetime.now().isoformat(),
                'random': secrets.token_hex(16)
            }
            
            # Convert to JSON and encode
            token_json = json.dumps(token_data)
            token_encoded = base64.b64encode(token_json.encode()).decode()
            
            return token_encoded
        except Exception as e:
            st.write(f"Debug: Error creating auth token: {e}")
            return None
    
    def verify_auth_token(self, token):
        """Verify authentication token and return username if valid"""
        try:
            # Decode token
            token_json = base64.b64decode(token.encode()).decode()
            token_data = json.loads(token_json)
            
            username = token_data.get('username')
            created_at = token_data.get('created_at')
            
            if not username or not created_at:
                return None
            
            # Check if token is expired (30 days)
            token_date = datetime.fromisoformat(created_at)
            if datetime.now() - token_date > timedelta(days=self.cookie_expiry_days):
                return None
            
            # Verify user still exists in database
            user = self.db.get_user(username)
            if not user:
                return None
            
            return username
            
        except Exception as e:
            st.write(f"Debug: Error verifying auth token: {e}")
            return None
    
    def set_persistent_login(self, username):
        """Set persistent login cookie"""
        try:
            # Import here to avoid caching issues
            from streamlit_cookies_controller import CookieController
            cookie_controller = CookieController()
            
            token = self.create_auth_token(username)
            if token:
                # Set cookie to expire in 30 days
                cookie_controller.set(
                    self.cookie_name, 
                    token,
                    max_age=self.cookie_expiry_days * 24 * 60 * 60  # 30 days in seconds
                )
                st.write(f"Debug: Cookie set for {username}")
                return True
        except Exception as e:
            st.write(f"Debug: Error setting persistent login: {e}")
        return False
    
    def check_persistent_login(self):
        """Check if user has valid persistent login cookie"""
        try:
            # Import here to avoid caching issues
            from streamlit_cookies_controller import CookieController
            cookie_controller = CookieController()
            
            # Skip if already checked or logged in
            if st.session_state.get('authentication_status') or st.session_state.get('cookie_login_checked'):
                return False
            
            token = cookie_controller.get(self.cookie_name)
            if token:
                username = self.verify_auth_token(token)
                if username:
                    # Valid token found, auto-login user
                    user = self.db.get_user(username)
                    if user:
                        # Set session state
                        st.session_state['authentication_status'] = True
                        st.session_state['username'] = username
                        st.session_state['name'] = user['name']
                        st.session_state['is_premium'] = user['is_premium']
                        st.session_state['premium_expires_at'] = user['premium_expires_at']
                        st.session_state['cookie_login_checked'] = True
                        
                        # Refresh cookie expiry
                        self.set_persistent_login(username)
                        
                        st.write(f"Debug: Auto-logged in user {username} from cookie")
                        return True
            
            # Mark as checked
            st.session_state['cookie_login_checked'] = True
            return False
            
        except Exception as e:
            st.write(f"Debug: Error checking persistent login: {e}")
            st.session_state['cookie_login_checked'] = True
            return False
    
    def logout(self):
        """Logout user and clear persistent login"""
        try:
            # Import here to avoid caching issues
            from streamlit_cookies_controller import CookieController
            cookie_controller = CookieController()
            
            # Clear cookie
            cookie_controller.remove(self.cookie_name)
            
            # Clear session state
            for key in ['authentication_status', 'username', 'name', 'is_premium', 'premium_expires_at', 'cookie_login_checked']:
                if key in st.session_state:
                    del st.session_state[key]
            
            st.write("Debug: Logged out and cleared cookies")
            return True
        except Exception as e:
            st.write(f"Debug: Error during logout: {e}")
            return False
    
    def login_user(self, username, password, remember_me=True):
        """Complete login process with optional persistent login"""
        if self.authenticate(username, password):
            user = self.db.get_user(username)
            if user:
                # Set session state
                st.session_state['authentication_status'] = True
                st.session_state['username'] = username
                st.session_state['name'] = user['name']
                st.session_state['is_premium'] = user['is_premium']
                st.session_state['premium_expires_at'] = user['premium_expires_at']
                
                # Set persistent login if requested
                if remember_me:
                    self.set_persistent_login(username)
                    st.write(f"Debug: Remember me enabled for {username}")
                
                return True
        return False
