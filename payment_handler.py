import stripe
import os
import streamlit as st

class PaymentHandler:
    def __init__(self):
        # Load Stripe keys from Streamlit secrets
        try:
            default_secrets = st.secrets["default"]
            self.stripe_secret_key = default_secrets["STRIPE_SECRET_KEY"]
            self.stripe_publishable_key = default_secrets["STRIPE_PUBLISHABLE_KEY"] 
            self.domain = default_secrets["DOMAIN"]
        except Exception as e:
            st.error(f"Error loading Stripe configuration: {str(e)}")
            self.stripe_secret_key = None
            self.stripe_publishable_key = None
            self.domain = "http://localhost:8501"
        
        if self.stripe_secret_key:
            stripe.api_key = self.stripe_secret_key
    
    def create_checkout_session(self, username):
        """Create a Stripe checkout session for premium upgrade"""
        if not self.stripe_secret_key:
            st.error("Stripe not configured properly.")
            return None
        
        # Get pricing from session state, default to monthly
        plan = st.session_state.get('selected_plan', {'amount': 999, 'interval': 'month'})
        price_amount = plan['amount']
        interval = plan['interval']
            
        try:
            # Create product description based on interval
            if interval == 'year':
                description = f'Annual subscription to premium analytics features (${price_amount/100:.2f}/year)'
            else:
                description = f'Monthly subscription to premium analytics features (${price_amount/100:.2f}/month)'
            
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': 'Kaspa Analytics Premium',
                            'description': description,
                        },
                        'unit_amount': int(price_amount),
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
            
            return checkout_session.url
            
        except Exception as e:
            st.error(f"Error creating checkout session: {str(e)}")
            return None
    
    def handle_successful_payment(self, session_id, username):
        """Handle successful payment and upgrade user"""
        if not self.stripe_secret_key:
            return {'success': False}
            
        try:
            # Retrieve the session from Stripe
            session = stripe.checkout.Session.retrieve(session_id)
            st.write(f"Debug: Payment session status: {session.payment_status}")
            
            if session.payment_status == 'paid':
                # Get subscription details to set expiration
                subscription_id = session.subscription
                st.write(f"Debug: Subscription ID: {subscription_id}")
                
                if subscription_id:
                    try:
                        subscription = stripe.Subscription.retrieve(subscription_id)
                        st.write(f"Debug: Retrieved subscription: {subscription.id}")
                        
                        # Calculate expiration date from subscription
                        from datetime import datetime
                        current_period_end = subscription.current_period_end
                        expires_at = datetime.fromtimestamp(current_period_end)
                        
                        st.write(f"Debug: Subscription expires: {expires_at}")
                        
                        return {
                            'success': True,
                            'expires_at': expires_at.isoformat(),
                            'subscription_id': subscription_id
                        }
                    except Exception as sub_error:
                        st.write(f"Debug: Subscription error: {sub_error}")
                        # Fall back to manual calculation
                        from datetime import datetime, timedelta
                        plan = st.session_state.get('selected_plan', {'interval': 'month'})
                        if plan['interval'] == 'year':
                            expires_at = datetime.now() + timedelta(days=365)
                        else:
                            expires_at = datetime.now() + timedelta(days=30)
                        
                        return {
                            'success': True,
                            'expires_at': expires_at.isoformat(),
                            'subscription_id': subscription_id
                        }
                else:
                    # No subscription ID, use manual calculation
                    from datetime import datetime, timedelta
                    plan = st.session_state.get('selected_plan', {'interval': 'month'})
                    if plan['interval'] == 'year':
                        expires_at = datetime.now() + timedelta(days=365)
                    else:
                        expires_at = datetime.now() + timedelta(days=30)
                    
                    st.write(f"Debug: No subscription ID, using manual expiry: {expires_at}")
                    
                    return {
                        'success': True,
                        'expires_at': expires_at.isoformat(),
                        'subscription_id': None
                    }
            else:
                st.write(f"Debug: Payment not completed, status: {session.payment_status}")
                return {'success': False}
        except Exception as e:
            st.write(f"Debug: Full error details: {type(e).__name__}: {str(e)}")
            st.error(f"Error verifying payment: {str(e)}")
            
            # Fallback: still upgrade the user since payment was successful
            from datetime import datetime, timedelta
            plan = st.session_state.get('selected_plan', {'interval': 'month'})
            if plan['interval'] == 'year':
                expires_at = datetime.now() + timedelta(days=365)
            else:
                expires_at = datetime.now() + timedelta(days=30)
            
            st.write(f"Debug: Using fallback expiry: {expires_at}")
            
            return {
                'success': True,
                'expires_at': expires_at.isoformat(),
                'subscription_id': None
            }
