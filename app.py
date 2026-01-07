from flask import Flask, render_template, request, jsonify, send_file, session
from datetime import datetime
import os
import json
import sys
# Add this line with other imports
from external_apis import RxNormAPI



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

@app.route('/analyze')  # This is the URL
def analyze_page():      # This is the function name
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

#added after app.route('/contact') and before app.rout('/api/analye')
@app.route('/api/check-medication', methods=['POST'])
def check_medication_realtime():
    """
    Real-time medication checking endpoint
    Checks a single medication against existing medications for immediate warnings
    """
    try:
        data = request.json
        
        # Get the medication being checked
        new_med_name = data.get('medication_name', '').strip()
        existing_meds = data.get('existing_medications', [])
        patient_age = int(data.get('age', 65))
        
        if not new_med_name:
            return jsonify({
                "success": True,
                "warnings": [],
                "safe": True
            })
        
        # Import necessary functions
        from interaction_database import (
            check_interaction, 
            normalize_drug_name,
            get_drug_profile,
            DRUG_PROFILES
        )
        from elderly_med_burden import BEERS_CRITERIA, FALL_RISK_DRUGS
        
        warnings = []
        normalized_name = normalize_drug_name(new_med_name)
        
        # Check if drug exists in database
        drug_profile = get_drug_profile(new_med_name)
        
        if not drug_profile:
            warnings.append({
                "severity": "low",
                "icon": "❔",
                "title": "Unknown Medication",
                "message": f'"{new_med_name}" is not in our database. This doesn\'t mean it\'s unsafe.',
                "recommendation": "Verify spelling or try the generic name.",
                "category": "Database Coverage"
            })
            return jsonify({
                "success": True,
                "warnings": warnings,
                "safe": False
            })
        
        # ========== CHECK 1: Drug Interactions (MOST IMPORTANT) ==========
        for existing_med in existing_meds:
            existing_name = existing_med.get('name', '')
            if not existing_name:
                continue
                
            interaction = check_interaction(new_med_name, existing_name)
            
            if interaction:
                severity = interaction.get('severity', 'moderate')
                
                # Icon mapping
                icon_map = {
                    'critical': '🚨',
                    'high': '⚠️',
                    'moderate': '⚡',
                    'low': 'ℹ️'
                }
                
                warnings.append({
                    "severity": severity,
                    "icon": icon_map.get(severity, '⚠️'),
                    "title": f"Interaction: {new_med_name} + {existing_name}",
                    "message": interaction.get('description', 'Drug interaction detected'),
                    "recommendation": interaction.get('action', 'Consult physician before combining'),
                    "category": "Drug-Drug Interaction"
                })
        
        # ========== CHECK 2: Beers Criteria ==========
        if drug_profile.beers_criteria and patient_age >= 65:
            warnings.append({
                "severity": "high",
                "icon": "🚫",
                "title": "Beers Criteria - Potentially Inappropriate",
                "message": f"{drug_profile.generic_name.title()} is flagged as potentially inappropriate for elderly patients.",
                "recommendation": "Discuss alternatives with prescriber. These medications often have safer options.",
                "category": "Beers Criteria"
            })
        
        # ========== CHECK 3: Fall Risk ==========
        if drug_profile.fall_risk_score >= 7:
            warnings.append({
                "severity": "high",
                "icon": "🏥",
                "title": "High Fall Risk",
                "message": f"{drug_profile.generic_name.title()} has very high fall risk (score: {drug_profile.fall_risk_score}/10).",
                "recommendation": "Implement fall prevention: remove hazards, use grab bars, consider alternatives.",
                "category": "Fall Risk"
            })
        elif drug_profile.fall_risk_score >= 5:
            warnings.append({
                "severity": "moderate",
                "icon": "⚠️",
                "title": "Elevated Fall Risk",
                "message": f"{drug_profile.generic_name.title()} increases fall risk (score: {drug_profile.fall_risk_score}/10).",
                "recommendation": "Use caution with ambulation, especially at night.",
                "category": "Fall Risk"
            })
        
        # ========== CHECK 4: Anticholinergic Burden ==========
        if drug_profile.anticholinergic_score >= 3:
            warnings.append({
                "severity": "high",
                "icon": "🧠",
                "title": "Severe Anticholinergic Effects",
                "message": f"{drug_profile.generic_name.title()} has severe anticholinergic effects (3/3). Increases confusion and delirium risk.",
                "recommendation": "Consider non-anticholinergic alternatives. Monitor for confusion, dry mouth, urinary retention.",
                "category": "Anticholinergic"
            })
        elif drug_profile.anticholinergic_score >= 2:
            warnings.append({
                "severity": "moderate",
                "icon": "🧠",
                "title": "Moderate Anticholinergic Burden",
                "message": f"{drug_profile.generic_name.title()} has moderate anticholinergic effects ({drug_profile.anticholinergic_score}/3).",
                "recommendation": "Monitor for dry mouth, constipation, confusion.",
                "category": "Anticholinergic"
            })
        
        # ========== CHECK 5: Sedative Effects ==========
        if drug_profile.sedative_score >= 3:
            warnings.append({
                "severity": "high",
                "icon": "😴",
                "title": "High Sedation Risk",
                "message": f"{drug_profile.generic_name.title()} causes significant sedation (3/3). Increases fall risk.",
                "recommendation": "Take at bedtime only. Avoid nighttime ambulation. Use bedside commode.",
                "category": "Sedation"
            })
        elif drug_profile.sedative_score >= 2:
            warnings.append({
                "severity": "moderate",
                "icon": "😴",
                "title": "Moderate Sedation",
                "message": f"{drug_profile.generic_name.title()} may cause drowsiness ({drug_profile.sedative_score}/3).",
                "recommendation": "Be cautious with driving and activities requiring alertness.",
                "category": "Sedation"
            })
        
        # ========== CHECK 6: Renal Adjustment ==========
        if drug_profile.renal_adjustment:
            warnings.append({
                "severity": "moderate",
                "icon": "🩺",
                "title": "Renal Dose Adjustment Required",
                "message": f"{drug_profile.generic_name.title()} requires dose adjustment in kidney impairment.",
                "recommendation": "Ensure kidney function checked. Dose may need reduction.",
                "category": "Renal"
            })
        
        # Sort by severity (critical/high first)
        severity_order = {"critical": 0, "high": 1, "moderate": 2, "low": 3}
        warnings.sort(key=lambda w: severity_order.get(w.get("severity", "low"), 3))
        
        # Determine if safe (no high/critical warnings)
        has_critical = any(w['severity'] in ['critical', 'high'] for w in warnings)
        is_safe = len(warnings) == 0 or not has_critical
        
        return jsonify({
            "success": True,
            "warnings": warnings,
            "safe": is_safe,
            "drug_info": {
                "generic_name": drug_profile.generic_name,
                "drug_class": drug_profile.drug_class,
                "brand_names": drug_profile.brand_names
            }
        })
        
    except Exception as e:
        print(f"❌ Error in check_medication: {str(e)}")
        import traceback
        traceback.print_exc()
        
        return jsonify({
            "success": False,
            "error": str(e),
            "warnings": []
        }), 500


def ordinal(n):
    """Convert number to ordinal string (1 -> 1st, 2 -> 2nd, etc.)"""
    if 10 <= n % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
    return f"{n}{suffix}"

#end of change

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

@app.route('/api/drug-suggest')
def drug_suggest():
    """Drug name autocomplete using RxNorm"""
    query = request.args.get('q', '').strip()
    if len(query) < 2:
        return jsonify({"success": True, "suggestions": []})
    
    try:
        # Use RxNorm API for suggestions
        import requests
        url = f"https://rxnav.nlm.nih.gov/REST/spellingsuggestions.json?name={requests.utils.quote(query)}"
        response = requests.get(url, timeout=5)
        
        suggestions = []
        if response.status_code == 200:
            data = response.json()
            suggestion_list = data.get('suggestionGroup', {}).get('suggestionList', {}).get('suggestion', [])
            
            for suggestion in suggestion_list[:10]:
                rxcui = RxNormAPI.get_rxcui(suggestion)
                drug_type = "Unknown"
                
                if rxcui:
                    info = RxNormAPI.get_drug_info(rxcui)
                    for group in info:
                        if group.get('tty') == 'IN':
                            drug_type = "Generic"
                            break
                        elif group.get('tty') == 'BN':
                            drug_type = "Brand"
                            break
                
                suggestions.append({
                    "name": suggestion,
                    "type": drug_type,
                    "rxcui": rxcui
                })
        
        return jsonify({
            "success": True,
            "suggestions": suggestions,
            "query": query
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "suggestions": []
        })


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
    
    # Get custom times from patient_info if available
    custom_times = patient_info.get("custom_times", None)
    schedule = generate_daily_schedule(meds, custom_times)  # <-- UPDATED LINE
    
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