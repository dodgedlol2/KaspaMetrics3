import stripe
import os
import streamlit as st

class PaymentHandler:
    def __init__(self):
        # For testing, use Stripe test keys
        # Get these from your Stripe dashboard
        self.stripe_secret_key = os.getenv('STRIPE_SECRET_KEY', 'sk_test_your_test_key_here')
        self.stripe_publishable_key = os.getenv('STRIPE_PUBLISHABLE_KEY', 'pk_test_your_test_key_here')
        stripe.api_key = self.stripe_secret_key
        
        # Your domain for redirects
        self.domain = os.getenv('DOMAIN', 'http://localhost:8501')
    
    def create_checkout_session(self, username):
        """Create a Stripe checkout session for premium upgrade"""
        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': 'Kaspa Analytics Premium',
                            'description': 'Monthly subscription to premium analytics features',
                        },
                        'unit_amount': 999,  # $9.99 in cents
                        'recurring': {
                            'interval': 'month',
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
            return checkout_session.url
        except Exception as e:
            st.error(f"Error creating checkout session: {str(e)}")
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
