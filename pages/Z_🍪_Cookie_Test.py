import streamlit as st

# Page config
st.set_page_config(page_title="Cookie Test", page_icon="🍪", layout="wide")

st.title("🍪 Cookie Controller Test")
st.write("This page tests if streamlit-cookies-controller is working properly.")

try:
    from streamlit_cookies_controller import CookieController
    cookie_controller = CookieController()
    
    st.success("✅ CookieController imported successfully!")
    
    # Test setting a cookie
    st.subheader("1. Test Setting Cookie")
    col1, col2 = st.columns(2)
    
    with col1:
        test_value = st.text_input("Cookie Value", value="test_value_123")
        if st.button("Set Test Cookie"):
            try:
                cookie_controller.set("test_cookie", test_value, max_age=3600)
                st.success(f"✅ Set cookie 'test_cookie' = '{test_value}'")
            except Exception as e:
                st.error(f"❌ Error setting cookie: {e}")
    
    # Test getting the cookie
    st.subheader("2. Test Reading Cookie")
    if st.button("Read Test Cookie"):
        try:
            value = cookie_controller.get("test_cookie")
            if value:
                st.success(f"✅ Read cookie 'test_cookie' = '{value}'")
            else:
                st.warning("⚠️ Cookie 'test_cookie' not found")
        except Exception as e:
            st.error(f"❌ Error reading cookie: {e}")
    
    # Test getting all cookies
    st.subheader("3. All Cookies")
    if st.button("Show All Cookies"):
        try:
            all_cookies = cookie_controller.getAll()
            if all_cookies:
                st.json(all_cookies)
            else:
                st.info("No cookies found")
        except Exception as e:
            st.error(f"❌ Error getting all cookies: {e}")
    
    # Test removing cookie
    st.subheader("4. Remove Cookie")
    if st.button("Remove Test Cookie"):
        try:
            cookie_controller.remove("test_cookie")
            st.success("✅ Removed cookie 'test_cookie'")
        except Exception as e:
            st.error(f"❌ Error removing cookie: {e}")
    
    # Check for auth cookie
    st.subheader("5. Check Auth Cookie")
    if st.button("Check Kaspa Auth Cookie"):
        try:
            auth_cookie = cookie_controller.get("kaspa_auth_token")
            if auth_cookie:
                st.success(f"✅ Found auth cookie: {auth_cookie[:50]}...")
            else:
                st.warning("⚠️ No auth cookie found")
        except Exception as e:
            st.error(f"❌ Error checking auth cookie: {e}")

except ImportError as e:
    st.error(f"❌ Failed to import CookieController: {e}")
    st.info("Make sure streamlit-cookies-controller is installed in requirements.txt")

except Exception as e:
    st.error(f"❌ Unexpected error: {e}")
    import traceback
    st.text(traceback.format_exc())

# Navigation
st.markdown("---")
if st.button("🏠 Back to Home"):
    st.switch_page("Home.py")
