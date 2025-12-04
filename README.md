<<<<<<< HEAD
## Title of the Project
Small description about the project like one below
The integration of a chatbot within a hostel booking system, aimed at streamlining the reservation process for students and improving the overall user experience.

## About
<!--Detailed Description about the project-->
Tailored Chatbot for Hostel Booking System is a project designed to integrate a chatbot that leverages advanced natural language processing techniques to understand and respond to user queries to the hostel booking system. Traditional hostel booking processes are often time-consuming and involve manual searches and extensive communication with hostel staff. This project seeks to overcome these challenges by creating an easy-to-use chatbot interface that assists students in addressing inquiries.

## Features
<!--List the features of the project as shown below-->
- Implements advance neural network method.
- A framework based application for deployment purpose.
- High scalability.
- Less time complexity.
- A specific scope of Chatbot response model, using json data format.

## Requirements
<!--List the requirements of the project as shown below-->
* Operating System: Requires a 64-bit OS (Windows 10 or Ubuntu) for compatibility with deep learning frameworks.
* Development Environment: Python 3.6 or later is necessary for coding the sign language detection system.
* Deep Learning Frameworks: TensorFlow for model training, MediaPipe for hand gesture recognition.
* Image Processing Libraries: OpenCV is essential for efficient image processing and real-time hand gesture recognition.
* Version Control: Implementation of Git for collaborative development and effective code management.
* IDE: Use of VSCode as the Integrated Development Environment for coding, debugging, and version control integration.
* Additional Dependencies: Includes scikit-learn, TensorFlow (versions 2.4.1), TensorFlow GPU, OpenCV, and Mediapipe for deep learning tasks.

## System Architecture
<!--Embed the system architecture diagram as shown below-->

![Screenshot 2023-11-25 133637](https://github.com/<<yourusername>>/Hand-Gesture-Recognition-System/assets/75235455/a60c11f3-0a11-47fb-ac89-755d5f45c995)


## Output

<!--Embed the Output picture at respective places as shown below as shown below-->
#### Output1 - Name of the output

![Screenshot 2023-11-25 134037](https://github.com/<<yourusername>>/Hand-Gesture-Recognition-System/assets/75235455/8c2b6b5c-5ed2-4ec4-b18e-5b6625402c16)

#### Output2 - Name of the output
![Screenshot 2023-11-25 134253](https://github.com/<<yourusername>>/Hand-Gesture-Recognition-System/assets/75235455/5e05c981-05ca-4aaa-aea2-d918dcf25cb7)

Detection Accuracy: 96.7%
Note: These metrics can be customized based on your actual performance evaluations.


## Results and Impact
<!--Give the results and impact as shown below-->
The Sign Language Detection System enhances accessibility for individuals with hearing and speech impairments, providing a valuable tool for inclusive communication. The project's integration of computer vision and deep learning showcases its potential for intuitive and interactive human-computer interaction.

This project serves as a foundation for future developments in assistive technologies and contributes to creating a more inclusive and accessible digital environment.

## Articles published / References
1. N. S. Gupta, S. K. Rout, S. Barik, R. R. Kalangi, and B. Swampa, “Enhancing Heart Disease Prediction Accuracy Through Hybrid Machine Learning Methods ”, EAI Endorsed Trans IoT, vol. 10, Mar. 2024.
2. A. A. BIN ZAINUDDIN, “Enhancing IoT Security: A Synergy of Machine Learning, Artificial Intelligence, and Blockchain”, Data Science Insights, vol. 2, no. 1, Feb. 2024.




=======
# College Bus Tracking Management System

A real-time bus tracking system built for Saveetha Engineering College with admin and student interfaces.

## Features

### Admin Interface
- Login: username `admin`, password `admin123`
- Add and manage student records (name, login, password, register number, age, blood group, bus route, area, bus stop, bus pass status)
- Add and manage bus records (driver info, bus details, route information)
- Update bus locations in real-time via Firebase
- Live location tracking for all buses

### Student Interface
- Personalized login with credentials set by admin
- Profile page with one-time photo upload
- Interactive bus cards with live tracking
- Real-time bus location on Chennai, Tamil Nadu map
- Proximity notifications when bus approaches student's stop
- Feedback system for queries and concerns
- Contact information page

## Tech Stack

- **Frontend**: Streamlit with custom CSS
- **Database**: PostgreSQL (via Replit)
- **Real-time Updates**: Firebase Realtime Database
- **Maps**: Folium with OpenStreetMap
- **Location**: Geopy for distance calculations

## Firebase Setup (Optional for Full Real-Time Tracking)

For complete real-time tracking with GPS-enabled bus drivers, you'll need to:

1. Create a Firebase project at https://console.firebase.google.com/
2. Enable Firebase Realtime Database
3. Download your service account JSON file
4. Upload the service account JSON content as `FIREBASE_SERVICE_ACCOUNT` secret

Currently, the system stores Firebase credentials in environment variables and allows manual location updates through the admin interface.

## Default Configuration

- Default map center: Chennai, Tamil Nadu (13.0827°N, 80.2707°E)
- Proximity notification threshold: 2 km
- Theme colors: Yellow (#FFD700), Orange (#FFA500), Purple (#6B46C1)

## Usage

### Admin Workflow
1. Login with admin/admin123
2. Navigate to "Students" tab to add student records
3. Navigate to "Buses" tab to add bus records
4. Use the location update feature to simulate bus movement
5. Buses sync with Firebase for real-time updates

### Student Workflow
1. Login with credentials provided by admin
2. View personal profile and upload photo (one-time only)
3. Browse available buses as interactive cards
4. Click on any bus card to see live location on map
5. Receive notifications when bus approaches your stop
6. Submit feedback or queries through the feedback form

## Color Scheme

The application uses the college's vibrant color scheme inspired by the yellow Saveetha Engineering College buses:
- Primary: Golden Yellow (#FFD700)
- Secondary: Orange (#FFA500)
- Accent: Purple (#6B46C1)
- Gradients for modern, attractive UI

## Security Notes

- Admin credentials are hardcoded for demonstration (change for production)
- Student passwords are stored in plain text (use hashing for production)
- Firebase service account should be properly secured
- All photos are stored locally in `student_photos/` directory
>>>>>>> 28784f1 (Integrate Firebase for real-time bus location tracking and updates)
