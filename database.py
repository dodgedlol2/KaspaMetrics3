import psycopg2
import bcrypt
import os
import streamlit as st
from urllib.parse import urlparse
import secrets
from datetime import datetime, timedelta

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
            
            # Check if reset token columns exist and add them if needed
            try:
                cursor.execute("""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name='users' AND column_name IN ('reset_token', 'reset_token_expires')
                """)
                existing_columns = [row[0] for row in cursor.fetchall()]
                
                if 'reset_token' not in existing_columns:
                    cursor.execute('ALTER TABLE users ADD COLUMN reset_token VARCHAR(100) NULL')
                    st.write("Debug: Added reset_token column")
                
                if 'reset_token_expires' not in existing_columns:
                    cursor.execute('ALTER TABLE users ADD COLUMN reset_token_expires TIMESTAMP NULL')
                    st.write("Debug: Added reset_token_expires column")
                
                conn.commit()
                
            except Exception as col_error:
                st.write(f"Debug: Error adding columns (may already exist): {col_error}")
                conn.rollback()
            
            # Create default demo users if they don't exist - in separate transaction
            try:
                self.create_demo_users_postgres(cursor)
                conn.commit()
            except Exception as demo_error:
                st.write(f"Debug: Error creating demo users: {demo_error}")
                conn.rollback()
                # Try again with fresh connection
                try:
                    conn.close()
                    conn = self.get_connection()
                    cursor = conn.cursor()
                    self.create_demo_users_postgres(cursor)
                    conn.commit()
                    st.write("Debug: Demo users created successfully on retry!")
                except Exception as retry_error:
                    st.write(f"Debug: Still couldn't create demo users: {retry_error}")
                    conn.rollback()
            
            conn.close()
            st.write("Debug: PostgreSQL database initialization complete!")
            
        except Exception as e:
            st.write(f"Debug: Error initializing PostgreSQL: {e}")
            try:
                conn.rollback()
                conn.close()
            except:
                pass
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
            
            # Check if reset token columns exist and add them if needed
            try:
                cursor.execute("PRAGMA table_info(users)")
                columns = [column[1] for column in cursor.fetchall()]
                
                if 'reset_token' not in columns:
                    cursor.execute('ALTER TABLE users ADD COLUMN reset_token TEXT NULL')
                    st.write("Debug: Added reset_token column")
                
                if 'reset_token_expires' not in columns:
                    cursor.execute('ALTER TABLE users ADD COLUMN reset_token_expires TIMESTAMP NULL')
                    st.write("Debug: Added reset_token_expires column")
            
            except Exception as col_error:
                st.write(f"Debug: Error adding columns (may already exist): {col_error}")
            
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
                # Handle cases where reset token columns might not exist
                user_dict = {
                    'id': user[0],
                    'username': user[1],
                    'email': user[2],
                    'password': user[3],
                    'name': user[4],
                    'is_premium': bool(user[5]),
                    'premium_expires_at': user[6],
                    'stripe_customer_id': user[7] if len(user) > 7 else None,
                    'stripe_subscription_id': user[8] if len(user) > 8 else None,
                    'reset_token': user[9] if len(user) > 9 else None,
                    'reset_token_expires': user[10] if len(user) > 10 else None
                }
                return user_dict
            else:
                st.write(f"Debug: User {username} not found!")
                return None
                
        except Exception as e:
            st.write(f"Debug: Error getting user {username}: {e}")
            return None
    
    def get_user_by_email(self, email):
        """Get user by email address"""
        try:
            st.write(f"Debug: Getting user by email {email}...")
            conn = self.get_connection()
            cursor = conn.cursor()
            
            if self.use_postgres:
                cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
            else:
                cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
            
            user = cursor.fetchone()
            conn.close()
            
            if user:
                st.write(f"Debug: User found for email {email}!")
                # Handle cases where reset token columns might not exist
                user_dict = {
                    'id': user[0],
                    'username': user[1],
                    'email': user[2],
                    'password': user[3],
                    'name': user[4],
                    'is_premium': bool(user[5]),
                    'premium_expires_at': user[6],
                    'stripe_customer_id': user[7] if len(user) > 7 else None,
                    'stripe_subscription_id': user[8] if len(user) > 8 else None,
                    'reset_token': user[9] if len(user) > 9 else None,
                    'reset_token_expires': user[10] if len(user) > 10 else None
                }
                return user_dict
            else:
                st.write(f"Debug: No user found for email {email}!")
                return None
                
        except Exception as e:
            st.write(f"Debug: Error getting user by email {email}: {e}")
            return None
    
    def create_reset_token(self, email):
        """Create a password reset token for user"""
        try:
            st.write(f"Debug: Creating reset token for email {email}...")
            
            # Generate secure token
            token = secrets.token_urlsafe(32)
            expires_at = datetime.now() + timedelta(hours=1)  # Token expires in 1 hour
            
            conn = self.get_connection()
            cursor = conn.cursor()
            
            if self.use_postgres:
                cursor.execute('''
                    UPDATE users 
                    SET reset_token = %s, reset_token_expires = %s 
                    WHERE email = %s
                ''', (token, expires_at, email))
            else:
                cursor.execute('''
                    UPDATE users 
                    SET reset_token = ?, reset_token_expires = ? 
                    WHERE email = ?
                ''', (token, expires_at, email))
            
            conn.commit()
            conn.close()
            
            st.write(f"Debug: Reset token created for {email}")
            return token
            
        except Exception as e:
            st.write(f"Debug: Error creating reset token for {email}: {e}")
            return None
    
    def verify_reset_token(self, token):
        """Verify reset token and return user if valid"""
        try:
            st.write(f"Debug: Verifying reset token...")
            conn = self.get_connection()
            cursor = conn.cursor()
            
            if self.use_postgres:
                cursor.execute('''
                    SELECT * FROM users 
                    WHERE reset_token = %s AND reset_token_expires > %s
                ''', (token, datetime.now()))
            else:
                cursor.execute('''
                    SELECT * FROM users 
                    WHERE reset_token = ? AND reset_token_expires > ?
                ''', (token, datetime.now()))
            
            user = cursor.fetchone()
            conn.close()
            
            if user:
                st.write("Debug: Valid reset token found!")
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
                st.write("Debug: Invalid or expired reset token!")
                return None
                
        except Exception as e:
            st.write(f"Debug: Error verifying reset token: {e}")
            return None
    
    def reset_password(self, token, new_password):
        """Reset password using valid token"""
        try:
            st.write(f"Debug: Resetting password with token...")
            
            # First verify token is still valid
            user = self.verify_reset_token(token)
            if not user:
                return False
            
            # Hash new password
            hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            conn = self.get_connection()
            cursor = conn.cursor()
            
            if self.use_postgres:
                cursor.execute('''
                    UPDATE users 
                    SET password = %s, reset_token = NULL, reset_token_expires = NULL 
                    WHERE reset_token = %s
                ''', (hashed_password, token))
            else:
                cursor.execute('''
                    UPDATE users 
                    SET password = ?, reset_token = NULL, reset_token_expires = NULL 
                    WHERE reset_token = ?
                ''', (hashed_password, token))
            
            conn.commit()
            conn.close()
            
            st.write("Debug: Password reset successfully!")
            return True
            
        except Exception as e:
            st.write(f"Debug: Error resetting password: {e}")
            return False
    
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
