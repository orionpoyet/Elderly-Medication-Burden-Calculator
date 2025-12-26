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

@app.route('/api/check-medication', methods=['POST'])
def check_medication_realtime():
    """
    Real-time medication checking with RxNorm integration
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
        
        warnings = []
        
        # ========== CHECK 0: RxNorm Normalization ==========
        normalized_name = RxNormAPI.normalize_drug_name(new_med_name)
        rxcui = RxNormAPI.get_rxcui(new_med_name)
        drug_classes = []
        
        if rxcui:
            drug_classes = RxNormAPI.get_drug_classes(rxcui)
            
            if normalized_name.lower() != new_med_name.lower():
                warnings.append({
                    "type": "normalization",
                    "severity": "info",
                    "icon": "🔍",
                    "title": "Drug Name Normalized",
                    "message": f"'{new_med_name}' → '{normalized_name}' (Standard name from RxNorm)",
                    "recommendation": "Using standardized name for accurate checking"
                })
        
        # ========== CHECK 1: Beers Criteria ==========
        from interaction_database import BEERS_CRITERIA
        if normalized_name in BEERS_CRITERIA:
            beers_info = BEERS_CRITERIA[normalized_name]
            warnings.append({
                "type": "beers_criteria",
                "severity": beers_info["risk"],
                "icon": "⚠️" if beers_info["risk"] == "moderate" else "🚨",
                "title": f"{normalized_name} - Potentially Inappropriate for Elderly",
                "message": beers_info["rationale"],
                "recommendation": beers_info["recommendation"],
                "category": beers_info["category"]
            })
        
        # ========== CHECK 2: Drug Interactions ==========
        for existing_med in existing_meds:
            existing_name = existing_med.get('name', '')
            if not existing_name:
                continue
                
            # Get normalized existing name
            existing_normalized = RxNormAPI.normalize_drug_name(existing_name)
            
            from interaction_database import check_interaction
            interaction = check_interaction(normalized_name, existing_normalized)
            if interaction:
                severity = interaction.get('severity', 'moderate')
                if severity in ['high', 'moderate']:
                    warnings.append({
                        "type": "interaction",
                        "severity": severity,
                        "icon": "🚨" if severity == "high" else "⚠️",
                        "title": f"Drug Interaction: {normalized_name} + {existing_normalized}",
                        "message": interaction.get('description', 'Interaction detected'),
                        "interacting_drug": existing_normalized,
                        "recommendation": "Consult healthcare provider before combining these medications"
                    })
        
        # ========== CHECK 3: Add Drug Class Information ==========
        if drug_classes:
            warnings.append({
                "type": "drug_class",
                "severity": "info",
                "icon": "🏷️",
                "title": "Drug Classification",
                "message": f"Classified as: {', '.join(drug_classes[:3])}",
                "recommendation": "Understanding drug class helps identify similar medications"
            })
        
        # ========== CHECK 4: Spelling Suggestions ==========
        spelling_suggestion = RxNormAPI.check_spelling(new_med_name)
        if spelling_suggestion and spelling_suggestion.lower() != new_med_name.lower():
            warnings.append({
                "type": "spelling",
                "severity": "info",
                "icon": "✏️",
                "title": "Spelling Suggestion",
                "message": f"Did you mean: '{spelling_suggestion}'?",
                "recommendation": "Correct spelling ensures accurate checking"
            })
        
        # ========== CHECK 5: Fall Risk Accumulation ==========
        from elderly_med_burden import FALL_RISK_DRUGS
        if normalized_name in FALL_RISK_DRUGS:
            fall_risk_count = sum(
                1 for med in existing_meds 
                if RxNormAPI.normalize_drug_name(med.get('name', '')) in FALL_RISK_DRUGS
            )
            
            if fall_risk_count >= 1:
                total_fall_risk_meds = fall_risk_count + 1
                warnings.append({
                    "type": "fall_risk",
                    "severity": "high" if total_fall_risk_meds >= 3 else "moderate",
                    "icon": "⚠️",
                    "title": f"Fall Risk Medication #{total_fall_risk_meds}",
                    "message": f"This is the {ordinal(total_fall_risk_meds)} medication that increases fall risk. Multiple fall-risk medications compound the danger.",
                    "recommendation": "Consider fall prevention strategies and discuss alternatives with physician",
                    "total_fall_risk_meds": total_fall_risk_meds
                })
            else:
                warnings.append({
                    "type": "fall_risk",
                    "severity": "low",
                    "icon": "ℹ️",
                    "title": "Fall Risk Medication",
                    "message": f"{normalized_name} may increase fall risk in elderly patients.",
                    "recommendation": "Monitor for dizziness, drowsiness, or balance issues"
                })
        
        # ========== CHECK 6: Anticholinergic Burden ==========
        from elderly_med_burden import ANTICHOLINERGIC_BURDEN
        if normalized_name in ANTICHOLINERGIC_BURDEN:
            anticholinergic_score = ANTICHOLINERGIC_BURDEN[normalized_name]
            
            existing_burden = sum(
                ANTICHOLINERGIC_BURDEN.get(RxNormAPI.normalize_drug_name(med.get('name', '')), 0)
                for med in existing_meds
            )
            
            new_total = existing_burden + anticholinergic_score
            
            if new_total >= 3:
                warnings.append({
                    "type": "anticholinergic",
                    "severity": "high",
                    "icon": "🧠",
                    "title": "High Anticholinergic Burden",
                    "message": f"Adding {normalized_name} increases total anticholinergic burden to {new_total}. High burden associated with cognitive impairment, confusion, and increased fall risk.",
                    "recommendation": "Consider alternatives with lower anticholinergic effects",
                    "anticholinergic_score": anticholinergic_score,
                    "new_total": new_total
                })
        
        # ========== CHECK 7: High Pill Burden ==========
        total_existing_pills = sum(med.get('doses_per_day', 1) for med in existing_meds)
        if total_existing_pills >= 10:
            warnings.append({
                "type": "pill_burden",
                "severity": "moderate",
                "icon": "💊",
                "title": "High Pill Burden",
                "message": f"Patient already takes {total_existing_pills} pills per day. Adding more medications increases complexity and reduces adherence.",
                "recommendation": "Consider if this medication is essential or if existing medications could be simplified"
            })
        
        # Sort warnings by severity (high first, then moderate, then low, then info)
        severity_order = {"high": 0, "moderate": 1, "low": 2, "info": 3}
        warnings.sort(key=lambda w: severity_order.get(w.get("severity", "info"), 3))
        
        return jsonify({
            "success": True,
            "warnings": warnings,
            "rxnorm_data": {
                "normalized_name": normalized_name,
                "rxcui": rxcui,
                "drug_classes": drug_classes,
                "is_normalized": normalized_name.lower() != new_med_name.lower()
            },
            "safe": len([w for w in warnings if w['severity'] in ['high', 'moderate']]) == 0
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
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