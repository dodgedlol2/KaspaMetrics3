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
            self.database_url = st.secrets["default"]["DATABASE_URL"]
        except:
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
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Create users table with all columns
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
                reset_token VARCHAR(100) NULL,
                reset_token_expires TIMESTAMP NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            ''')
            
            conn.commit()
            
            # Create demo users
            self.create_demo_users_postgres(cursor)
            conn.commit()
            conn.close()
            
        except Exception as e:
            try:
                conn.close()
            except:
                pass
    
    def init_sqlite_database(self):
        """Initialize SQLite database (fallback)"""
        try:
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
                reset_token TEXT NULL,
                reset_token_expires TIMESTAMP NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            ''')
            
            self.create_demo_users_sqlite(cursor)
            conn.commit()
            conn.close()
            
        except Exception as e:
            pass
    
    def create_demo_users_postgres(self, cursor):
        """Create demo users for PostgreSQL"""
        try:
            demo_password = bcrypt.hashpw("demo123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            # Check existing users
            cursor.execute('SELECT username FROM users WHERE username IN (%s, %s)', ('demo_user', 'premium_user'))
            existing_users = [row[0] for row in cursor.fetchall()]
            
            if 'demo_user' not in existing_users:
                cursor.execute('''
                INSERT INTO users (username, email, password, name, is_premium)
                VALUES (%s, %s, %s, %s, %s)
                ''', ("demo_user", "demo@kaspa.com", demo_password, "Demo User", False))
                
            if 'premium_user' not in existing_users:
                cursor.execute('''
                INSERT INTO users (username, email, password, name, is_premium)
                VALUES (%s, %s, %s, %s, %s)
                ''', ("premium_user", "premium@kaspa.com", demo_password, "Premium User", True))
            
        except Exception as e:
            pass
    
    def create_demo_users_sqlite(self, cursor):
        """Create demo users for SQLite"""
        try:
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
            
        except Exception as e:
            pass
    
    def add_user(self, username, email, password, name):
        """Add a new user to the database"""
        try:
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
            return True
            
        except Exception as e:
            return False
    
    def get_user(self, username):
        """Get user by username"""
        try:
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
                    'stripe_customer_id': user[7] if len(user) > 7 else None,
                    'stripe_subscription_id': user[8] if len(user) > 8 else None,
                    'reset_token': user[9] if len(user) > 9 else None,
                    'reset_token_expires': user[10] if len(user) > 10 else None,
                    'subscription_cancelled': bool(user[11]) if len(user) > 11 else False
                }
            return None
                
        except Exception as e:
            return None
    
    def get_user_by_email(self, email):
        """Get user by email address"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            if self.use_postgres:
                cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
            else:
                cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
            
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
                    'stripe_customer_id': user[7] if len(user) > 7 else None,
                    'stripe_subscription_id': user[8] if len(user) > 8 else None,
                    'reset_token': user[9] if len(user) > 9 else None,
                    'reset_token_expires': user[10] if len(user) > 10 else None
                }
            return None
                
        except Exception as e:
            return None
    
    def create_reset_token(self, email):
        """Create a password reset token for user"""
        try:
            token = secrets.token_urlsafe(32)
            expires_at = datetime.now() + timedelta(hours=1)
            
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
            return token
            
        except Exception as e:
            return None
    
    def verify_reset_token(self, token):
        """Verify reset token and return user if valid"""
        try:
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
                
        except Exception as e:
            return None
    
    def reset_password(self, token, new_password):
        """Reset password using valid token"""
        try:
            user = self.verify_reset_token(token)
            if not user:
                return False
            
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
            return True
            
        except Exception as e:
            return False
    
    def cancel_premium_subscription(self, username):
        """Cancel user's premium subscription (mark for end of current period)"""
        try:
            # Get current user data first
            user = self.get_user(username)
            if not user:
                return False, "User not found"
            
            if not user['is_premium']:
                return False, "User is not currently premium"
            
            # Check if already cancelled (stripe_subscription_id = 'CANCELLED')
            if user.get('stripe_subscription_id') == 'CANCELLED':
                return False, "Subscription is already cancelled"
            
            # Simple approach - mark subscription as cancelled by setting stripe_subscription_id to 'CANCELLED'
            conn = self.get_connection()
            cursor = conn.cursor()
            
            if self.use_postgres:
                cursor.execute('''
                    UPDATE users 
                    SET stripe_subscription_id = 'CANCELLED'
                    WHERE username = %s AND stripe_subscription_id IS NOT NULL AND stripe_subscription_id != 'CANCELLED'
                ''', (username,))
            else:
                cursor.execute('''
                    UPDATE users 
                    SET stripe_subscription_id = 'CANCELLED'
                    WHERE username = ? AND stripe_subscription_id IS NOT NULL AND stripe_subscription_id != 'CANCELLED'
                ''', (username,))
            
            rows_affected = cursor.rowcount
            conn.commit()
            conn.close()
            
            if rows_affected > 0:
                # Calculate days remaining
                expires_at = user.get('premium_expires_at')
                days_remaining = "until expiry"
                if expires_at:
                    try:
                        if isinstance(expires_at, str):
                            expiry_date = datetime.fromisoformat(expires_at.replace('Z', '+00:00'))
                        else:
                            expiry_date = expires_at
                        days_remaining = f"until {expiry_date.strftime('%Y-%m-%d')}"
                    except:
                        pass
                
                return True, f"Subscription cancelled successfully. Premium access continues {days_remaining}"
            else:
                return False, "Subscription is already cancelled"
                
        except Exception as e:
            st.write(f"Debug: Error cancelling subscription for {username}: {e}")
            return False, f"Database error: {str(e)}"
    
    def update_premium_status(self, username, is_premium, expires_at=None, subscription_id=None):
        """✅ FIXED: Update user's premium status with proper time calculation for resubscriptions"""
        try:
            # ✅ Get current user data to check for resubscription scenario
            current_user = self.get_user(username)
            
            # ✅ Handle resubscription after cancellation
            if current_user and current_user.get('stripe_subscription_id') == 'CANCELLED' and is_premium:
                st.write("Debug: Handling resubscription after cancellation...")
                
                # ✅ FIXED: Add new time to existing premium time instead of replacing
                if expires_at:
                    try:
                        # Parse the new subscription period from payment handler
                        if isinstance(expires_at, str):
                            new_period_end = datetime.fromisoformat(expires_at.replace('Z', '+00:00'))
                        else:
                            new_period_end = expires_at
                        
                        # Get current expiry date
                        current_expiry = current_user.get('premium_expires_at')
                        if current_expiry:
                            try:
                                if isinstance(current_expiry, str):
                                    current_expiry_date = datetime.fromisoformat(current_expiry.replace('Z', '+00:00'))
                                else:
                                    current_expiry_date = current_expiry
                                
                                # ✅ Calculate new period length from payment
                                payment_period_days = (new_period_end - datetime.now()).days
                                
                                # ✅ Add new period to existing expiry (not current time)
                                final_expiry = current_expiry_date + timedelta(days=payment_period_days)
                                final_expires_at = final_expiry.isoformat()
                                
                                st.write(f"Debug: Current expiry: {current_expiry_date.strftime('%Y-%m-%d')}")
                                st.write(f"Debug: Adding {payment_period_days} days to existing expiry")
                                st.write(f"Debug: New final expiry: {final_expiry.strftime('%Y-%m-%d')}")
                                
                            except Exception as date_error:
                                st.write(f"Debug: Error parsing current expiry: {date_error}")
                                # Fallback: use payment handler expiry directly
                                final_expires_at = new_period_end.isoformat()
                        else:
                            # No current expiry, use payment handler expiry directly
                            final_expires_at = new_period_end.isoformat()
                            st.write("Debug: No current expiry found, using payment expiry directly")
                        
                    except Exception as parse_error:
                        st.write(f"Debug: Error parsing payment expires_at: {parse_error}")
                        # This should rarely happen since payment_handler provides good dates
                        final_expires_at = expires_at
                else:
                    # This should not happen since payment_handler always provides expires_at
                    st.write("Debug: No expires_at provided - this should not happen")
                    final_expires_at = None
            
            # ✅ Handle new subscription (not a resubscription)
            elif is_premium and expires_at:
                final_expires_at = expires_at
            else:
                final_expires_at = expires_at
            
            conn = self.get_connection()
            cursor = conn.cursor()
            
            if self.use_postgres:
                cursor.execute('''
                    UPDATE users 
                    SET is_premium = %s, premium_expires_at = %s, stripe_subscription_id = %s 
                    WHERE username = %s
                ''', (is_premium, final_expires_at, subscription_id, username))
            else:
                cursor.execute('''
                    UPDATE users 
                    SET is_premium = ?, premium_expires_at = ?, stripe_subscription_id = ? 
                    WHERE username = ?
                ''', (is_premium, final_expires_at, subscription_id, username))
            
            rows_affected = cursor.rowcount
            conn.commit()
            conn.close()
            return rows_affected > 0
                
        except Exception as e:
            st.write(f"Debug: Error updating premium status: {e}")
            return False
    
    def check_premium_expiration(self, username):
        """Check if user's premium subscription has expired"""
        try:
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
            return False, "Error"

    # ✅ NEW SUBSCRIPTION MANAGEMENT FUNCTIONS
    
    def check_and_process_expired_subscriptions(self):
        """
        Check for expired subscriptions and process renewals
        This should be called on app startup or user login
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Find users with expired premium that have active Stripe subscriptions
            if self.use_postgres:
                cursor.execute('''
                    SELECT username, premium_expires_at, stripe_subscription_id, email, name
                    FROM users 
                    WHERE is_premium = TRUE 
                    AND premium_expires_at < %s 
                    AND stripe_subscription_id IS NOT NULL 
                    AND stripe_subscription_id != 'CANCELLED'
                ''', (datetime.now(),))
            else:
                cursor.execute('''
                    SELECT username, premium_expires_at, stripe_subscription_id, email, name
                    FROM users 
                    WHERE is_premium = 1 
                    AND premium_expires_at < ? 
                    AND stripe_subscription_id IS NOT NULL 
                    AND stripe_subscription_id != 'CANCELLED'
                ''', (datetime.now(),))
            
            expired_users = cursor.fetchall()
            conn.close()
            
            renewal_results = []
            
            for user_data in expired_users:
                username, old_expiry, subscription_id, email, name = user_data
                
                # Try to process renewal for this user
                renewal_result = self.process_subscription_renewal(username, subscription_id)
                renewal_results.append({
                    'username': username,
                    'result': renewal_result
                })
            
            return renewal_results
            
        except Exception as e:
            st.write(f"Debug: Error checking expired subscriptions: {e}")
            return []
    
    def process_subscription_renewal(self, username, stripe_subscription_id):
        """
        Process renewal for a specific user subscription
        Returns: {'success': bool, 'message': str, 'new_expiry': str}
        """
        try:
            # Import here to avoid circular imports
            import stripe
            stripe.api_key = st.secrets["default"]["STRIPE_SECRET_KEY"]
            
            # Check subscription status in Stripe
            subscription = stripe.Subscription.retrieve(stripe_subscription_id)
            
            if subscription.status == 'active':
                # Subscription is still active in Stripe, extend the user's premium
                
                # Determine renewal period based on subscription interval
                if subscription.plan.interval == 'year':
                    renewal_days = 365
                    plan_type = "Annual"
                elif subscription.plan.interval == 'month':
                    renewal_days = 30
                    plan_type = "Monthly"
                else:
                    renewal_days = 30  # Default fallback
                    plan_type = "Monthly"
                
                # Calculate new expiry date (add renewal period to current time)
                new_expiry = datetime.now() + timedelta(days=renewal_days)
                
                # Update user's premium status
                success = self.update_premium_status(
                    username, 
                    True, 
                    new_expiry.isoformat(), 
                    stripe_subscription_id
                )
                
                if success:
                    st.write(f"Debug: Auto-renewed {username} - {plan_type} subscription extended to {new_expiry.strftime('%Y-%m-%d')}")
                    return {
                        'success': True,
                        'message': f'{plan_type} subscription auto-renewed',
                        'new_expiry': new_expiry.isoformat(),
                        'plan_type': plan_type
                    }
                else:
                    return {
                        'success': False,
                        'message': 'Database update failed',
                        'new_expiry': None
                    }
                    
            elif subscription.status in ['canceled', 'unpaid', 'past_due']:
                # Subscription is no longer active, revoke premium access
                self.update_premium_status(username, False, None, 'CANCELLED')
                
                return {
                    'success': False,
                    'message': f'Subscription {subscription.status} - premium access revoked',
                    'new_expiry': None
                }
            else:
                st.write(f"Debug: Unknown subscription status: {subscription.status}")
                return {
                    'success': False,
                    'message': f'Unknown subscription status: {subscription.status}',
                    'new_expiry': None
                }
                
        except Exception as e:
            st.write(f"Debug: Error processing renewal for {username}: {e}")
            # If we can't reach Stripe, don't revoke access yet
            return {
                'success': False,
                'message': f'Renewal check failed: {str(e)}',
                'new_expiry': None
            }
    
    def get_subscription_status_summary(self):
        """
        Get a summary of all subscription statuses for admin/debugging
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            if self.use_postgres:
                cursor.execute('''
                    SELECT 
                        COUNT(*) as total_users,
                        COUNT(CASE WHEN is_premium = TRUE THEN 1 END) as premium_users,
                        COUNT(CASE WHEN stripe_subscription_id = 'CANCELLED' THEN 1 END) as cancelled_users,
                        COUNT(CASE WHEN is_premium = TRUE AND premium_expires_at < %s THEN 1 END) as expired_users
                    FROM users
                ''', (datetime.now(),))
            else:
                cursor.execute('''
                    SELECT 
                        COUNT(*) as total_users,
                        COUNT(CASE WHEN is_premium = 1 THEN 1 END) as premium_users,
                        COUNT(CASE WHEN stripe_subscription_id = 'CANCELLED' THEN 1 END) as cancelled_users,
                        COUNT(CASE WHEN is_premium = 1 AND premium_expires_at < ? THEN 1 END) as expired_users
                    FROM users
                ''', (datetime.now(),))
            
            result = cursor.fetchone()
            conn.close()
            
            return {
                'total_users': result[0],
                'premium_users': result[1], 
                'cancelled_users': result[2],
                'expired_users': result[3]
            }
            
        except Exception as e:
            st.write(f"Debug: Error getting subscription summary: {e}")
            return {}
    
    # ✅ TESTING FUNCTIONS
    
    def create_test_expiration(self, username, minutes_from_now=5):
        """
        FOR TESTING ONLY: Set a user's premium to expire in X minutes
        This allows testing the renewal system without waiting 30 days
        """
        try:
            test_expiry = datetime.now() + timedelta(minutes=minutes_from_now)
            
            conn = self.get_connection()
            cursor = conn.cursor()
            
            if self.use_postgres:
                cursor.execute('''
                    UPDATE users 
                    SET premium_expires_at = %s 
                    WHERE username = %s
                ''', (test_expiry, username))
            else:
                cursor.execute('''
                    UPDATE users 
                    SET premium_expires_at = ? 
                    WHERE username = ?
                ''', (test_expiry, username))
            
            conn.commit()
            conn.close()
            
            st.write(f"⚠️ TEST MODE: Set {username} premium to expire at {test_expiry.strftime('%Y-%m-%d %H:%M:%S')}")
            return True
            
        except Exception as e:
            st.write(f"Debug: Error creating test expiration: {e}")
            return False
