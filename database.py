import psycopg2
import bcrypt
import os
import streamlit as st
from urllib.parse import urlparse

class Database:
    def __init__(self):
        # Get database URL from Streamlit secrets or environment
        try:
            # Try accessing from [default] section first
            self.database_url = st.secrets["default"]["DATABASE_URL"]
            st.write(f"Debug: Found DATABASE_URL in default section: {self.database_url[:30]}...")
        except Exception as e:
            st.write(f"Debug: Error accessing default section: {e}")
            try:
                # Fallback to direct access
                self.database_url = st.secrets["DATABASE_URL"]
                st.write(f"Debug: Found DATABASE_URL direct: {self.database_url[:30]}...")
            except Exception as e2:
                # Final fallback to SQLite
                self.database_url = os.getenv('DATABASE_URL', 'sqlite:///kaspa_users.db')
                st.write(f"Debug: Error accessing DATABASE_URL directly: {e2}")
                st.write(f"Debug: Using fallback SQLite: {self.database_url}")
        
        # Check if using PostgreSQL (Supabase) or fallback to SQLite
        if self.database_url.startswith('postgresql://'):
            self.use_postgres = True
            st.write("Debug: Initializing PostgreSQL database...")
            self.init_postgres_database()
        else:
            self.use_postgres = False
            st.write("Debug: Initializing SQLite database...")
            self.init_sqlite_database()
    
    def get_connection(self):
        """Get database connection"""
        if self.use_postgres:
            st.write(f"Debug: Connecting to PostgreSQL...")
            try:
                conn = psycopg2.connect(self.database_url)
                st.write("Debug: PostgreSQL connection successful!")
                return conn
            except Exception as e:
                st.write(f"Debug: PostgreSQL connection failed: {e}")
                raise e
        else:
            st.write(f"Debug: Connecting to SQLite...")
            import sqlite3
            return sqlite3.connect('kaspa_users.db')
    
    def init_postgres_database(self):
        """Initialize PostgreSQL database with users table"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            st.write("Debug: Creating PostgreSQL users table...")
            
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
            
            st.write("Debug: PostgreSQL users table created/verified!")
            
            # Create default demo users if they don't exist
            self.create_demo_users_postgres(cursor)
            
            conn.commit()
            conn.close()
            st.write("Debug: PostgreSQL database initialization complete!")
            
        except Exception as e:
            st.write(f"Debug: Error initializing PostgreSQL: {e}")
            raise e
    
    def init_sqlite_database(self):
        """Initialize SQLite database (fallback)"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            st.write("Debug: Creating SQLite users table...")
            
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
            st.write("Debug: SQLite database initialization complete!")
            
        except Exception as e:
            st.write(f"Debug: Error initializing SQLite: {e}")
            raise e
    
    def create_demo_users_postgres(self, cursor):
        """Create demo users for PostgreSQL"""
        try:
            st.write("Debug: Creating demo users in PostgreSQL...")
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
            
            st.write("Debug: Demo users created in PostgreSQL!")
            
        except Exception as e:
            st.write(f"Debug: Error creating demo users in PostgreSQL: {e}")
    
    def create_demo_users_sqlite(self, cursor):
        """Create demo users for SQLite"""
        try:
            st.write("Debug: Creating demo users in SQLite...")
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
            
            st.write("Debug: Demo users created in SQLite!")
            
        except Exception as e:
            st.write(f"Debug: Error creating demo users in SQLite: {e}")
    
    def add_user(self, username, email, password, name):
        """Add a new user to the database"""
        try:
            st.write(f"Debug: Adding user {username} to database...")
            conn = self.get_connection()
            cursor = conn.cursor()
            
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
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
            conn.close()
            st.write(f"Debug: User {username} added successfully!")
            return True
            
        except Exception as e:
            st.write(f"Debug: Error adding user {username}: {e}")
            return False
    
    def get_user(self, username):
        """Get user by username"""
        try:
            st.write(f"Debug: Getting user {username} from database...")
            conn = self.get_connection()
            cursor = conn.cursor()
            
            if self.use_postgres:
                cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
            else:
                cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
            
            user = cursor.fetchone()
            conn.close()
            
            if user:
                st.write(f"Debug: User {username} found!")
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
            else:
                st.write(f"Debug: User {username} not found!")
                return None
                
        except Exception as e:
            st.write(f"Debug: Error getting user {username}: {e}")
            return None
    
    def update_premium_status(self, username, is_premium, expires_at=None, subscription_id=None):
        """Update user's premium status with expiration date"""
        try:
            st.write(f"Debug: Updating premium status for {username} to {is_premium}")
            conn = self.get_connection()
            cursor = conn.cursor()
            
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
            conn.close()
            
            if rows_affected > 0:
                st.write(f"Debug: Successfully updated {username} premium status to {is_premium}")
                st.write(f"Debug: Expires at: {expires_at}")
                return True
            else:
                st.write(f"Debug: Failed to update {username} - user not found")
                return False
                
        except Exception as e:
            st.write(f"Debug: Error updating premium status for {username}: {e}")
            return False
    
    def check_premium_expiration(self, username):
        """Check if user's premium subscription has expired"""
        try:
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
            
        except Exception as e:
            st.write(f"Debug: Error checking premium expiration for {username}: {e}")
            return False, "Error"
