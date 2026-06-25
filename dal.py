from models import db, User, Patient, Vital, Alert, Report, AnalysisHistory

def get_user_by_email(email):
    return User.query.filter_by(email=email).first()

def create_user(name, email, raw_password, role='Hepatologist'):
    new_user = User(name=name, email=email, role=role)
    new_user.set_password(raw_password)
    db.session.add(new_user)
    db.session.commit()
    return new_user

def update_user(user_id, name, email, role):
    u = User.query.get(user_id)
    if u:
        u.name = name
        u.email = email
        u.role = role
        db.session.commit()
    return u

def get_all_patients():
    return Patient.query.all()

def get_patient_by_mrn(mrn):
    return Patient.query.filter_by(mrn=mrn).first()

def create_patient(name, mrn, age, gender, child_pugh=None):
    p = Patient(name=name, mrn=mrn, age=age, gender=gender, child_pugh=child_pugh)
    db.session.add(p)
    db.session.commit()
    return p

def delete_patient(mrn):
    p = Patient.query.filter_by(mrn=mrn).first()
    if p:
        db.session.delete(p)
        db.session.commit()
        return True
    return False

def add_vital(patient_id, bp, hr, spo2, temperature):
    v = Vital(patient_id=patient_id, bp=bp, hr=hr, spo2=spo2, temperature=temperature)
    db.session.add(v)
    db.session.commit()
    return v

def get_latest_vital(patient_id):
    return Vital.query.filter_by(patient_id=patient_id).order_by(Vital.recorded_at.desc()).first()

def add_alert(patient_id, alert_type, message):
    a = Alert(patient_id=patient_id, type=alert_type, message=message, status='active')
    db.session.add(a)
    db.session.commit()
    return a

def get_active_alerts(patient_id):
    return Alert.query.filter_by(patient_id=patient_id, status='active').all()

def get_all_alerts(filter_type='all'):
    if filter_type == 'all':
        return Alert.query.order_by(Alert.created_at.desc()).all()
    else:
        return Alert.query.filter_by(status=filter_type).order_by(Alert.created_at.desc()).all()

def update_alert_status(alert_id, status):
    a = Alert.query.get(alert_id)
    if a:
        a.status = status
        db.session.commit()
        return a
    return None

def add_report(patient_id, file_path, report_type):
    r = Report(patient_id=patient_id, file_path=file_path, type=report_type)
    db.session.add(r)
    db.session.commit()
    return r

def add_analysis_history(patient_id, result_json, risk_level):
    h = AnalysisHistory(patient_id=patient_id, result=result_json, risk_level=risk_level)
    db.session.add(h)
    db.session.commit()
    return h

def get_all_analysis_history():
    return AnalysisHistory.query.order_by(AnalysisHistory.created_at.desc()).all()
