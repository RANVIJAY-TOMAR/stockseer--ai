import streamlit as st
import hashlib
import sqlite3
import os
from datetime import datetime, timedelta
import json

# Database setup
DB_PATH = "users.db"

def init_database():
    """Initialize the SQLite database for user management"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            full_name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP,
            is_active BOOLEAN DEFAULT 1,
            subscription_tier TEXT DEFAULT 'free',
            preferences TEXT DEFAULT '{}'
        )
    ''')
    
    # Create sessions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            session_token TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hashed):
    """Verify password against hash"""
    return hash_password(password) == hashed

def create_user(username, email, password, full_name=""):
    """Create a new user account"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Check if username or email already exists
        cursor.execute("SELECT id FROM users WHERE username = ? OR email = ?", (username, email))
        if cursor.fetchone():
            return False, "Username or email already exists"
        
        # Create new user
        password_hash = hash_password(password)
        cursor.execute('''
            INSERT INTO users (username, email, password_hash, full_name)
            VALUES (?, ?, ?, ?)
        ''', (username, email, password_hash, full_name))
        
        conn.commit()
        conn.close()
        return True, "Account created successfully"
        
    except Exception as e:
        return False, f"Error creating account: {str(e)}"

def authenticate_user(username_or_email, password):
    """Authenticate user login"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Check if input is email or username
        if '@' in username_or_email:
            cursor.execute("SELECT id, username, password_hash FROM users WHERE email = ? AND is_active = 1", (username_or_email,))
        else:
            cursor.execute("SELECT id, username, password_hash FROM users WHERE username = ? AND is_active = 1", (username_or_email,))
        
        user = cursor.fetchone()
        
        if user and verify_password(password, user[2]):
            # Update last login
            cursor.execute("UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?", (user[0],))
            
            # Create session
            session_token = create_session(user[0])
            
            conn.commit()
            conn.close()
            
            return True, {
                'user_id': user[0],
                'username': user[1],
                'session_token': session_token
            }
        else:
            conn.close()
            return False, "Invalid credentials"
            
    except Exception as e:
        return False, f"Authentication error: {str(e)}"

def create_session(user_id):
    """Create a new session for user"""
    import secrets
    session_token = secrets.token_urlsafe(32)
    expires_at = datetime.now() + timedelta(days=30)  # 30 days session
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO sessions (user_id, session_token, expires_at)
        VALUES (?, ?, ?)
    ''', (user_id, session_token, expires_at))
    
    conn.commit()
    conn.close()
    
    return session_token

def validate_session(session_token):
    """Validate session token and return user info"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT u.id, u.username, u.email, u.full_name, u.subscription_tier, u.preferences
            FROM users u
            JOIN sessions s ON u.id = s.user_id
            WHERE s.session_token = ? AND s.expires_at > CURRENT_TIMESTAMP AND u.is_active = 1
        ''', (session_token,))
        
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return True, {
                'user_id': user[0],
                'username': user[1],
                'email': user[2],
                'full_name': user[3],
                'subscription_tier': user[4],
                'preferences': json.loads(user[5]) if user[5] else {}
            }
        else:
            return False, "Invalid or expired session"
            
    except Exception as e:
        return False, f"Session validation error: {str(e)}"

def logout_user(session_token):
    """Logout user by removing session"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM sessions WHERE session_token = ?", (session_token,))
        
        conn.commit()
        conn.close()
        
        return True, "Logged out successfully"
        
    except Exception as e:
        return False, f"Logout error: {str(e)}"

def update_user_preferences(user_id, preferences):
    """Update user preferences"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("UPDATE users SET preferences = ? WHERE id = ?", (json.dumps(preferences), user_id))
        
        conn.commit()
        conn.close()
        
        return True, "Preferences updated"
        
    except Exception as e:
        return False, f"Error updating preferences: {str(e)}"

def get_user_stats():
    """Get user statistics"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Total users
        cursor.execute("SELECT COUNT(*) FROM users WHERE is_active = 1")
        total_users = cursor.fetchone()[0]
        
        # New users this month
        cursor.execute("SELECT COUNT(*) FROM users WHERE created_at >= date('now', 'start of month')")
        new_users_month = cursor.fetchone()[0]
        
        # Active sessions
        cursor.execute("SELECT COUNT(*) FROM sessions WHERE expires_at > CURRENT_TIMESTAMP")
        active_sessions = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total_users': total_users,
            'new_users_month': new_users_month,
            'active_sessions': active_sessions
        }
        
    except Exception as e:
        return {'error': str(e)}

# Initialize database on import
init_database()
