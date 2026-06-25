# 🩺 Liver Cirrhosis Patient Monitoring System

A full-stack healthcare web application developed to assist healthcare professionals in monitoring liver cirrhosis patients through patient management, vital sign tracking, report analysis, automated risk assessment, and alert generation.

> Developed as part of the Software Engineering and Project Management course using an Agile Scrum methodology.

---

## 📌 Project Overview

The **Liver Cirrhosis Patient Monitoring System** enables doctors to securely manage patient records, upload medical reports, monitor vital signs, assess patient risk levels, and receive automated alerts for critical health conditions.

The project follows an **Iterative Enhancement Model**, where new features and improvements are added incrementally across development sprints.

---

## ✨ Features

### 🔐 Authentication
- User Login
- User Registration
- Persistent account storage
- Profile management

### 👨‍⚕️ Patient Management
- Add new patients
- View patient records
- Search patients by Name or MRN
- Delete patient records
- Persistent patient database

### ❤️ Vital Sign Monitoring
- Blood Pressure
- Heart Rate
- Temperature
- Oxygen Saturation (SpO₂)

### 📊 Patient Status Calculation
Patient condition is automatically classified as:
- 🟢 Stable
- 🟡 Monitoring
- 🔴 Critical

Status is calculated dynamically based on the patient's latest vital signs.

### 🚨 Automatic Alert Generation
The system automatically generates alerts when abnormal vital signs are detected.

Examples:
- High Blood Pressure
- Low Oxygen Saturation
- Fever
- High Heart Rate

### 📂 Report Management
- Upload Current Report
- Upload Previous Report
- Store PDF/Image reports
- Report comparison support

### 📈 Dashboard
- Total Patients
- Critical Cases
- Monitoring Cases
- Stable Patients
- Risk Distribution
- Treatment Distribution

### ⚙️ Settings
- Update profile information
- Save user preferences

---

## 🏗️ System Architecture

The project follows a **Three-Tier Architecture** consisting of:

### Presentation Layer
- HTML
- CSS
- JavaScript

### Application Layer
- Flask
- REST APIs
- Business Logic
- Authentication
- Status Calculation
- Alert Generation

### Data Layer
- SQLite Database
- File Storage (Patient Reports)

---

## 🛠️ Tech Stack

### Frontend
- HTML5
- CSS3
- JavaScript

### Backend
- Python
- Flask

### Database
- SQLite

### File Storage
- Local Upload Directory

---

## 📁 Project Structure

```text
Liver-Cirrhosis-Patient-Monitoring-System/
│
├── backend/
│   ├── app.py
│   ├── routes/
│   ├── models/
│   └── database/
│
├── frontend/
│   ├── login.html
│   ├── dashboard.html
│   ├── patient_records.html
│   ├── add_patient.html
│   ├── upload_reports.html
│   ├── alerts.html
│   ├── settings.html
│   ├── css/
│   └── js/
│
├── uploads/
│
├── screenshots/
│
├── README.md
├── requirements.txt
└── LICENSE
```

---

## 🚀 Installation

### Clone Repository

```bash
git clone https://github.com/FarzeenAjmal/Liver-Cirrhosis-Patient-Monitoring-System.git
```

### Navigate into the project

```bash
cd Liver-Cirrhosis-Patient-Monitoring-System
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the Application

```bash
python app.py
```

The application will be available at:

```
http://localhost:5000
```

---

## 📸 Screenshots

You can add screenshots here.

Example:

```
screenshots/
├── login.png
├── dashboard.png
├── patient_records.png
├── upload_reports.png
├── alerts.png
└── settings.png
```

---

## 📋 Sprint Highlights

### Sprint 1
- User Authentication
- Dashboard UI
- Patient Records
- Add Patient
- Upload Reports
- Alerts
- Settings
- Three-Tier Architecture Design

### Sprint 2
- SQLite Database Integration
- Persistent Data Storage
- Dynamic Patient Status Calculation
- Automatic Alert Generation
- Delete Patient Feature
- Backend Validation
- Improved Risk Analysis
- Functional Testing
- Risk Management (RMMM)

---

## 🧪 Testing

The project includes:

- Functional Test Cases
- Acceptance Criteria Validation
- Sprint Retrospective
- Risk Mitigation, Monitoring and Management (RMMM)

---

## 📖 Development Methodology

- Agile Scrum
- Iterative Enhancement Model
- Sprint Planning
- Sprint Review
- Sprint Retrospective

---

## 👥 Team Members

- **Mohammed Farzeen Ajmal**
- **Guna Sekhar Reddy Kuppala**
- **Mohammed Febinsha**

---

## 📄 License

This project is developed for academic purposes under the Software Engineering and Project Management course.

---

## ⭐ If you like this project

Consider giving this repository a ⭐ on GitHub!
