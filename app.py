from flask import Flask, render_template, request, jsonify, send_file, session
from datetime import datetime
import os
import json
import sys

# Add your existing modules to path
sys.path.append('.')

from core.cognitive_load import calculate_mcls
from core.interaction_score import calculate_dir_score_from_list
from interaction_database import check_interaction
from elderly_med_burden import (
    assess_beers_criteria,
    calculate_fall_risk,
    generate_daily_schedule,
    calculate_pill_burden,
    predict_adherence,
    calculate_anticholinergic_burden,
    generate_simplification_recommendations,
    calculate_memory_actions_per_day
)

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Ensure reports folder exists
REPORTS_DIR = 'reports'
if not os.path.exists(REPORTS_DIR):
    os.makedirs(REPORTS_DIR)

# ==================== ROUTES ====================

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/analyze')
def analyze_page():
    """Analyze medications page"""
    return render_template('analyze.html')

@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')

@app.route('/contact')
def contact():
    """Contact page"""
    return render_template('contact.html')

@app.route('/api/analyze', methods=['POST'])
def analyze_api():
    """API endpoint for analysis"""
    try:
        data = request.json
        patient_info = {
            "age": int(data.get('age', 65)),
            "cognitive_impairment": data.get('cognitive_impairment', False),
            "caregiver_present": data.get('caregiver_present', False)
        }
        
        medications = data.get('medications', [])
        
        # Convert medication format
        meds = []
        for med in medications:
            meds.append({
                "name": med.get('name', ''),
                "doses_per_day": int(med.get('doses_per_day', 1)),
                "sedative": False,
                "anticholinergic": False,
                "rxcui": None
            })
        
        # Run analysis
        dir_triggers = filter_interactions_web(meds)
        mcls_score, mcls_burden, mcls_explanation = calculate_mcls(meds)
        
        # Generate report
        report_data = generate_comprehensive_report_web(
            patient_info, meds, dir_triggers, 
            mcls_score, mcls_burden, mcls_explanation
        )
        
        # Store in session for PDF generation
        session['last_report'] = report_data
        session['last_meds'] = medications
        session['last_dir_triggers'] = dir_triggers
        
        return jsonify({
            "success": True,
            "report": report_data
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400

@app.route('/api/export/pdf')
def export_pdf():
    """Generate PDF report"""
    try:
        # Check if we have a PDF generator
        from utils.pdf_generator import generate_pdf_report
        report_data = session.get('last_report', {})
        if not report_data:
            return jsonify({"error": "No report data found"}), 400
            
        pdf_path = generate_pdf_report(report_data)
        return send_file(pdf_path, as_attachment=True)
        
    except ImportError:
        return jsonify({"error": "PDF generation not available"}), 501
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/export/csv')
def export_csv():
    """Generate CSV report"""
    try:
        report_data = session.get('last_report', {})
        meds = session.get('last_meds', [])
        dir_triggers = session.get('last_dir_triggers', [])
        
        csv_path = export_detailed_report_web(report_data, meds, dir_triggers)
        return send_file(csv_path, as_attachment=True)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

# ==================== HELPER FUNCTIONS ====================

def filter_interactions_web(meds):
    """Check interactions - web version"""
    interactions = []
    for i, med1 in enumerate(meds):
        for med2 in meds[i+1:]:
            interaction = check_interaction(med1["name"], med2["name"])
            if interaction:
                interactions.append((
                    med1["name"],
                    med2["name"],
                    interaction["severity"]
                ))
    return interactions

def generate_comprehensive_report_web(patient_info, meds, dir_triggers, mcls_score, mcls_burden, mcls_explanation):
    """Generate report for web"""
    # Calculate all metrics
    beers_violations = assess_beers_criteria(meds)
    fall_risk_score, fall_risk_category, fall_risk_meds = calculate_fall_risk(meds, patient_info["age"])
    schedule = generate_daily_schedule(meds)
    total_pills, total_meds, pill_burden_level, pill_concern = calculate_pill_burden(meds)
    adherence_prediction = predict_adherence(meds, patient_info["age"], patient_info["cognitive_impairment"])
    anticholinergic_score, anticholinergic_contributors = calculate_anticholinergic_burden(meds)
    simplification_recs = generate_simplification_recommendations(meds)
    memory_actions = calculate_memory_actions_per_day(meds)
    dir_score, dir_risk = calculate_dir_score_from_list(dir_triggers)
    
    return {
        "patient_info": patient_info,
        "total_pills": total_pills,
        "total_meds": total_meds,
        "pill_burden_level": pill_burden_level,
        "adherence_prediction": adherence_prediction,
        "beers_violations": beers_violations,
        "fall_risk_score": fall_risk_score,
        "fall_risk_category": fall_risk_category,
        "anticholinergic_score": anticholinergic_score,
        "mcls_score": mcls_score,
        "mcls_burden": mcls_burden,
        "mcls_explanation": mcls_explanation,
        "dir_score": dir_score,
        "dir_risk": dir_risk,
        "dir_triggers": dir_triggers,
        "schedule": schedule,
        "simplification_recs": simplification_recs,
        "memory_actions": memory_actions
    }

def export_detailed_report_web(report_data, meds, dir_triggers):
    """Export CSV - web version"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_filename = f"elderly_med_report_{timestamp}.csv"
    report_path = os.path.join(REPORTS_DIR, report_filename)
    
    # Your existing CSV generation code here
    import csv
    with open(report_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["ELDER MED MANAGER - COMPREHENSIVE REPORT"])
        writer.writerow(["Generated:", datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
        writer.writerow([])
        writer.writerow(["PATIENT INFORMATION"])
        writer.writerow(["Age", report_data["patient_info"]["age"]])
        writer.writerow(["Cognitive Impairment", "Yes" if report_data["patient_info"]["cognitive_impairment"] else "No"])
        writer.writerow(["Caregiver Present", "Yes" if report_data["patient_info"]["caregiver_present"] else "No"])
    
    return report_path

# ==================== TEMPLATE PAGES ====================

@app.route('/templates/<template_name>')
def serve_template(template_name):
    """Serve template files directly (for debugging)"""
    return render_template(template_name)

# ==================== MAIN ====================

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)