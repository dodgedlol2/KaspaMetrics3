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
            stripe_customer_id TEXT,
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
                'stripe_customer_id': user[6]
            }
        return None
    
    def update_premium_status(self, username, is_premium):
        """Update user's premium status"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('UPDATE users SET is_premium = ? WHERE username = ?', (is_premium, username))
        conn.commit()
        conn.close()
