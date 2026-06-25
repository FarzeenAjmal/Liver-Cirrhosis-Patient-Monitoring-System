from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import bcrypt

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(150), nullable=True)
    email = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    role = db.Column(db.String(50), nullable=True, default='Hepatologist')

    def set_password(self, raw_password):
        self.password = bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, raw_password):
        return bcrypt.checkpw(raw_password.encode('utf-8'), self.password.encode('utf-8'))

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'email': self.email, 'role': self.role}

class Patient(db.Model):
    __tablename__ = 'patients'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(150), nullable=False)
    mrn = db.Column(db.String(50), nullable=False, unique=True)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(20))
    child_pugh = db.Column(db.String(20), nullable=True)
    last_visit = db.Column(db.DateTime, nullable=True)
    
    # Cascade deletions
    vitals = db.relationship('Vital', backref='patient', cascade="all, delete-orphan")
    alerts = db.relationship('Alert', backref='patient', cascade="all, delete-orphan")
    reports = db.relationship('Report', backref='patient', cascade="all, delete-orphan")
    analysis_history = db.relationship('AnalysisHistory', backref='patient', cascade="all, delete-orphan")

    def to_dict(self):
        return {
            'id': self.id, 'name': self.name, 'mrn': self.mrn, 
            'age': self.age, 'gender': self.gender, 
            'child_pugh': self.child_pugh,
            'last_visit': self.last_visit.strftime("%Y-%m-%d %H:%M:%S") if self.last_visit else ''
        }

class Vital(db.Model):
    __tablename__ = 'vitals'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id', ondelete='CASCADE'))
    bp = db.Column(db.String(20))
    hr = db.Column(db.Integer)
    spo2 = db.Column(db.Float)
    temperature = db.Column(db.Float)
    recorded_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id, 'patient_id': self.patient_id, 'bp': self.bp, 
            'hr': self.hr, 'spo2': self.spo2, 'temperature': self.temperature, 
            'recorded_at': self.recorded_at.strftime("%Y-%m-%d %H:%M:%S") if self.recorded_at else ''
        }

class Alert(db.Model):
    __tablename__ = 'alerts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id', ondelete='CASCADE'))
    type = db.Column(db.String(50)) # CRITICAL / WARNING
    message = db.Column(db.Text)
    status = db.Column(db.String(20), default='active') # active / resolved
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        patient_name = f"{self.patient.name} ({self.patient.mrn})" if self.patient else "Unknown"
        return {
            'id': self.id, 'patient_id': self.patient_id, 'patientName': patient_name,
            'type': self.type, 'message': self.message, 'status': self.status, 
            'created_at': self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else ''
        }

class Report(db.Model):
    __tablename__ = 'reports'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id', ondelete='CASCADE'))
    file_path = db.Column(db.String(300))
    type = db.Column(db.String(100), nullable=True) # e.g. blood_test, fibroscan
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id, 'patient_id': self.patient_id, 
            'file_path': self.file_path, 
            'type': self.type,
            'uploaded_at': self.uploaded_at.strftime("%Y-%m-%d %H:%M:%S") if self.uploaded_at else ''
        }

class AnalysisHistory(db.Model):
    __tablename__ = 'analysis_history'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id', ondelete='CASCADE'))
    result = db.Column(db.Text) # e.g. JSON string of parameter changes/recommendations
    risk_level = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        patient_name = self.patient.name if self.patient else "Unknown"
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'patient_name': patient_name,
            'result': self.result,
            'risk_level': self.risk_level,
            'created_at': self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else ''
        }
