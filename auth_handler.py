import bcrypt
from database import Database

class AuthHandler:
    def __init__(self, database):
        self.db = database
    
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
