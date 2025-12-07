# College Bus Tracking Management System

## Overview

A real-time bus tracking system designed for Saveetha Engineering College that enables administrators to manage student and bus records while providing students with live bus tracking, proximity notifications, and feedback capabilities. The system features dual interfaces (admin and student) with real-time location updates powered by Firebase and PostgreSQL for persistent data storage.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit with custom CSS styling
- **Design Pattern**: Multi-page application with separate interface modules (`admin_interface.py`, `student_interface.py`)
- **UI Components**: 
  - Custom gradient themes using yellow (#FFD700), orange (#FFA500), and purple (#6B46C1)
  - Interactive navigation using `streamlit_option_menu`
  - Card-based layouts with hover effects for bus displays
  - Responsive design with animation keyframes
- **Routing**: Session-based state management for user authentication and interface switching

### Backend Architecture
- **Database ORM**: SQLAlchemy with declarative base pattern
- **Data Models**:
  - `Student`: User credentials, personal details, bus assignment, photo management
  - `Bus`: Driver information, vehicle details, route mapping, real-time coordinates
  - `Feedback`: Student queries and concerns collection
  - `Notification`: (Referenced but implementation incomplete)
- **Session Management**: SQLAlchemy SessionLocal with connection pooling (pool_pre_ping, pool_recycle=3600)
- **Authentication**: Simple credential matching against database records

### Real-Time Location System
- **Architecture**: Hybrid approach combining Firebase Realtime Database with PostgreSQL
- **Design Decision**: 
  - Firebase handles live GPS coordinate streaming for minimal latency
  - PostgreSQL stores persistent bus/student data and last-known positions
  - Rationale: Firebase provides sub-second updates for tracking while PostgreSQL ensures data integrity
- **Location Updates**: Admin-triggered manual updates or Firebase real-time sync
- **Proximity Detection**: Geopy geodesic calculations with 2km threshold for notifications

### Data Storage Solutions
- **Primary Database**: PostgreSQL via Replit environment (`DATABASE_URL`)
- **Real-Time Cache**: Firebase Realtime Database for bus coordinates
- **File Storage**: Local filesystem for student photo uploads (`student_photos/` directory)
- **Connection Strategy**: Environment-based configuration with connection pooling

### Authentication & Authorization
- **Admin Access**: Hardcoded credentials (username: `admin`, password: `admin123`)
- **Student Access**: Database-driven with unique login_id/password pairs created by admin
- **Session Persistence**: Streamlit session_state for maintaining login status
- **Security Note**: Current implementation uses plain-text passwords (production would require hashing)

### Mapping & Geolocation
- **Mapping Library**: Folium with OpenStreetMap tiles
- **Integration**: `streamlit_folium` for embedding interactive maps
- **Default Center**: Chennai, Tamil Nadu (13.0827°N, 80.2707°E)
- **Distance Calculations**: Geopy for proximity-based notifications
- **Location Flow**: Firebase → Database sync → Map rendering with live markers

### Application State Management
- **Pattern**: Centralized session state in `app.py`
- **Tracked States**: `logged_in`, `user_type`, `student_login_id`, `login_selection`
- **Initialization**: Default values set on application startup
- **Persistence**: Session-scoped (resets on browser refresh)

## External Dependencies

### Firebase Integration
- **Service**: Firebase Realtime Database
- **Purpose**: Live GPS coordinate streaming for bus tracking
- **Configuration**: Service account JSON credentials via environment variables
  - `FIREBASE_PROJECT_ID`
  - `FIREBASE_DATABASE_URL`
- **Data Structure**: Bus locations stored at `/buses/{bus_number}` with latitude, longitude, timestamp, and speed
- **Initialization**: Lazy initialization with global flag to prevent duplicate app instances
- **Fallback**: Graceful degradation to PostgreSQL-only mode if Firebase unavailable

### Database Service
- **Provider**: PostgreSQL (Replit-hosted)
- **Connection**: Environment variable `DATABASE_URL`
- **Schema Management**: SQLAlchemy declarative models with automatic table creation
- **Connection Pooling**: Pre-ping validation and 1-hour recycling for reliability

### Third-Party Python Libraries
- **streamlit**: Web application framework
- **streamlit-option-menu**: Navigation menu component
- **sqlalchemy**: Database ORM and connection management
- **firebase-admin**: Firebase SDK for Python
- **folium**: Interactive map generation
- **streamlit-folium**: Folium-Streamlit integration
- **geopy**: Geocoding and distance calculations
- **Pillow (PIL)**: Image processing for photo uploads

### External APIs & Services
- **OpenStreetMap**: Map tile provider for Folium visualizations
- **Firebase Authentication Services**: OAuth endpoints for service account validation
- **Google Fonts**: Poppins font family for UI typography

### Configuration Dependencies
- Environment variables required for operation:
  - `DATABASE_URL`: PostgreSQL connection string
  - `FIREBASE_PROJECT_ID`: Firebase project identifier
  - `FIREBASE_DATABASE_URL`: Realtime database endpoint
  - Optional: `FIREBASE_SERVICE_ACCOUNT` for complete credentials JSON