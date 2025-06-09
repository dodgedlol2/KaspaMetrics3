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
            
            st.write(f"Debug: Created token for {username}: {token_encoded[:50]}...")
            return token_encoded
        except Exception as e:
            st.write(f"Debug: Error creating auth token: {e}")
            return None
    
    def verify_auth_token(self, token):
        """Verify authentication token and return username if valid"""
        try:
            if not token:
                st.write("Debug: No token provided")
                return None
                
            st.write(f"Debug: Verifying token: {token[:50]}...")
            
            # Decode token
            token_json = base64.b64decode(token.encode()).decode()
            token_data = json.loads(token_json)
            
            username = token_data.get('username')
            created_at = token_data.get('created_at')
            
            st.write(f"Debug: Token data - username: {username}, created: {created_at}")
            
            if not username or not created_at:
                st.write("Debug: Missing username or created_at in token")
                return None
            
            # Check if token is expired (30 days)
            token_date = datetime.fromisoformat(created_at)
            age_days = (datetime.now() - token_date).days
            st.write(f"Debug: Token age: {age_days} days (expires after {self.cookie_expiry_days})")
            
            if age_days > self.cookie_expiry_days:
                st.write("Debug: Token expired")
                return None
            
            # Verify user still exists in database
            user = self.db.get_user(username)
            if not user:
                st.write(f"Debug: User {username} not found in database")
                return None
            
            st.write(f"Debug: Token verified successfully for {username}")
            return username
            
        except Exception as e:
            st.write(f"Debug: Error verifying auth token: {e}")
            return None
    
    def set_persistent_login(self, username):
        """Set persistent login cookie"""
        try:
            st.write(f"🔐 **Debug: Setting persistent login for:** {username}")
            
            # Import here to avoid caching issues
            from streamlit_cookies_controller import CookieController
            cookie_controller = CookieController()
            
            token = self.create_auth_token(username)
            if token:
                # Set cookie to expire in 30 days
                max_age_seconds = self.cookie_expiry_days * 24 * 60 * 60
                st.write(f"⏰ **Debug: Cookie expiry:** {self.cookie_expiry_days} days ({max_age_seconds} seconds)")
                
                cookie_controller.set(
                    self.cookie_name, 
                    token,
                    max_age=max_age_seconds
                )
                
                # Verify the cookie was set
                st.write("🔍 **Debug: Verifying cookie was set...**")
                read_back = cookie_controller.get(self.cookie_name)
                if read_back:
                    st.success(f"✅ **Debug: Cookie set successfully!** Preview: {read_back[:50]}...")
                    return True
                else:
                    st.error("❌ **Debug: Cookie was not set or cannot be read back**")
                    return False
                
        except Exception as e:
            st.error(f"💥 **Debug: Error setting persistent login:** {e}")
            import traceback
            st.text(traceback.format_exc())
        return False
    
    def check_persistent_login(self):
        """Check if user has valid persistent login cookie"""
        try:
            # Skip if already authenticated
            if st.session_state.get('authentication_status'):
                return False
            
            # DON'T skip if already checked - we need to check on fresh page loads
            st.write("🔍 **Debug: Checking for persistent login cookie...**")
            
            # Import here to avoid caching issues
            from streamlit_cookies_controller import CookieController
            cookie_controller = CookieController()
            
            # Get all cookies for debugging
            try:
                all_cookies = cookie_controller.getAll()
                st.write(f"🍪 **Debug: All cookies found:** {list(all_cookies.keys()) if all_cookies else 'None'}")
            except Exception as cookie_err:
                st.write(f"⚠️ **Debug: Could not get all cookies:** {cookie_err}")
            
            token = cookie_controller.get(self.cookie_name)
            st.write(f"🔑 **Debug: Auth cookie '{self.cookie_name}':** {'FOUND ✅' if token else 'NOT FOUND ❌'}")
            
            if token:
                st.write(f"📄 **Debug: Token preview:** {token[:50]}...")
                username = self.verify_auth_token(token)
                if username:
                    st.write(f"👤 **Debug: Valid token for user:** {username}")
                    
                    # Valid token found, auto-login user
                    user = self.db.get_user(username)
                    if user:
                        # Set session state
                        st.session_state['authentication_status'] = True
                        st.session_state['username'] = username
                        st.session_state['name'] = user['name']
                        st.session_state['is_premium'] = user['is_premium']
                        st.session_state['premium_expires_at'] = user['premium_expires_at']
                        
                        st.success(f"🎉 **AUTO-LOGIN SUCCESS!** Welcome back, {user['name']}!")
                        
                        # Refresh cookie to extend expiry
                        self.set_persistent_login(username)
                        
                        return True
                    else:
                        st.error(f"❌ **Debug: User {username} not found in database**")
                else:
                    st.error("❌ **Debug: Token verification failed**")
            else:
                st.info("ℹ️ **Debug: No auth cookie found - user needs to login**")
            
            return False
            
        except Exception as e:
            st.error(f"💥 **Debug: Error checking persistent login:** {e}")
            import traceback
            st.text(traceback.format_exc())
            return False
    
    def logout(self):
        """Logout user and clear persistent login"""
        try:
            st.write("Debug: Logging out user...")
            
            # Import here to avoid caching issues
            from streamlit_cookies_controller import CookieController
            cookie_controller = CookieController()
            
            # Clear cookie
            st.write(f"Debug: Removing cookie '{self.cookie_name}'")
            cookie_controller.remove(self.cookie_name)
            
            # Verify cookie was removed
            remaining_cookie = cookie_controller.get(self.cookie_name)
            if remaining_cookie:
                st.write(f"Debug: ❌ Cookie still exists after removal: {remaining_cookie[:50]}...")
            else:
                st.write("Debug: ✅ Cookie successfully removed")
            
            # Clear session state
            keys_to_clear = ['authentication_status', 'username', 'name', 'is_premium', 'premium_expires_at', 'cookie_login_checked']
            for key in keys_to_clear:
                if key in st.session_state:
                    del st.session_state[key]
                    st.write(f"Debug: Cleared session state key: {key}")
            
            st.write("Debug: ✅ Logout completed")
            return True
        except Exception as e:
            st.write(f"Debug: Error during logout: {e}")
            import traceback
            st.write(f"Debug: Full traceback: {traceback.format_exc()}")
            return False
    
    def login_user(self, username, password, remember_me=True):
        """Complete login process with optional persistent login"""
        st.write(f"Debug: Attempting login for {username}, remember_me: {remember_me}")
        
        if self.authenticate(username, password):
            user = self.db.get_user(username)
            if user:
                st.write(f"Debug: Authentication successful for {username}")
                
                # Set session state
                st.session_state['authentication_status'] = True
                st.session_state['username'] = username
                st.session_state['name'] = user['name']
                st.session_state['is_premium'] = user['is_premium']
                st.session_state['premium_expires_at'] = user['premium_expires_at']
                
                # Set persistent login if requested
                if remember_me:
                    st.write(f"Debug: Setting persistent login for {username}")
                    success = self.set_persistent_login(username)
                    if success:
                        st.write("Debug: ✅ Persistent login set successfully")
                    else:
                        st.write("Debug: ❌ Failed to set persistent login")
                
                return True
            else:
                st.write(f"Debug: User {username} not found after authentication")
        else:
            st.write(f"Debug: Authentication failed for {username}")
        return False
