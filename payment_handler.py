import stripe
import os
import streamlit as st

class PaymentHandler:
    def __init__(self):
        # Debug: Check if secrets are available
        st.write("Debug: Checking Streamlit secrets...")
        try:
            st.write(f"Debug: Available secrets keys: {list(st.secrets.keys())}")
            if 'default' in st.secrets:
                st.write(f"Debug: Keys in default section: {list(st.secrets['default'].keys())}")
        except:
            st.write("Debug: No secrets available")
            
        # Load Stripe keys from Streamlit secrets or environment variables
        try:
            # Access secrets through the 'default' section
            self.stripe_secret_key = st.secrets["default"]["STRIPE_SECRET_KEY"]
            self.stripe_publishable_key = st.secrets["default"]["STRIPE_PUBLISHABLE_KEY"] 
            self.domain = st.secrets["default"]["DOMAIN"]
            
            # Debug: Show what keys we loaded (partially masked)
            if self.stripe_secret_key:
                masked_key = self.stripe_secret_key[:12] + "***" + self.stripe_secret_key[-4:]
                st.write(f"Debug: Loaded secret key: {masked_key}")
                st.write(f"Debug: Key length: {len(self.stripe_secret_key)}")
                st.write(f"Debug: Key starts with: {self.stripe_secret_key[:10]}")
            else:
                st.write("Debug: Secret key is empty")
                
        except KeyError as e:
            st.write(f"Debug: Secret key not found: {e}")
            # Fallback to environment variables (for local development)
            self.stripe_secret_key = os.getenv('STRIPE_SECRET_KEY')
            self.stripe_publishable_key = os.getenv('STRIPE_PUBLISHABLE_KEY')
            self.domain = os.getenv('DOMAIN', 'http://localhost:8501')
        except Exception as e:
            st.write(f"Debug: Error accessing secrets: {e}")
            # Fallback to environment variables (for local development)
            self.stripe_secret_key = os.getenv('STRIPE_SECRET_KEY')
            self.stripe_publishable_key = os.getenv('STRIPE_PUBLISHABLE_KEY')
            self.domain = os.getenv('DOMAIN', 'http://localhost:8501')
        
        if not self.stripe_secret_key:
            st.error("Stripe secret key not found. Please set STRIPE_SECRET_KEY in Streamlit Cloud secrets")
            return
        
        # Set the Stripe API key
        stripe.api_key = self.stripe_secret_key
        st.write(f"Debug: Stripe API key set successfully")
    
    def create_checkout_session(self, username):
        """Create a Stripe checkout session for premium upgrade"""
        if not self.stripe_secret_key:
            st.error("Stripe not configured. Please add your API keys to Streamlit Cloud secrets.")
            return None
        
        # Get pricing from session state, default to monthly
        plan = st.session_state.get('selected_plan', {'amount': 999, 'interval': 'month'})
        price_amount = plan['amount']
        interval = plan['interval']
        
        # Debug logging
        st.write(f"Debug: Creating session for {username}, ${price_amount/100:.2f}/{interval}")
            
        try:
            # Create product description based on interval
            if interval == 'year':
                description = f'Annual subscription to premium analytics features (${price_amount/100:.2f}/year)'
            else:
                description = f'Monthly subscription to premium analytics features (${price_amount/100:.2f}/month)'
            
            st.write(f"Debug: Creating Stripe session with amount {price_amount}")
            
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': 'Kaspa Analytics Premium',
                            'description': description,
                        },
                        'unit_amount': int(price_amount),  # Ensure it's an integer
                        'recurring': {
                            'interval': interval,
                        },
                    },
                    'quantity': 1,
                }],
                mode='subscription',
                success_url=f'{self.domain}?session_id={{CHECKOUT_SESSION_ID}}&upgrade=success',
                cancel_url=f'{self.domain}?upgrade=cancelled',
                metadata={
                    'username': username
                }
            )
            
            st.write(f"Debug: Session created successfully: {checkout_session.id}")
            return checkout_session.url
            
        except stripe.error.AuthenticationError as e:
            st.error(f"Stripe authentication error: {str(e)}")
            st.error("Please check your STRIPE_SECRET_KEY in Streamlit Cloud secrets")
            return None
        except Exception as e:
            st.error(f"Error creating checkout session: {str(e)}")
            st.write(f"Debug: Full error details: {type(e).__name__}: {str(e)}")
            return None
    
    def handle_successful_payment(self, session_id, username):
        """Handle successful payment and upgrade user"""
        try:
            session = stripe.checkout.Session.retrieve(session_id)
            if session.payment_status == 'paid':
                # Upgrade user to premium
                from database import Database
                db = Database()
                db.update_premium_status(username, True)
                return True
        except Exception as e:
            st.error(f"Error processing payment: {str(e)}")
        return False
