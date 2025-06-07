import stripe
import os
import streamlit as st

class PaymentHandler:
    def __init__(self):
        # Load Stripe keys from Streamlit secrets or environment variables
        try:
            # Try Streamlit secrets first (for Streamlit Cloud)
            self.stripe_secret_key = st.secrets.get("STRIPE_SECRET_KEY") or os.getenv('STRIPE_SECRET_KEY')
            self.stripe_publishable_key = st.secrets.get("STRIPE_PUBLISHABLE_KEY") or os.getenv('STRIPE_PUBLISHABLE_KEY')
            self.domain = st.secrets.get("DOMAIN", "http://localhost:8501") or os.getenv('DOMAIN', 'http://localhost:8501')
        except:
            # Fallback to environment variables (for local development)
            self.stripe_secret_key = os.getenv('STRIPE_SECRET_KEY')
            self.stripe_publishable_key = os.getenv('STRIPE_PUBLISHABLE_KEY')
            self.domain = os.getenv('DOMAIN', 'http://localhost:8501')
        
        if not self.stripe_secret_key:
            st.error("Stripe secret key not found. Please set STRIPE_SECRET_KEY in Streamlit Cloud secrets or .env file")
            return
            
        stripe.api_key = self.stripe_secret_key
    
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
