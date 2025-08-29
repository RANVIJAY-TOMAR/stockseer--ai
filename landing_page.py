import streamlit as st
import streamlit.components.v1 as components
from auth_utils import create_user, authenticate_user, validate_session
import re

def render_landing_page():
    """Render the main landing page with authentication"""
    
    # Custom CSS for landing page
    st.markdown("""
        <style>
        /* Landing Page Styles */
        .landing-container {
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%);
            min-height: 100vh;
            color: white;
        }
        
        .hero-section {
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 50%, #2a2a2a 100%);
            padding: 4rem 2rem;
            text-align: center;
            position: relative;
            overflow: hidden;
        }
        
        .hero-section::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grid" width="10" height="10" patternUnits="userSpaceOnUse"><path d="M 10 0 L 0 0 0 10" fill="none" stroke="rgba(57,255,20,0.1)" stroke-width="0.5"/></pattern></defs><rect width="100" height="100" fill="url(%23grid)"/></svg>');
            opacity: 0.3;
        }
        
        .hero-content {
            position: relative;
            z-index: 2;
        }
        
        .hero-title {
            font-size: 4rem;
            font-weight: 800;
            background: linear-gradient(45deg, #39ff14, #00ff88);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 1rem;
            text-shadow: 0 4px 20px rgba(57, 255, 20, 0.3);
        }
        
        .hero-subtitle {
            font-size: 1.5rem;
            color: #b0b0b0;
            margin-bottom: 2rem;
            max-width: 600px;
            margin-left: auto;
            margin-right: auto;
        }
        
        .auth-container {
            background: rgba(26, 26, 26, 0.9);
            border-radius: 20px;
            padding: 2rem;
            margin: 2rem auto;
            max-width: 400px;
            border: 1px solid rgba(57, 255, 20, 0.2);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        }
        
        .auth-tabs {
            display: flex;
            margin-bottom: 2rem;
            border-radius: 10px;
            overflow: hidden;
            background: rgba(0, 0, 0, 0.3);
        }
        
        .auth-tab {
            flex: 1;
            padding: 1rem;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease;
            border: none;
            background: transparent;
            color: #888;
        }
        
        .auth-tab.active {
            background: #39ff14;
            color: #000;
            font-weight: bold;
        }
        
        .auth-form {
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }
        
        .form-group {
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }
        
        .form-label {
            color: #b0b0b0;
            font-weight: 500;
        }
        
        .form-input {
            padding: 0.75rem;
            border: 1px solid rgba(57, 255, 20, 0.3);
            border-radius: 8px;
            background: rgba(0, 0, 0, 0.3);
            color: white;
            font-size: 1rem;
        }
        
        .form-input:focus {
            outline: none;
            border-color: #39ff14;
            box-shadow: 0 0 10px rgba(57, 255, 20, 0.2);
        }
        
        .auth-button {
            background: linear-gradient(45deg, #39ff14, #00ff88);
            color: #000;
            border: none;
            padding: 1rem;
            border-radius: 8px;
            font-size: 1.1rem;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
            margin-top: 1rem;
        }
        
        .auth-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(57, 255, 20, 0.3);
        }
        
        .features-section {
            padding: 4rem 2rem;
            background: rgba(0, 0, 0, 0.5);
        }
        
        .features-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .feature-card {
            background: rgba(26, 26, 26, 0.9);
            border-radius: 15px;
            padding: 2rem;
            border: 1px solid rgba(57, 255, 20, 0.2);
            transition: all 0.3s ease;
        }
        
        .feature-card:hover {
            transform: translateY(-5px);
            border-color: #39ff14;
            box-shadow: 0 10px 30px rgba(57, 255, 20, 0.1);
        }
        
        .feature-icon {
            font-size: 3rem;
            margin-bottom: 1rem;
        }
        
        .feature-title {
            font-size: 1.5rem;
            font-weight: bold;
            margin-bottom: 1rem;
            color: #39ff14;
        }
        
        .feature-description {
            color: #b0b0b0;
            line-height: 1.6;
        }
        
        .stats-section {
            padding: 3rem 2rem;
            background: linear-gradient(135deg, #1a1a1a 0%, #2a2a2a 100%);
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 2rem;
            max-width: 800px;
            margin: 0 auto;
        }
        
        .stat-item {
            text-align: center;
            padding: 2rem;
            background: rgba(0, 0, 0, 0.3);
            border-radius: 15px;
            border: 1px solid rgba(57, 255, 20, 0.2);
        }
        
        .stat-number {
            font-size: 3rem;
            font-weight: bold;
            color: #39ff14;
            margin-bottom: 0.5rem;
        }
        
        .stat-label {
            color: #b0b0b0;
            font-size: 1.1rem;
        }
        
        .footer {
            background: #0a0a0a;
            padding: 2rem;
            text-align: center;
            border-top: 1px solid rgba(57, 255, 20, 0.2);
        }
        
        .footer-content {
            max-width: 600px;
            margin: 0 auto;
            color: #888;
        }
        
        @media (max-width: 768px) {
            .hero-title {
                font-size: 2.5rem;
            }
            
            .hero-subtitle {
                font-size: 1.2rem;
            }
            
            .auth-container {
                margin: 1rem;
                padding: 1.5rem;
            }
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Check if user is already logged in
    if 'session_token' in st.session_state:
        is_valid, user_info = validate_session(st.session_state.session_token)
        if is_valid:
            # Redirect to main app
            st.success(f"Welcome back, {user_info['username']}!")
            st.button("Continue to Dashboard", on_click=lambda: st.switch_page("app.py"))
            return
    
    # Landing page content
    st.markdown("""
        <div class="landing-container">
            <div class="hero-section">
                <div class="hero-content">
                    <h1 class="hero-title">StockSeer.AI</h1>
                    <p class="hero-subtitle">
                        Your AI-powered companion for intelligent stock analysis, 
                        predictive insights, and confident investment decisions
                    </p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Authentication Section
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
            <div class="auth-container">
                <div class="auth-tabs">
                    <button class="auth-tab active" onclick="showLogin()">Login</button>
                    <button class="auth-tab" onclick="showSignup()">Sign Up</button>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Authentication Forms
        auth_tab = st.radio("", ["Login", "Sign Up"], horizontal=True, label_visibility="collapsed")
        
        if auth_tab == "Login":
            render_login_form()
        else:
            render_signup_form()
    
    # Features Section
    st.markdown("""
        <div class="features-section">
            <h2 style="text-align: center; font-size: 2.5rem; margin-bottom: 3rem; color: #39ff14;">
                Why Choose StockSeer.AI?
            </h2>
            <div class="features-grid">
                <div class="feature-card">
                    <div class="feature-icon">🤖</div>
                    <h3 class="feature-title">AI-Powered Analysis</h3>
                    <p class="feature-description">
                        Advanced machine learning algorithms analyze market patterns, 
                        news sentiment, and technical indicators to provide intelligent insights.
                    </p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">📊</div>
                    <h3 class="feature-title">Global Market Coverage</h3>
                    <p class="feature-description">
                        Access real-time data from 30+ global markets including US, 
                        India, Europe, Asia, and emerging markets.
                    </p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">🔮</div>
                    <h3 class="feature-title">Future Predictions</h3>
                    <p class="feature-description">
                        Get AI-powered price predictions for 3 months to 5 years 
                        with confidence levels and risk assessments.
                    </p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">📰</div>
                    <h3 class="feature-title">Real-time News Analysis</h3>
                    <p class="feature-description">
                        Comprehensive news aggregation from Bloomberg, CNBC, 
                        MarketWatch, and global sources with sentiment analysis.
                    </p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">🎯</div>
                    <h3 class="feature-title">Personalized Insights</h3>
                    <p class="feature-description">
                        Tailored investment recommendations based on your risk 
                        profile, goals, and market preferences.
                    </p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">⚡</div>
                    <h3 class="feature-title">Instant Alerts</h3>
                    <p class="feature-description">
                        Set up custom alerts for price movements, news events, 
                        and technical signals to never miss opportunities.
                    </p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Stats Section
    from auth_utils import get_user_stats
    stats = get_user_stats()
    
    st.markdown(f"""
        <div class="stats-section">
            <h2 style="text-align: center; font-size: 2.5rem; margin-bottom: 3rem; color: #39ff14;">
                Trusted by Investors Worldwide
            </h2>
            <div class="stats-grid">
                <div class="stat-item">
                    <div class="stat-number">{stats.get('total_users', 0)}</div>
                    <div class="stat-label">Active Users</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">{stats.get('new_users_month', 0)}</div>
                    <div class="stat-label">New This Month</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">30+</div>
                    <div class="stat-label">Global Markets</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">99.9%</div>
                    <div class="stat-label">Uptime</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
        <div class="footer">
            <div class="footer-content">
                <p>&copy; 2024 StockSeer.AI. All rights reserved.</p>
                <p>Empowering investors with AI-driven insights and intelligent analysis.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

def render_login_form():
    """Render the login form"""
    st.markdown("### 🔐 Login to Your Account")
    
    with st.form("login_form"):
        username_or_email = st.text_input("Username or Email", placeholder="Enter your username or email")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        
        col1, col2 = st.columns([1, 1])
        with col1:
            remember_me = st.checkbox("Remember me")
        with col2:
            st.markdown("[Forgot Password?](#)")
        
        submit_button = st.form_submit_button("Login", type="primary")
        
        if submit_button:
            if username_or_email and password:
                success, result = authenticate_user(username_or_email, password)
                if success:
                    st.session_state.session_token = result['session_token']
                    st.session_state.user_info = result
                    st.success("Login successful! Redirecting...")
                    st.rerun()
                else:
                    st.error(result)
            else:
                st.error("Please fill in all fields")

def render_signup_form():
    """Render the signup form"""
    st.markdown("### 🚀 Create Your Account")
    
    with st.form("signup_form"):
        full_name = st.text_input("Full Name", placeholder="Enter your full name")
        username = st.text_input("Username", placeholder="Choose a unique username")
        email = st.text_input("Email", placeholder="Enter your email address")
        password = st.text_input("Password", type="password", placeholder="Create a strong password")
        confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
        
        # Password strength indicator
        if password:
            strength = check_password_strength(password)
            st.markdown(f"Password Strength: {strength}")
        
        terms = st.checkbox("I agree to the Terms of Service and Privacy Policy")
        
        submit_button = st.form_submit_button("Create Account", type="primary")
        
        if submit_button:
            if not all([full_name, username, email, password, confirm_password]):
                st.error("Please fill in all fields")
            elif password != confirm_password:
                st.error("Passwords do not match")
            elif not terms:
                st.error("Please agree to the terms and conditions")
            elif not is_valid_email(email):
                st.error("Please enter a valid email address")
            elif len(password) < 8:
                st.error("Password must be at least 8 characters long")
            else:
                success, result = create_user(username, email, password, full_name)
                if success:
                    st.success("Account created successfully! Please login.")
                else:
                    st.error(result)

def check_password_strength(password):
    """Check password strength and return indicator"""
    score = 0
    feedback = []
    
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("At least 8 characters")
    
    if re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("Lowercase letter")
    
    if re.search(r"[A-Z]", password):
        score += 1
    else:
        feedback.append("Uppercase letter")
    
    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("Number")
    
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 1
    else:
        feedback.append("Special character")
    
    if score <= 2:
        return "🟥 Weak"
    elif score <= 3:
        return "🟨 Fair"
    elif score <= 4:
        return "🟩 Good"
    else:
        return "🟦 Strong"

def is_valid_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

if __name__ == "__main__":
    render_landing_page()
