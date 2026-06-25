import dal
from datetime import datetime, timedelta

def calculate_status(bp_str, hr, spo2):
    """
    Input: bp (string "sys/dia"), hr (int), spo2 (float)
    Output: "stable", "monitoring", "critical"
    """
    try:
        sys, dia = map(int, bp_str.split('/'))
    except (ValueError, AttributeError):
        return "stable" # Default or handle error

    # Critical Rules
    if sys >= 160 or dia >= 100 or hr > 110:
        return "critical"
    
    # Monitoring Rules
    if sys >= 140 or dia >= 90 or hr > 95 or dia < 60:
        return "monitoring"
    
    return "stable"

def evaluate_vitals_and_alert(patient_id, bp, hr, spo2):
    status = calculate_status(bp, hr, spo2)
    
    # Check for duplicate alerts (active alerts of the same type within last hour)
    active_alerts = dal.get_active_alerts(patient_id)
    
    if status == "critical":
        has_critical = any(a.type == "CRITICAL" for a in active_alerts)
        if not has_critical:
            dal.add_alert(patient_id, "CRITICAL", "Patient vitals are in critical range. Immediate attention required.")
    
    elif status == "monitoring":
        has_warning = any(a.type == "WARNING" for a in active_alerts)
        if not has_warning:
            dal.add_alert(patient_id, "WARNING", "Patient requires monitoring due to abnormal vitals.")
            
    return status

def add_patient_service(name, mrn, age, gender, bp, hr, spo2, temperature):
    # 1. Check if MRN unique
    if dal.get_patient_by_mrn(mrn):
        return None, "MRN already exists"
    
    # 2. Create patient
    patient = dal.create_patient(name, mrn, age, gender)
    
    # 3. Add initial vitals
    dal.add_vital(patient.id, bp, hr, spo2, temperature)
    
    # 4. Update last visit
    patient.last_visit = datetime.utcnow()
    dal.db.session.commit()
    
    # 5. Evaluate and alert
    evaluate_vitals_and_alert(patient.id, bp, hr, spo2)
    
    return patient, None

def get_dashboard_stats():
    patients = dal.get_all_patients()
    total = len(patients)
    critical = 0
    monitoring = 0
    stable = 0
    
    for p in patients:
        latest = dal.get_latest_vital(p.id)
        if latest:
            status = calculate_status(latest.bp, latest.hr, latest.spo2)
            if status == "critical": critical += 1
            elif status == "monitoring": monitoring += 1
            else: stable += 1
        else:
            stable += 1
            
    return {
        "total_patients": total,
        "critical_count": critical,
        "monitoring_count": monitoring,
        "stable_count": stable,
        "risk_distribution": [stable, monitoring, critical],
        "treatment_distribution": [round(total * 0.8), round(total * 0.6), round(total * 0.4), round(total * 0.15)]
    }

def get_patient_records_service():
    patients = dal.get_all_patients()
    results = []
    for p in patients:
        pd = p.to_dict()
        latest = dal.get_latest_vital(p.id)
        if latest:
            pd['bp'] = latest.bp
            pd['hr'] = latest.hr
            pd['spo2'] = latest.spo2
            pd['status'] = calculate_status(latest.bp, latest.hr, latest.spo2)
        else:
            pd['bp'] = 'N/A'
            pd['hr'] = 'N/A'
            pd['spo2'] = 'N/A'
            pd['status'] = 'stable'
        results.append(pd)
    return results
