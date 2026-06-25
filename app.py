import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from models import db
import dal
import services
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'liver_monitor.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

UPLOAD_FOLDER = os.path.join(basedir, 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

db.init_app(app)

with app.app_context():
    # Force schema update for Sprint 2
    print("Resetting database for Sprint 2 upgrade...")
    db.drop_all() 
    db.create_all()

# --- AUTH ---
@app.route('/login', methods=['POST'])
def login():
    data = request.json or {}
    email = data.get('email', '')
    password = data.get('password', '')

    user = dal.get_user_by_email(email)
    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid credentials"}), 401
    
    return jsonify({"message": "Login successful", "token": "dummy-token-123", "user": user.to_dict()}), 200

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json or {}
    email = data.get('email', '')
    password = data.get('password', '')
    name = data.get('full_name', '')
    role = data.get('specialization', 'Hepatologist')

    if dal.get_user_by_email(email):
        return jsonify({"error": "Email already exists"}), 409
    
    user = dal.create_user(name, email, password, role)
    return jsonify({"message": "Registration successful", "user": user.to_dict()}), 201

# --- PROFILE ---
@app.route('/profile', methods=['GET'])
def get_profile():
    # For now, return the first user or mock
    users = db.session.query(db.Model.metadata.tables['users']).all() # Use raw or DAL if needed
    # Better: return based on token (dummy for now)
    user = dal.db.session.query(dal.User).first()
    return jsonify(user.to_dict() if user else {"name": "Unknown"}), 200

@app.route('/update_profile', methods=['POST'])
def update_profile():
    data = request.json or {}
    user = dal.db.session.query(dal.User).first()
    if user:
        updated = dal.update_user(user.id, data.get('full_name'), data.get('email'), data.get('specialization'))
        return jsonify(updated.to_dict()), 200
    return jsonify({"error": "User not found"}), 404

# --- ALERTS ---
@app.route('/alerts', methods=['GET'])
def get_alerts():
    filter_type = request.args.get('filter', 'all')
    alerts = dal.get_all_alerts(filter_type)
    return jsonify([a.to_dict() for a in alerts]), 200

@app.route('/resolve_alert', methods=['POST'])
def resolve_alert():
    data = request.json or {}
    a = dal.update_alert_status(data.get('id'), 'resolved')
    return jsonify({"message": "success", "alert": a.to_dict() if a else {}}), 200 if a else 404

# --- PATIENTS ---
@app.route('/patients', methods=['GET'])
def get_patients():
    records = services.get_patient_records_service()
    return jsonify(records), 200

@app.route('/add_patient', methods=['POST'])
def add_patient():
    data = request.json or {}
    patient, error = services.add_patient_service(
        data.get('name'), data.get('patient_id'), # patient_id maps to mrn
        data.get('age'), data.get('gender'),
        data.get('bp'), data.get('heart_rate'),
        data.get('spo2', 98), data.get('temperature')
    )
    if error:
        return jsonify({"error": error}), 400
    return jsonify({"message": "Patient recorded successfully!", "patient": patient.to_dict()}), 201

@app.route('/patients/<mrn>', methods=['DELETE'])
def delete_patient(mrn):
    success = dal.delete_patient(mrn)
    if success:
        return jsonify({"message": "Patient deleted successfully"}), 200
    return jsonify({"error": "Patient not found"}), 404

@app.route('/dashboard/stats', methods=['GET'])
def get_dashboard_stats():
    stats = services.get_dashboard_stats()
    return jsonify(stats), 200

# --- UPLOADS & VITALS ---
@app.route('/save_vitals', methods=['POST'])
def save_vitals():
    data = request.json or {}
    p = dal.get_patient_by_mrn(data.get('patient_id'))
    if not p:
        return jsonify({"error": "Patient not found"}), 404
    
    dal.add_vital(p.id, data.get('bp'), data.get('heart_rate'), data.get('oxygen'), data.get('temperature'))
    services.evaluate_vitals_and_alert(p.id, data.get('bp'), data.get('heart_rate'), data.get('oxygen'))
    return jsonify({"message": "Vitals saved successfully!"}), 200

@app.route('/upload_report', methods=['POST'])
def upload_report():
    if 'file' not in request.files: return jsonify({"error": "No file"}), 400
    file = request.files['file']
    patient_id = request.form.get('patient_id') # MRN
    
    if file:
        filename = secure_filename(file.filename)
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(path)
        
        p = dal.get_patient_by_mrn(patient_id)
        if p:
            dal.add_report(p.id, path, 'medical_report')
        return jsonify({"message": "File uploaded!", "path": path}), 200

@app.route('/analyze_condition', methods=['POST'])
def analyze_condition():
    data = request.json or {}
    p = dal.get_patient_by_mrn(data.get('patient_id'))
    if not p: return jsonify({"error": "Patient not found"}), 400

    # Logic for analysis (mocked for now but saves to DB)
    result = {
        "risk_level": "Monitoring",
        "summary": "Moderate progression detected.",
        "recommendations": ["Monitor weekly", "Check enzymes"]
    }
    import json
    dal.add_analysis_history(p.id, json.dumps(result), "Monitoring")
    return jsonify(result), 200

@app.route('/history', methods=['GET'])
def get_history():
    history = dal.get_all_analysis_history()
    return jsonify([h.to_dict() for h in history]), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
