import streamlit as st
from streamlit_option_menu import option_menu
from database import get_db, close_db, Student, Bus
from sqlalchemy.exc import IntegrityError

def show():
    st.markdown("""
        <style>
        .admin-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 1.5rem;
            border-radius: 15px;
            color: white;
            text-align: center;
            margin-bottom: 2rem;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        
        .admin-title {
            font-size: 2.5rem;
            font-weight: 700;
            margin: 0;
        }
        
        .nav-container {
            background: white;
            padding: 1rem;
            border-radius: 15px;
            margin-bottom: 2rem;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        
        .form-container {
            background: white;
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            margin-bottom: 2rem;
        }
        
        .record-card {
            background: linear-gradient(135deg, #f6f8fb 0%, #ffffff 100%);
            padding: 1.5rem;
            border-radius: 12px;
            border-left: 5px solid #667eea;
            margin-bottom: 1rem;
            box-shadow: 0 3px 10px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
        }
        
        .record-card:hover {
            transform: translateX(5px);
            box-shadow: 0 5px 20px rgba(0,0,0,0.15);
        }
        
        .logout-btn {
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 999;
        }
        
        .stTextInput>div>div>input, .stSelectbox>div>div>select {
            border: 2px solid #E2E8F0;
            border-radius: 10px;
            padding: 0.75rem;
        }
        
        .stTextInput>div>div>input:focus, .stSelectbox>div>div>select:focus {
            border-color: #667eea;
        }
        </style>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([6, 1])
    with col2:
        if st.button("🚪 Logout", key="admin_logout"):
            st.session_state.logged_in = False
            st.session_state.user_type = None
            st.session_state.login_selection = None
            st.rerun()
    
    st.markdown("<div class='admin-header'><h1 class='admin-title'>🔐 Admin Dashboard</h1></div>", unsafe_allow_html=True)
    
    selected = option_menu(
        menu_title=None,
        options=["Students", "Buses"],
        icons=["people-fill", "bus-front-fill"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "white", "border-radius": "15px"},
            "icon": {"color": "#667eea", "font-size": "20px"},
            "nav-link": {
                "font-size": "16px",
                "text-align": "center",
                "margin": "0px",
                "padding": "15px",
                "border-radius": "10px",
            },
            "nav-link-selected": {"background": "linear-gradient(135deg, #FFD700 0%, #FFA500 100%)", "color": "black", "font-weight": "600"},
        }
    )
    
    if selected == "Students":
        show_students_page()
    elif selected == "Buses":
        show_buses_page()

def show_students_page():
    st.markdown("<div class='form-container'>", unsafe_allow_html=True)
    st.markdown("### 📝 Add New Student")
    
    with st.form("student_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Student Name *", placeholder="Enter full name")
            login_id = st.text_input("Login ID *", placeholder="Unique login ID")
            password = st.text_input("Password *", type="password", placeholder="Student password")
            register_number = st.text_input("Register Number *", placeholder="Registration number")
            age = st.number_input("Age", min_value=15, max_value=30, value=18)
        
        with col2:
            blood_group = st.selectbox("Blood Group", ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
            bus_route = st.text_input("Bus Route", placeholder="e.g., Route 1, Route 2")
            area = st.text_input("Area", placeholder="Student's area")
            bus_stop = st.text_input("Bus Stop", placeholder="Nearest bus stop")
            buspass_status = st.selectbox("Bus Pass Status", ["Active", "Inactive", "Pending"])
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            submit = st.form_submit_button("💾 Save Student", use_container_width=True)
        
        with col2:
            add_another = st.form_submit_button("➕ Save & Add Another", use_container_width=True)
        
        if submit or add_another:
            if not all([name, login_id, password, register_number]):
                st.error("Please fill all required fields marked with *")
            else:
                db = get_db()
                try:
                    new_student = Student(
                        name=name,
                        login_id=login_id,
                        password=password,
                        register_number=register_number,
                        age=age,
                        blood_group=blood_group,
                        bus_route=bus_route,
                        area=area,
                        bus_stop=bus_stop,
                        buspass_status=buspass_status
                    )
                    db.add(new_student)
                    db.commit()
                    st.success(f"✅ Student {name} added successfully!")
                    
                    if add_another:
                        st.rerun()
                    
                except IntegrityError:
                    db.rollback()
                    st.error("❌ Login ID or Register Number already exists!")
                except Exception as e:
                    db.rollback()
                    st.error(f"Error: {str(e)}")
                finally:
                    close_db(db)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("### 👥 Registered Students")
    
    db = get_db()
    try:
        students = db.query(Student).order_by(Student.created_at.desc()).all()
        
        if students:
            for student in students:
                st.markdown(f"""
                    <div class='record-card'>
                        <h4>🎓 {student.name}</h4>
                        <p><strong>Register Number:</strong> {student.register_number} | <strong>Login ID:</strong> {student.login_id}</p>
                        <p><strong>Age:</strong> {student.age} | <strong>Blood Group:</strong> {student.blood_group}</p>
                        <p><strong>Bus Route:</strong> {student.bus_route} | <strong>Bus Stop:</strong> {student.bus_stop}</p>
                        <p><strong>Bus Pass:</strong> {student.buspass_status}</p>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No students registered yet.")
    finally:
        close_db(db)

def show_buses_page():
    st.markdown("<div class='form-container'>", unsafe_allow_html=True)
    st.markdown("### 🚌 Add New Bus")
    
    with st.form("bus_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            driver_name = st.text_input("Driver Name *", placeholder="Enter driver name")
            driver_phone = st.text_input("Driver Phone *", placeholder="10-digit phone number")
            bus_name = st.text_input("Bus Name *", placeholder="e.g., Saveetha Express")
            bus_via = st.text_input("Bus Via", placeholder="Areas covered by bus")
        
        with col2:
            bus_number = st.text_input("Bus Number *", placeholder="Vehicle registration number")
            bus_route_number = st.text_input("Bus Route Number *", placeholder="e.g., Route 1")
            current_latitude = st.number_input("Current Latitude", value=13.0827, format="%.6f", help="Default: Chennai")
            current_longitude = st.number_input("Current Longitude", value=80.2707, format="%.6f", help="Default: Chennai")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            submit = st.form_submit_button("💾 Save Bus", use_container_width=True)
        
        with col2:
            add_another = st.form_submit_button("➕ Save & Add Another", use_container_width=True)
        
        if submit or add_another:
            if not all([driver_name, driver_phone, bus_name, bus_number, bus_route_number]):
                st.error("Please fill all required fields marked with *")
            else:
                db = get_db()
                try:
                    new_bus = Bus(
                        driver_name=driver_name,
                        driver_phone=driver_phone,
                        bus_name=bus_name,
                        bus_via=bus_via,
                        bus_number=bus_number,
                        bus_route_number=bus_route_number,
                        current_latitude=current_latitude,
                        current_longitude=current_longitude
                    )
                    db.add(new_bus)
                    db.commit()
                    st.success(f"✅ Bus {bus_name} added successfully!")
                    
                    if add_another:
                        st.rerun()
                    
                except IntegrityError:
                    db.rollback()
                    st.error("❌ Bus Number already exists!")
                except Exception as e:
                    db.rollback()
                    st.error(f"Error: {str(e)}")
                finally:
                    close_db(db)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("### 🚍 Registered Buses")
    
    db = get_db()
    try:
        buses = db.query(Bus).order_by(Bus.created_at.desc()).all()
        
        if buses:
            for bus in buses:
                st.markdown(f"""
                    <div class='record-card'>
                        <h4>🚌 {bus.bus_name}</h4>
                        <p><strong>Bus Number:</strong> {bus.bus_number} | <strong>Route:</strong> {bus.bus_route_number}</p>
                        <p><strong>Driver:</strong> {bus.driver_name} | <strong>Phone:</strong> {bus.driver_phone}</p>
                        <p><strong>Via:</strong> {bus.bus_via}</p>
                        <p><strong>Location:</strong> {bus.current_latitude}, {bus.current_longitude}</p>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No buses registered yet.")
    finally:
        close_db(db)
