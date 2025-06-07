import sqlite3
import bcrypt
import os
import streamlit as st

class Database:
    def __init__(self, db_path="kaspa_users.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database with users table"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            name TEXT NOT NULL,
            is_premium BOOLEAN DEFAULT FALSE,
            premium_expires_at TIMESTAMP NULL,
            stripe_customer_id TEXT,
            stripe_subscription_id TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Create default demo users if they don't exist
        self.create_demo_users(cursor)
        
        conn.commit()
        conn.close()
    
    def create_demo_users(self, cursor):
        """Create demo users for testing"""
        demo_password = bcrypt.hashpw("demo123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        users = [
            ("demo_user", "demo@kaspa.com", demo_password, "Demo User", False),
            ("premium_user", "premium@kaspa.com", demo_password, "Premium User", True)
        ]
        
        for user in users:
            cursor.execute('''
            INSERT OR IGNORE INTO users (username, email, password, name, is_premium)
            VALUES (?, ?, ?, ?, ?)
            ''', user)
    
    def add_user(self, username, email, password, name):
        """Add a new user to the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        try:
            cursor.execute('''
            INSERT INTO users (username, email, password, name, is_premium)
            VALUES (?, ?, ?, ?, ?)
            ''', (username, email, hashed_password, name, False))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()
    
    def get_user(self, username):
        """Get user by username"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return {
                'id': user[0],
                'username': user[1],
                'email': user[2],
                'password': user[3],
                'name': user[4],
                'is_premium': bool(user[5]),
                'premium_expires_at': user[6],
                'stripe_customer_id': user[7],
                'stripe_subscription_id': user[8]
            }
        return None
    
    def update_premium_status(self, username, is_premium, expires_at=None, subscription_id=None):
        """Update user's premium status with expiration date"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                UPDATE users 
                SET is_premium = ?, premium_expires_at = ?, stripe_subscription_id = ? 
                WHERE username = ?
            ''', (is_premium, expires_at, subscription_id, username))
            
            rows_affected = cursor.rowcount
            conn.commit()
            
            # Debug: Verify the update worked
            cursor.execute('SELECT username, is_premium, premium_expires_at FROM users WHERE username = ?', (username,))
            result = cursor.fetchone()
            
            if result and rows_affected > 0:
                st.write(f"Debug: Successfully updated {username} premium status to {is_premium}")
                st.write(f"Debug: Expires at: {expires_at}")
                return True
            else:
                st.write(f"Debug: Failed to update {username} - user not found or no changes made")
                return False
                
        except Exception as e:
            st.write(f"Debug: Database error updating premium status: {e}")
            return False
        finally:
            conn.close()
    
    def check_premium_expiration(self, username):
        """Check if user's premium subscription has expired"""
        from datetime import datetime
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT premium_expires_at, is_premium FROM users WHERE username = ?', (username,))
        result = cursor.fetchone()
        conn.close()
        
        if result and result[1]:  # is_premium is True
            expires_at = result[0]
            if expires_at:
                # Parse the expiration date
                try:
                    expiry_date = datetime.fromisoformat(expires_at.replace('Z', '+00:00'))
                    if datetime.now() > expiry_date:
                        # Subscription expired, update user
                        self.update_premium_status(username, False)
                        return False, "Subscription expired"
                    else:
                        return True, expiry_date
                except:
                    return True, "Active"
            else:
                return True, "Lifetime"  # No expiration set
        return False, "Not premium"
