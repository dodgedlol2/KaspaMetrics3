import bcrypt
import secrets
import streamlit as st
from database import Database
from datetime import datetime, timedelta
import json
import base64
import hashlib

class AuthHandler:
    def __init__(self, database):
        self.db = database
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
    
    def get_remember_me_key(self):
        """Generate a unique key for remember me based on browser session"""
        # Use a combination of browser info to create a semi-persistent key
        # This won't survive browser restart but will work for the session
        try:
            import streamlit.runtime.scriptrunner as sr
            script_run_ctx = sr.get_script_run_ctx()
            if script_run_ctx and script_run_ctx.session_id:
                session_id = script_run_ctx.session_id
                # Create a hash of session ID for consistency
                return f"remember_me_{hashlib.md5(session_id.encode()).hexdigest()[:16]}"
        except:
            pass
        return "remember_me_default"
    
    def set_persistent_login(self, username):
        """Set persistent login using Streamlit's session state with a semi-permanent key"""
        try:
            token = self.create_auth_token(username)
            if token:
                remember_key = self.get_remember_me_key()
                
                # Store in session state with remember me key
                st.session_state[remember_key] = {
                    'token': token,
                    'username': username,
                    'created_at': datetime.now().isoformat()
                }
                
                # Also set a simpler fallback
                st.session_state['remember_me_token'] = token
                st.session_state['remember_me_username'] = username
                
                st.write(f"Debug: Remember me set for {username} with key {remember_key}")
                return True
        except Exception as e:
            st.write(f"Debug: Error setting persistent login: {e}")
        return False
    
    def check_persistent_login(self):
        """Check if user has valid persistent login"""
        try:
            # Skip if already checked or logged in
            if st.session_state.get('authentication_status') or st.session_state.get('cookie_login_checked'):
                return False
            
            # Method 1: Check with session-based key
            remember_key = self.get_remember_me_key()
            remember_data = st.session_state.get(remember_key)
            
            if remember_data:
                token = remember_data.get('token')
                username = remember_data.get('username')
                
                if token and username:
                    if self.verify_auth_token(token):
                        return self._auto_login_user(username, "session key")
            
            # Method 2: Check fallback remember me token
            fallback_token = st.session_state.get('remember_me_token')
            fallback_username = st.session_state.get('remember_me_username')
            
            if fallback_token and fallback_username:
                if self.verify_auth_token(fallback_token):
                    return self._auto_login_user(fallback_username, "fallback token")
            
            # Mark as checked
            st.session_state['cookie_login_checked'] = True
            return False
            
        except Exception as e:
            st.write(f"Debug: Error checking persistent login: {e}")
            st.session_state['cookie_login_checked'] = True
            return False
    
    def _auto_login_user(self, username, method):
        """Helper method to auto-login user"""
        try:
            user = self.db.get_user(username)
            if user:
                # Set session state
                st.session_state['authentication_status'] = True
                st.session_state['username'] = username
                st.session_state['name'] = user['name']
                st.session_state['is_premium'] = user['is_premium']
                st.session_state['premium_expires_at'] = user['premium_expires_at']
                st.session_state['cookie_login_checked'] = True
                
                st.write(f"Debug: Auto-logged in user {username} via {method}")
                return True
        except Exception as e:
            st.write(f"Debug: Error auto-logging in user: {e}")
        return False
    
    def logout(self):
        """Logout user and clear persistent login"""
        try:
            # Clear remember me data
            remember_key = self.get_remember_me_key()
            
            # Clear all auth-related session state
            keys_to_clear = [
                'authentication_status', 'username', 'name', 'is_premium', 
                'premium_expires_at', 'cookie_login_checked', 'remember_me_token',
                'remember_me_username', remember_key
            ]
            
            for key in keys_to_clear:
                if key in st.session_state:
                    del st.session_state[key]
            
            st.write("Debug: Logged out and cleared remember me data")
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
