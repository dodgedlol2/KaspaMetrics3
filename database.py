import psycopg2
import bcrypt
import os
import streamlit as st
from urllib.parse import urlparse

def __init__(self):
    # DEBUG: Check if secrets are accessible
    try:
        test_url = st.secrets["DATABASE_URL"]
        st.write(f"Debug: Found DATABASE_URL in secrets: {test_url[:30]}...")
    except Exception as e:
        st.write(f"Debug: Error accessing DATABASE_URL: {e}")
    
    # Get database URL from Streamlit secrets or environment
    try:
        self.database_url = st.secrets["DATABASE_URL"]
    except:
        self.database_url = os.getenv('DATABASE_URL', 'sqlite:///kaspa_users.db')
    
    st.write(f"Debug: Using database URL: {self.database_url[:30]}...")
 # DEBUG: Check if secrets are accessible

class Database:
    def __init__(self):
        # Get database URL from Streamlit secrets or environment
        try:
            self.database_url = st.secrets["DATABASE_URL"]
        except:
            self.database_url = os.getenv('DATABASE_URL', 'sqlite:///kaspa_users.db')
        
        # Check if using PostgreSQL (Supabase) or fallback to SQLite
        if self.database_url.startswith('postgresql://'):
            self.use_postgres = True
            self.init_postgres_database()
        else:
            self.use_postgres = False
            self.init_sqlite_database()
    
    def get_connection(self):
        """Get database connection"""
        if self.use_postgres:
            return psycopg2.connect(self.database_url)
        else:
            import sqlite3
            return sqlite3.connect('kaspa_users.db')
    
    def init_postgres_database(self):
        """Initialize PostgreSQL database with users table"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Create users table for PostgreSQL
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            name VARCHAR(100) NOT NULL,
            is_premium BOOLEAN DEFAULT FALSE,
            premium_expires_at TIMESTAMP NULL,
            stripe_customer_id VARCHAR(100),
            stripe_subscription_id VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Create default demo users if they don't exist
        self.create_demo_users_postgres(cursor)
        
        conn.commit()
        conn.close()
    
    def init_sqlite_database(self):
        """Initialize SQLite database (fallback)"""
        conn = self.get_connection()
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
        
        self.create_demo_users_sqlite(cursor)
        conn.commit()
        conn.close()
    
    def create_demo_users_postgres(self, cursor):
        """Create demo users for PostgreSQL"""
        demo_password = bcrypt.hashpw("demo123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        users = [
            ("demo_user", "demo@kaspa.com", demo_password, "Demo User", False),
            ("premium_user", "premium@kaspa.com", demo_password, "Premium User", True)
        ]
        
        for user in users:
            cursor.execute('''
            INSERT INTO users (username, email, password, name, is_premium)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (username) DO NOTHING
            ''', user)
    
    def create_demo_users_sqlite(self, cursor):
        """Create demo users for SQLite"""
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
        conn = self.get_connection()
        cursor = conn.cursor()
        
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        try:
            if self.use_postgres:
                cursor.execute('''
                INSERT INTO users (username, email, password, name, is_premium)
                VALUES (%s, %s, %s, %s, %s)
                ''', (username, email, hashed_password, name, False))
            else:
                cursor.execute('''
                INSERT INTO users (username, email, password, name, is_premium)
                VALUES (?, ?, ?, ?, ?)
                ''', (username, email, hashed_password, name, False))
            
            conn.commit()
            return True
        except Exception as e:
            st.write(f"Debug: Database error adding user: {e}")
            return False
        finally:
            conn.close()
    
    def get_user(self, username):
        """Get user by username"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if self.use_postgres:
            cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        else:
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
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            if self.use_postgres:
                cursor.execute('''
                    UPDATE users 
                    SET is_premium = %s, premium_expires_at = %s, stripe_subscription_id = %s 
                    WHERE username = %s
                ''', (is_premium, expires_at, subscription_id, username))
            else:
                cursor.execute('''
                    UPDATE users 
                    SET is_premium = ?, premium_expires_at = ?, stripe_subscription_id = ? 
                    WHERE username = ?
                ''', (is_premium, expires_at, subscription_id, username))
            
            rows_affected = cursor.rowcount
            conn.commit()
            
            if rows_affected > 0:
                st.write(f"Debug: Successfully updated {username} premium status to {is_premium}")
                return True
            else:
                st.write(f"Debug: Failed to update {username}")
                return False
                
        except Exception as e:
            st.write(f"Debug: Database error updating premium status: {e}")
            return False
        finally:
            conn.close()
    
    def check_premium_expiration(self, username):
        """Check if user's premium subscription has expired"""
        from datetime import datetime
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if self.use_postgres:
            cursor.execute('SELECT premium_expires_at, is_premium FROM users WHERE username = %s', (username,))
        else:
            cursor.execute('SELECT premium_expires_at, is_premium FROM users WHERE username = ?', (username,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result and result[1]:  # is_premium is True
            expires_at = result[0]
            if expires_at:
                try:
                    if isinstance(expires_at, str):
                        expiry_date = datetime.fromisoformat(expires_at.replace('Z', '+00:00'))
                    else:
                        expiry_date = expires_at
                        
                    if datetime.now() > expiry_date:
                        # Subscription expired, update user
                        self.update_premium_status(username, False)
                        return False, "Subscription expired"
                    else:
                        return True, expiry_date
                except:
                    return True, "Active"
            else:
                return True, "Lifetime"
        return False, "Not premium"
