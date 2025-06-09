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
        """Set persistent login cookie using HTML/JavaScript"""
        try:
            token = self.create_auth_token(username)
            if token:
                # Use HTML/JavaScript to set cookie since streamlit-cookies-controller has issues
                cookie_script = f"""
                <script>
                document.cookie = "{self.cookie_name}={token}; path=/; max-age={self.cookie_expiry_days * 24 * 60 * 60}; SameSite=Strict; Secure";
                </script>
                """
                st.markdown(cookie_script, unsafe_allow_html=True)
                st.write(f"Debug: Cookie set for {username}")
                return True
        except Exception as e:
            st.write(f"Debug: Error setting persistent login: {e}")
        return False
    
    def get_cookie_value(self, cookie_name):
        """Get cookie value using JavaScript"""
        try:
            # Create a unique key for this cookie check
            import time
            key = f"cookie_check_{int(time.time())}"
            
            cookie_script = f"""
            <script>
            function getCookie(name) {{
                let nameEQ = name + "=";
                let ca = document.cookie.split(';');
                for(let i=0;i < ca.length;i++) {{
                    let c = ca[i];
                    while (c.charAt(0)==' ') c = c.substring(1,c.length);
                    if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
                }}
                return null;
            }}
            
            const cookieValue = getCookie('{cookie_name}');
            if (cookieValue) {{
                window.parent.postMessage({{
                    type: 'cookie_value',
                    cookie: cookieValue
                }}, '*');
            }}
            </script>
            """
            
            # Use components.html to execute JavaScript
            import streamlit.components.v1 as components
            components.html(cookie_script, height=0)
            
            # Check if cookie value was stored in session state by the JavaScript
            return st.session_state.get(f'cookie_{cookie_name}')
            
        except Exception as e:
            st.write(f"Debug: Error getting cookie: {e}")
            return None
    
    def check_persistent_login(self):
        """Check if user has valid persistent login cookie"""
        try:
            # Don't check multiple times in same session
            if st.session_state.get('cookie_login_checked'):
                return False
            
            # Try to get cookie using URL query params as fallback method
            # This is a simpler approach that works better with Streamlit
            
            # Check if there's a stored auth token in session state from previous cookie
            stored_token = st.session_state.get('stored_auth_token')
            
            if stored_token:
                username = self.verify_auth_token(stored_token)
                if username:
                    user = self.db.get_user(username)
                    if user:
                        # Set session state
                        st.session_state['authentication_status'] = True
                        st.session_state['username'] = username
                        st.session_state['name'] = user['name']
                        st.session_state['is_premium'] = user['is_premium']
                        st.session_state['premium_expires_at'] = user['premium_expires_at']
                        st.session_state['cookie_login_checked'] = True
                        
                        st.write(f"Debug: Auto-logged in user {username} from stored token")
                        return True
            
            st.session_state['cookie_login_checked'] = True
            return False
            
        except Exception as e:
            st.write(f"Debug: Error checking persistent login: {e}")
            st.session_state['cookie_login_checked'] = True
            return False
    
    def logout(self):
        """Logout user and clear persistent login"""
        try:
            # Clear cookie using JavaScript
            cookie_script = f"""
            <script>
            document.cookie = "{self.cookie_name}=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT; SameSite=Strict";
            </script>
            """
            st.markdown(cookie_script, unsafe_allow_html=True)
            
            # Clear session state
            for key in ['authentication_status', 'username', 'name', 'is_premium', 'premium_expires_at', 'cookie_login_checked', 'stored_auth_token']:
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
                    token = self.create_auth_token(username)
                    if token:
                        # Store token in session state as backup method
                        st.session_state['stored_auth_token'] = token
                        # Also try to set browser cookie
                        self.set_persistent_login(username)
                        st.write(f"Debug: Remember me enabled for {username}")
                
                return True
        return False
