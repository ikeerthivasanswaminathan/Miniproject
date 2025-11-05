import streamlit as st
from streamlit_option_menu import option_menu
from database import get_db, close_db, Student, Bus, Feedback, Notification
import os
from PIL import Image
import io
import base64
from datetime import datetime
from geopy.distance import geodesic
import folium
from streamlit_folium import st_folium

UPLOAD_FOLDER = "student_photos"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def show():
    st.markdown("""
        <style>
        .student-header {
            background: linear-gradient(135deg, #FFD700 0%, #FFA500 50%, #6B46C1 100%);
            padding: 1.5rem;
            border-radius: 15px;
            color: white;
            text-align: center;
            margin-bottom: 2rem;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        
        .student-title {
            font-size: 2.5rem;
            font-weight: 700;
            margin: 0;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .profile-card {
            background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
            padding: 2rem;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.15);
            margin-bottom: 2rem;
            border: 3px solid #FFD700;
            transition: all 0.3s ease;
        }
        
        .profile-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(0,0,0,0.2);
        }
        
        .info-row {
            display: flex;
            justify-content: space-between;
            padding: 1rem;
            margin: 0.5rem 0;
            background: white;
            border-radius: 10px;
            border-left: 4px solid #6B46C1;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }
        
        .info-label {
            font-weight: 600;
            color: #4A5568;
        }
        
        .info-value {
            color: #2D3748;
            font-weight: 500;
        }
        
        .bus-card {
            background: linear-gradient(135deg, #ffffff 0%, #f6f8fb 100%);
            padding: 1.5rem;
            border-radius: 15px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            margin-bottom: 1.5rem;
            border: 2px solid transparent;
            cursor: pointer;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            position: relative;
            overflow: hidden;
        }
        
        .bus-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 215, 0, 0.3), transparent);
            transition: left 0.5s ease;
        }
        
        .bus-card:hover::before {
            left: 100%;
        }
        
        .bus-card:hover {
            transform: translateY(-10px) scale(1.02);
            box-shadow: 0 15px 40px rgba(107, 70, 193, 0.3);
            border-color: #FFD700;
        }
        
        .bus-card-header {
            font-size: 1.5rem;
            font-weight: 700;
            color: #6B46C1;
            margin-bottom: 0.5rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        .bus-card-route {
            font-size: 1.1rem;
            color: #FFA500;
            font-weight: 600;
            margin-bottom: 1rem;
        }
        
        .bus-card-detail {
            font-size: 0.95rem;
            color: #4A5568;
            margin: 0.3rem 0;
        }
        
        .notification-badge {
            background: #FF4444;
            color: white;
            padding: 0.3rem 0.8rem;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.7; }
        }
        
        .photo-upload-section {
            background: linear-gradient(135deg, #6B46C1 0%, #8B5CF6 100%);
            padding: 2rem;
            border-radius: 15px;
            color: white;
            text-align: center;
            margin-bottom: 2rem;
        }
        
        .contact-card {
            background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
            padding: 2rem;
            border-radius: 15px;
            color: #2D3748;
            margin-bottom: 1.5rem;
            box-shadow: 0 8px 25px rgba(255, 165, 0, 0.3);
            transition: all 0.3s ease;
        }
        
        .contact-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 35px rgba(255, 165, 0, 0.4);
        }
        
        .feedback-container {
            background: white;
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        }
        
        </style>
    """, unsafe_allow_html=True)
    
    check_bus_proximity()
    
    db = get_db()
    try:
        student = db.query(Student).filter(Student.login_id == st.session_state.student_login_id).first()
        
        col1, col2 = st.columns([5, 1])
        with col1:
            st.markdown(f"<div class='student-header'><h1 class='student-title'>👋 Welcome, {student.name}!</h1></div>", unsafe_allow_html=True)
        
        with col2:
            unread_notifications = db.query(Notification).filter(
                Notification.student_login_id == st.session_state.student_login_id,
                Notification.is_read == False
            ).count()
            
            if unread_notifications > 0:
                st.markdown(f"<div class='notification-badge'>🔔 {unread_notifications} New</div>", unsafe_allow_html=True)
    finally:
        close_db(db)
    
    selected = option_menu(
        menu_title=None,
        options=["Profile", "Buses", "Feedback", "Contact", "Logout"],
        icons=["person-circle", "bus-front", "chat-left-text", "telephone", "box-arrow-right"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "white", "border-radius": "15px"},
            "icon": {"color": "#6B46C1", "font-size": "18px"},
            "nav-link": {
                "font-size": "15px",
                "text-align": "center",
                "margin": "0px",
                "padding": "12px",
                "border-radius": "10px",
            },
            "nav-link-selected": {"background": "linear-gradient(135deg, #FFD700 0%, #FFA500 100%)", "color": "black", "font-weight": "600"},
        }
    )
    
    if selected == "Profile":
        show_profile_page()
    elif selected == "Buses":
        show_buses_page()
    elif selected == "Feedback":
        show_feedback_page()
    elif selected == "Contact":
        show_contact_page()
    elif selected == "Logout":
        st.session_state.logged_in = False
        st.session_state.user_type = None
        st.session_state.student_login_id = None
        st.session_state.login_selection = None
        st.rerun()

def show_profile_page():
    db = get_db()
    try:
        student = db.query(Student).filter(Student.login_id == st.session_state.student_login_id).first()
        
        col1, col2 = st.columns([2, 1])
        
        with col2:
            if student.photo_uploaded and student.photo_path and os.path.exists(student.photo_path):
                st.image(student.photo_path, caption="Profile Photo", use_container_width=True)
            else:
                st.markdown("<div class='photo-upload-section'>", unsafe_allow_html=True)
                st.markdown("### 📸 Upload Profile Photo")
                st.markdown("One-time upload only")
                
                uploaded_file = st.file_uploader("Choose a photo", type=["jpg", "jpeg", "png"], key="photo_upload")
                
                if uploaded_file is not None:
                    if st.button("Upload Photo"):
                        image = Image.open(uploaded_file)
                        photo_path = os.path.join(UPLOAD_FOLDER, f"{student.login_id}.jpg")
                        image.save(photo_path)
                        
                        student.photo_uploaded = True
                        student.photo_path = photo_path
                        db.commit()
                        st.success("Photo uploaded successfully!")
                        st.rerun()
                
                st.markdown("</div>", unsafe_allow_html=True)
        
        with col1:
            st.markdown("<div class='profile-card'>", unsafe_allow_html=True)
            st.markdown("### 🎓 Student Information")
            
            st.markdown(f"""
                <div class='info-row'>
                    <span class='info-label'>📛 Name:</span>
                    <span class='info-value'>{student.name}</span>
                </div>
                <div class='info-row'>
                    <span class='info-label'>🆔 Register Number:</span>
                    <span class='info-value'>{student.register_number}</span>
                </div>
                <div class='info-row'>
                    <span class='info-label'>🔑 Login ID:</span>
                    <span class='info-value'>{student.login_id}</span>
                </div>
                <div class='info-row'>
                    <span class='info-label'>🎂 Age:</span>
                    <span class='info-value'>{student.age} years</span>
                </div>
                <div class='info-row'>
                    <span class='info-label'>🩸 Blood Group:</span>
                    <span class='info-value'>{student.blood_group}</span>
                </div>
                <div class='info-row'>
                    <span class='info-label'>🚌 Bus Route:</span>
                    <span class='info-value'>{student.bus_route}</span>
                </div>
                <div class='info-row'>
                    <span class='info-label'>📍 Area:</span>
                    <span class='info-value'>{student.area}</span>
                </div>
                <div class='info-row'>
                    <span class='info-label'>🛑 Bus Stop:</span>
                    <span class='info-value'>{student.bus_stop}</span>
                </div>
                <div class='info-row'>
                    <span class='info-label'>🎫 Bus Pass Status:</span>
                    <span class='info-value'>{student.buspass_status}</span>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
    
    finally:
        close_db(db)

def show_buses_page():
    st.markdown("### 🚌 Available Buses")
    
    if 'selected_bus' not in st.session_state:
        st.session_state.selected_bus = None
    
    db = get_db()
    try:
        buses = db.query(Bus).filter(Bus.is_active == True).all()
        
        if not buses:
            st.info("No buses available at the moment.")
            return
        
        if st.session_state.selected_bus is None:
            cols = st.columns(2)
            
            for idx, bus in enumerate(buses):
                with cols[idx % 2]:
                    bus_card_html = f"""
                        <div class='bus-card'>
                            <div class='bus-card-header'>
                                🚌 {bus.bus_name}
                            </div>
                            <div class='bus-card-route'>
                                📍 Route {bus.bus_route_number}
                            </div>
                            <div class='bus-card-detail'>
                                <strong>Via:</strong> {bus.bus_via or 'Multiple areas'}
                            </div>
                            <div class='bus-card-detail'>
                                <strong>Bus Number:</strong> {bus.bus_number}
                            </div>
                            <div class='bus-card-detail'>
                                <strong>Driver:</strong> {bus.driver_name}
                            </div>
                        </div>
                    """
                    st.markdown(bus_card_html, unsafe_allow_html=True)
                    
                    if st.button(f"📍 Track {bus.bus_name}", key=f"track_{bus.id}", use_container_width=True):
                        st.session_state.selected_bus = bus.id
                        st.rerun()
        
        else:
            bus = db.query(Bus).filter(Bus.id == st.session_state.selected_bus).first()
            
            if st.button("⬅️ Back to All Buses"):
                st.session_state.selected_bus = None
                st.rerun()
            
            st.markdown(f"### 🚌 {bus.bus_name} - Live Tracking")
            
            m = folium.Map(
                location=[bus.current_latitude, bus.current_longitude],
                zoom_start=13,
                tiles='OpenStreetMap'
            )
            
            folium.Marker(
                [bus.current_latitude, bus.current_longitude],
                popup=f"<b>{bus.bus_name}</b><br>Route {bus.bus_route_number}",
                tooltip=f"{bus.bus_name}",
                icon=folium.Icon(color='red', icon='bus', prefix='fa')
            ).add_to(m)
            
            st_folium(m, width=700, height=500)
            
            st.markdown("<div class='profile-card'>", unsafe_allow_html=True)
            st.markdown("### 📊 Bus Details")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                    <div class='info-row'>
                        <span class='info-label'>🚌 Bus Name:</span>
                        <span class='info-value'>{bus.bus_name}</span>
                    </div>
                    <div class='info-row'>
                        <span class='info-label'>🔢 Bus Number:</span>
                        <span class='info-value'>{bus.bus_number}</span>
                    </div>
                    <div class='info-row'>
                        <span class='info-label'>📍 Route Number:</span>
                        <span class='info-value'>{bus.bus_route_number}</span>
                    </div>
                    <div class='info-row'>
                        <span class='info-label'>🛣️ Via:</span>
                        <span class='info-value'>{bus.bus_via or 'Multiple areas'}</span>
                    </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                    <div class='info-row'>
                        <span class='info-label'>👨‍✈️ Driver Name:</span>
                        <span class='info-value'>{bus.driver_name}</span>
                    </div>
                    <div class='info-row'>
                        <span class='info-label'>📞 Driver Phone:</span>
                        <span class='info-value'>{bus.driver_phone}</span>
                    </div>
                    <div class='info-row'>
                        <span class='info-label'>📍 Current Location:</span>
                        <span class='info-value'>{bus.current_latitude:.4f}, {bus.current_longitude:.4f}</span>
                    </div>
                    <div class='info-row'>
                        <span class='info-label'>🟢 Status:</span>
                        <span class='info-value'>Active</span>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
    
    finally:
        close_db(db)

def show_feedback_page():
    st.markdown("<div class='feedback-container'>", unsafe_allow_html=True)
    st.markdown("### 💬 Submit Feedback or Query")
    st.markdown("We value your feedback! Please share your thoughts, queries, or concerns.")
    
    db = get_db()
    try:
        student = db.query(Student).filter(Student.login_id == st.session_state.student_login_id).first()
        
        with st.form("feedback_form", clear_on_submit=True):
            st.text_input("Register Number", value=student.register_number, disabled=True)
            st.text_input("Name", value=student.name, disabled=True)
            
            query = st.text_area("Your Query/Feedback *", placeholder="Please describe your query or feedback in detail...", height=150)
            
            submit = st.form_submit_button("📤 Submit Feedback", use_container_width=True)
            
            if submit:
                if not query.strip():
                    st.error("Please enter your query or feedback.")
                else:
                    new_feedback = Feedback(
                        register_number=student.register_number,
                        student_name=student.name,
                        query=query
                    )
                    db.add(new_feedback)
                    db.commit()
                    st.success("✅ Your feedback has been submitted successfully! We'll get back to you soon.")
    
    finally:
        close_db(db)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 📋 Your Previous Feedback")
    
    db = get_db()
    try:
        student = db.query(Student).filter(Student.login_id == st.session_state.student_login_id).first()
        feedbacks = db.query(Feedback).filter(
            Feedback.register_number == student.register_number
        ).order_by(Feedback.submitted_at.desc()).all()
        
        if feedbacks:
            for feedback in feedbacks:
                status_color = "#28a745" if feedback.status == "Resolved" else "#ffc107"
                st.markdown(f"""
                    <div class='profile-card'>
                        <p><strong>📅 Date:</strong> {feedback.submitted_at.strftime('%B %d, %Y at %I:%M %p')}</p>
                        <p><strong>💬 Query:</strong> {feedback.query}</p>
                        <p><strong>Status:</strong> <span style='color: {status_color}; font-weight: 600;'>{feedback.status}</span></p>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No previous feedback found.")
    
    finally:
        close_db(db)

def show_contact_page():
    st.markdown("### 📞 Contact Information")
    
    st.markdown("""
        <div class='contact-card'>
            <h3>🏫 Saveetha Engineering College</h3>
            <p style='font-size: 1.1rem; margin-top: 1rem;'>
                <strong>📍 Address:</strong><br>
                Saveetha Nagar, Thandalam<br>
                Chennai - 602 105, Tamil Nadu, India
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div class='contact-card'>
                <h4>📞 Phone Numbers</h4>
                <p><strong>Main Office:</strong> +91 44 6680 1000</p>
                <p><strong>Transport Dept:</strong> +91 44 6680 1234</p>
                <p><strong>Emergency:</strong> +91 98765 43210</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class='contact-card'>
                <h4>📧 Email Addresses</h4>
                <p><strong>General Inquiry:</strong><br>info@saveetha.ac.in</p>
                <p><strong>Transport:</strong><br>transport@saveetha.ac.in</p>
                <p><strong>Support:</strong><br>support@saveetha.ac.in</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class='contact-card'>
            <h4>🕒 Office Hours</h4>
            <p><strong>Monday - Friday:</strong> 8:00 AM - 5:00 PM</p>
            <p><strong>Saturday:</strong> 8:00 AM - 1:00 PM</p>
            <p><strong>Sunday:</strong> Closed</p>
        </div>
    """, unsafe_allow_html=True)

def check_bus_proximity():
    db = get_db()
    try:
        student = db.query(Student).filter(Student.login_id == st.session_state.student_login_id).first()
        
        if not student or not student.bus_stop:
            return
        
        buses = db.query(Bus).filter(Bus.is_active == True).all()
        
        PROXIMITY_THRESHOLD_KM = 2.0
        
        student_location = (13.0827, 80.2707)
        
        for bus in buses:
            bus_location = (bus.current_latitude, bus.current_longitude)
            distance = geodesic(student_location, bus_location).kilometers
            
            if distance <= PROXIMITY_THRESHOLD_KM:
                existing_notification = db.query(Notification).filter(
                    Notification.student_login_id == student.login_id,
                    Notification.bus_number == bus.bus_number,
                    Notification.is_read == False
                ).first()
                
                if not existing_notification:
                    notification = Notification(
                        student_login_id=student.login_id,
                        bus_number=bus.bus_number,
                        message=f"🚌 {bus.bus_name} is approaching your stop! Distance: {distance:.1f} km"
                    )
                    db.add(notification)
                    db.commit()
    
    except Exception as e:
        pass
    finally:
        close_db(db)
