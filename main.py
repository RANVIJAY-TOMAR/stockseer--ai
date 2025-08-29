import streamlit as st
from auth_utils import validate_session, logout_user
from landing_page import render_landing_page
import os

# Page configuration
st.set_page_config(
    page_title="StockSeer.AI - AI-Powered Stock Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    """Main application entry point"""
    
    # Initialize session state
    if 'session_token' not in st.session_state:
        st.session_state.session_token = None
    if 'user_info' not in st.session_state:
        st.session_state.user_info = None
    
    # Check if user is authenticated
    if st.session_state.session_token:
        is_valid, user_info = validate_session(st.session_state.session_token)
        if is_valid:
            st.session_state.user_info = user_info
            # User is authenticated, show main app
            show_main_app()
        else:
            # Session expired or invalid
            st.session_state.session_token = None
            st.session_state.user_info = None
            st.warning("Session expired. Please login again.")
            render_landing_page()
    else:
        # No session token, show landing page
        render_landing_page()

def show_main_app():
    """Show the main application after authentication"""
    
    # Add logout button to sidebar
    with st.sidebar:
        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True):
            if st.session_state.session_token:
                logout_user(st.session_state.session_token)
            st.session_state.session_token = None
            st.session_state.user_info = None
            st.rerun()
    
    # Show user info in sidebar
    if st.session_state.user_info:
        st.sidebar.markdown(f"""
        <div style="padding: 1rem; background: rgba(57, 255, 20, 0.1); border-radius: 10px; margin-bottom: 1rem;">
            <h4 style="color: #39ff14; margin-bottom: 0.5rem;">👤 Welcome!</h4>
            <p style="color: #e0e0e0; margin: 0;"><strong>{st.session_state.user_info.get('full_name', st.session_state.user_info['username'])}</strong></p>
            <p style="color: #888; font-size: 0.9rem; margin: 0;">{st.session_state.user_info['email']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Import and run the main app
    try:
        # Import the main app module
        import app
        # The app.py will run automatically when imported
    except ImportError as e:
        st.error(f"Error loading main application: {str(e)}")
        st.info("Please ensure app.py exists and is properly configured.")

if __name__ == "__main__":
    main()
