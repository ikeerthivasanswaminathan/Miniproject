import streamlit as st
from database import init_db
import admin_interface
import student_interface

st.set_page_config(
    page_title="College Bus Tracking System",
    page_icon="🚌",
    layout="wide",
    initial_sidebar_state="collapsed"
)

init_db()

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_type' not in st.session_state:
    st.session_state.user_type = None
if 'student_login_id' not in st.session_state:
    st.session_state.student_login_id = None
if 'login_selection' not in st.session_state:
    st.session_state.login_selection = None

def load_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
        
        * {
            font-family: 'Poppins', sans-serif;
        }
        
        .main {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            background-attachment: fixed;
        }
        
        .login-container {
            background: white;
            padding: 3rem;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            max-width: 450px;
            margin: 2rem auto;
            animation: fadeIn 0.5s ease-in;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .login-title {
            text-align: center;
            color: #6B46C1;
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }
        
        .login-subtitle {
            text-align: center;
            color: #718096;
            font-size: 1rem;
            margin-bottom: 2rem;
        }
        
        .bus-icon {
            font-size: 4rem;
            text-align: center;
            margin-bottom: 1rem;
        }
        
        .stButton>button {
            width: 100%;
            background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
            color: #000;
            border: none;
            padding: 0.75rem;
            border-radius: 10px;
            font-weight: 600;
            font-size: 1.1rem;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(255, 215, 0, 0.4);
        }
        
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(255, 215, 0, 0.6);
        }
        
        .selection-card {
            background: white;
            padding: 2rem;
            border-radius: 15px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            margin: 1rem;
        }
        
        .selection-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        
        .selection-icon {
            font-size: 3rem;
            margin-bottom: 1rem;
        }
        
        .selection-title {
            font-size: 1.5rem;
            font-weight: 600;
            color: #2D3748;
        }
        
        .stTextInput>div>div>input {
            border: 2px solid #E2E8F0;
            border-radius: 10px;
            padding: 0.75rem;
            font-size: 1rem;
        }
        
        .stTextInput>div>div>input:focus {
            border-color: #6B46C1;
            box-shadow: 0 0 0 3px rgba(107, 70, 193, 0.1);
        }
        
        </style>
    """, unsafe_allow_html=True)

def main_login_page():
    load_css()
    
    st.markdown("<div class='bus-icon'>🚌</div>", unsafe_allow_html=True)
    st.markdown("<h1 class='login-title'>College Bus Tracking</h1>", unsafe_allow_html=True)
    st.markdown("<p class='login-subtitle'>Real-Time Bus Management System</p>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔐 Admin Login", key="admin_select", use_container_width=True):
            st.session_state.login_selection = 'admin'
            st.rerun()
    
    with col2:
        if st.button("🎓 Student Login", key="student_select", use_container_width=True):
            st.session_state.login_selection = 'student'
            st.rerun()

def admin_login():
    load_css()
    
    st.markdown("<div class='bus-icon'>🔐</div>", unsafe_allow_html=True)
    st.markdown("<h1 class='login-title'>Admin Login</h1>", unsafe_allow_html=True)
    st.markdown("<p class='login-subtitle'>Access the administrative dashboard</p>", unsafe_allow_html=True)
    
    st.markdown("<div class='login-container'>", unsafe_allow_html=True)
    
    username = st.text_input("Username", placeholder="Enter admin username")
    password = st.text_input("Password", type="password", placeholder="Enter password")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("Login", use_container_width=True):
            if username == "admin" and password == "admin123":
                st.session_state.logged_in = True
                st.session_state.user_type = 'admin'
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid credentials!")
    
    with col2:
        if st.button("Back", use_container_width=True):
            st.session_state.login_selection = None
            st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)

def student_login():
    load_css()
    
    st.markdown("<div class='bus-icon'>🎓</div>", unsafe_allow_html=True)
    st.markdown("<h1 class='login-title'>Student Login</h1>", unsafe_allow_html=True)
    st.markdown("<p class='login-subtitle'>Access your personalized dashboard</p>", unsafe_allow_html=True)
    
    st.markdown("<div class='login-container'>", unsafe_allow_html=True)
    
    login_id = st.text_input("Login ID", placeholder="Enter your login ID")
    password = st.text_input("Password", type="password", placeholder="Enter password")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("Login", use_container_width=True):
            from database import get_db, close_db, Student
            db = get_db()
            try:
                student = db.query(Student).filter(
                    Student.login_id == login_id,
                    Student.password == password
                ).first()
                
                if student:
                    st.session_state.logged_in = True
                    st.session_state.user_type = 'student'
                    st.session_state.student_login_id = login_id
                    st.session_state.student_name = student.name
                    st.success(f"Welcome, {student.name}!")
                    st.rerun()
                else:
                    st.error("Invalid login credentials!")
            finally:
                close_db(db)
    
    with col2:
        if st.button("Back", use_container_width=True):
            st.session_state.login_selection = None
            st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)

if not st.session_state.logged_in:
    if st.session_state.login_selection == 'admin':
        admin_login()
    elif st.session_state.login_selection == 'student':
        student_login()
    else:
        main_login_page()
else:
    if st.session_state.user_type == 'admin':
        admin_interface.show()
    elif st.session_state.user_type == 'student':
        student_interface.show()
