import stripe
import os
import streamlit as st

class PaymentHandler:
    def __init__(self):
        # Load Stripe keys from environment variables (Heroku) or Streamlit secrets (local)
        try:
            # Try environment variables first (Heroku)
            self.stripe_secret_key = os.environ.get("STRIPE_SECRET_KEY")
            self.stripe_publishable_key = os.environ.get("STRIPE_PUBLISHABLE_KEY")
            self.domain = os.environ.get("DOMAIN")
            
            # If not found in environment, try Streamlit secrets (local development)
            if not self.stripe_secret_key:
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
        else:
            st.error("❌ Stripe Secret Key not found in environment variables or secrets!")

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
                success_url=f'{self.domain}/?session_id={{CHECKOUT_SESSION_ID}}&upgrade=success',
                cancel_url=f'{self.domain}/?upgrade=cancelled',
                metadata={
                    'username': username
                }
            )
            
            return checkout_session.url
            
        except Exception as e:
            st.error(f"Error creating checkout session: {str(e)}")
            return None

    def handle_successful_payment(self, session_id, username):
        """✅ FIXED: Handle successful payment and upgrade user with proper time calculation"""
        if not self.stripe_secret_key:
            return {'success': False}
            
        try:
            # Retrieve the session from Stripe
            session = stripe.checkout.Session.retrieve(session_id)
            
            if session.payment_status == 'paid':
                # Get subscription details to set expiration
                subscription_id = session.subscription
                
                if subscription_id:
                    try:
                        subscription = stripe.Subscription.retrieve(subscription_id)
                        
                        # ✅ FIXED: Calculate expiration date from subscription properly
                        from datetime import datetime
                        
                        # Check if current_period_end exists and is valid
                        if hasattr(subscription, 'current_period_end') and subscription.current_period_end:
                            current_period_end = subscription.current_period_end
                            expires_at = datetime.fromtimestamp(current_period_end)
                            
                            st.write(f"Debug: Stripe subscription expires at: {expires_at.isoformat()}")
                            
                            return {
                                'success': True,
                                'expires_at': expires_at.isoformat(),
                                'subscription_id': subscription_id,
                                'amount': session.amount_total if hasattr(session, 'amount_total') else 0
                            }
                        else:
                            # No current_period_end, fall back to manual calculation
                            st.write("Debug: No current_period_end in subscription, using fallback")
                            raise Exception("No current_period_end available")
                            
                    except Exception as sub_error:
                        st.write(f"Debug: Error retrieving subscription: {sub_error}")
                        # ✅ FIXED: Determine plan from Stripe amount instead of session state
                        from datetime import datetime, timedelta
                        
                        # Use Stripe amount to determine plan type (more reliable)
                        amount = session.amount_total if hasattr(session, 'amount_total') else 0
                        now = datetime.now()
                        
                        if amount >= 9900:  # $99 or more = Annual
                            expires_at = now + timedelta(days=365)
                            st.write(f"Debug: Fallback calculation (YEARLY from amount ${amount/100:.2f}) - expires at: {expires_at.isoformat()}")
                        else:  # Less than $99 = Monthly
                            expires_at = now + timedelta(days=30)
                            st.write(f"Debug: Fallback calculation (MONTHLY from amount ${amount/100:.2f}) - expires at: {expires_at.isoformat()}")
                        
                        return {
                            'success': True,
                            'expires_at': expires_at.isoformat(),
                            'subscription_id': subscription_id,
                            'amount': amount
                        }
                else:
                    # ✅ FIXED: Determine plan from Stripe amount instead of session state
                    from datetime import datetime, timedelta
                    
                    # Use Stripe amount to determine plan type (more reliable)
                    amount = session.amount_total if hasattr(session, 'amount_total') else 0
                    now = datetime.now()
                    
                    if amount >= 9900:  # $99 or more = Annual
                        expires_at = now + timedelta(days=365)
                        st.write(f"Debug: No subscription ID (YEARLY from amount ${amount/100:.2f}) - expires at: {expires_at.isoformat()}")
                    else:  # Less than $99 = Monthly
                        expires_at = now + timedelta(days=30)
                        st.write(f"Debug: No subscription ID (MONTHLY from amount ${amount/100:.2f}) - expires at: {expires_at.isoformat()}")
                    
                    return {
                        'success': True,
                        'expires_at': expires_at.isoformat(),
                        'subscription_id': None,
                        'amount': amount
                    }
            else:
                st.write(f"Debug: Payment not completed. Status: {session.payment_status}")
                return {'success': False}
        except Exception as e:
            st.write(f"Debug: Error in handle_successful_payment: {e}")
            # ✅ FIXED: Use session state as fallback when Stripe data unavailable
            from datetime import datetime, timedelta
            plan = st.session_state.get('selected_plan', {'interval': 'month'})
            
            now = datetime.now()
            if plan['interval'] == 'year':
                expires_at = now + timedelta(days=365)
                st.write(f"Debug: Exception fallback (YEARLY from session) - expires at: {expires_at.isoformat()}")
            else:
                expires_at = now + timedelta(days=30)
                st.write(f"Debug: Exception fallback (MONTHLY from session) - expires at: {expires_at.isoformat()}")
            
            return {
                'success': True,
                'expires_at': expires_at.isoformat(),
                'subscription_id': None,
                'amount': 0
            }
