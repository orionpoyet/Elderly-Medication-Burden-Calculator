# main.py - Elder Med Manager
# Medication Burden Calculator for Elderly Patients (65+)

from core.cognitive_load import calculate_mcls
from core.interaction_score import calculate_dir_score_from_list
from interaction_database import check_interaction, normalize_drug_name
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
import os
import csv
from datetime import datetime

# Create reports directory if it doesn't exist
REPORTS_DIR = "reports"
if not os.path.exists(REPORTS_DIR):
    os.makedirs(REPORTS_DIR)

DISCLAIMER = """
================================================================================
                    ELDER MED MANAGER - EDUCATIONAL TOOL
================================================================================
This tool is specifically designed for assessing medication burden in 
ELDERLY PATIENTS (age 65+) and is for EDUCATIONAL PURPOSES ONLY.

⚠️  CRITICAL DISCLAIMERS:
- This is NOT a substitute for professional medical advice
- Do NOT stop or change medications without consulting a doctor
- Medication decisions for elderly patients require comprehensive assessment
- Tool based on 2023 AGS Beers Criteria and geriatric pharmacology literature

ALWAYS consult with:
- The patient's physician
- A clinical pharmacist
- A geriatric specialist for complex cases

For emergency situations, call 911 or go to the nearest emergency room.
================================================================================
"""

def get_patient_info():
    """Collect patient information"""
    print("\n" + "="*80)
    print("PATIENT INFORMATION")
    print("="*80)
    
    while True:
        try:
            age = int(input("\nPatient age: ").strip())
            if age < 65:
                print("⚠️  This tool is specifically designed for patients 65 and older.")
                confirm = input("Continue anyway? (yes/no): ").strip().lower()
                if confirm != "yes":
                    continue
            if age > 120:
                print("Please enter a valid age.")
                continue
            break
        except ValueError:
            print("Please enter a valid number for age.")
    
    cognitive_impairment = input("\nDoes patient have cognitive impairment (dementia, MCI)? (yes/no): ").strip().lower() == "yes"
    
    caregiver_present = input("Is there a caregiver managing medications? (yes/no): ").strip().lower() == "yes"
    
    return {
        "age": age,
        "cognitive_impairment": cognitive_impairment,
        "caregiver_present": caregiver_present
    }

def filter_interactions(meds):
    """Check interactions using local database"""
    interactions = []
    
    print("\n" + "="*80)
    print("CHECKING DRUG INTERACTIONS")
    print("="*80)
    
    checked_pairs = 0
    for i, med1 in enumerate(meds):
        for med2 in meds[i+1:]:
            checked_pairs += 1
            interaction = check_interaction(med1["name"], med2["name"])
            if interaction:
                print(f"⚠️  INTERACTION: {med1['name']} + {med2['name']}")
                interactions.append((
                    med1["name"],
                    med2["name"],
                    interaction["severity"]
                ))
            else:
                print(f"   ✓ No known interaction: {med1['name']} + {med2['name']}")
    
    print(f"\n📊 Checked {checked_pairs} drug pair(s), found {len(interactions)} interaction(s)")
    
    return interactions

def print_daily_schedule(schedule):
    """Print visual daily medication schedule"""
    print("\n" + "="*80)
    print("📅 DAILY MEDICATION SCHEDULE")
    print("="*80)
    
    for time_slot, medications in schedule.items():
        if medications:
            print(f"\n{time_slot}")
            print("-" * 40)
            for med in medications:
                print(f"  💊 {med}")
        else:
            print(f"\n{time_slot}")
            print("-" * 40)
            print("  (none)")
    
    print("\n💡 TIP: Use a pill organizer to prepare medications weekly")
    print("💡 TIP: Set phone alarms for each medication time")

def generate_comprehensive_report(patient_info, meds, dir_triggers, mcls_score, mcls_burden, mcls_explanation):
    """Generate comprehensive elderly medication burden report"""
    
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
    
    # Print comprehensive report
    print("\n" + "="*80)
    print("🏥 COMPREHENSIVE ELDERLY MEDICATION BURDEN ASSESSMENT")
    print("="*80)
    
    # Patient Summary
    print(f"\n📋 PATIENT SUMMARY")
    print("-" * 80)
    print(f"Age: {patient_info['age']} years")
    print(f"Cognitive Impairment: {'Yes' if patient_info['cognitive_impairment'] else 'No'}")
    print(f"Caregiver Present: {'Yes' if patient_info['caregiver_present'] else 'No'}")
    
    # Medication Overview
    print(f"\n💊 MEDICATION OVERVIEW")
    print("-" * 80)
    print(f"Total Medications: {total_meds}")
    print(f"Total Pills Per Day: {total_pills}")
    print(f"Memory Actions Required Per Day: {memory_actions}")
    print(f"Pill Burden Level: {pill_burden_level}")
    print(f"Assessment: {pill_concern}")
    
    # Adherence Prediction
    print(f"\n📊 PREDICTED MEDICATION ADHERENCE")
    print("-" * 80)
    print(f"Estimated Adherence: {adherence_prediction}%")
    if adherence_prediction >= 80:
        print("✓ Good - Regimen is manageable")
    elif adherence_prediction >= 60:
        print("⚠️  Fair - Consider simplification strategies")
    else:
        print("❌ Poor - High risk of non-adherence, urgent simplification needed")
    
    if not patient_info['caregiver_present'] and adherence_prediction < 70:
        print("\n⚠️  WARNING: Low predicted adherence without caregiver support")
        print("   Recommend involving family member or home care services")
    
    # Beers Criteria Violations
    print(f"\n🚨 BEERS CRITERIA ASSESSMENT (Potentially Inappropriate Medications)")
    print("-" * 80)
    if beers_violations:
        print(f"⚠️  {len(beers_violations)} POTENTIALLY INAPPROPRIATE MEDICATION(S) IDENTIFIED:\n")
        for violation in beers_violations:
            print(f"❌ {violation['drug'].upper()}")
            print(f"   Category: {violation['details']['category']}")
            print(f"   Risk Level: {violation['details']['risk'].upper()}")
            print(f"   Why Inappropriate: {violation['details']['rationale']}")
            print(f"   Recommendation: {violation['details']['recommendation']}")
            print()
    else:
        print("✓ No Beers Criteria violations detected")
    
    # Fall Risk Assessment
    print(f"\n⚠️  FALL RISK ASSESSMENT")
    print("-" * 80)
    print(f"Fall Risk Score: {fall_risk_score}/10")
    print(f"Fall Risk Category: {fall_risk_category}")
    if fall_risk_meds:
        print(f"\nMedications Contributing to Fall Risk:")
        for med, risk_level in fall_risk_meds:
            print(f"  • {med} ({risk_level} risk)")
        print("\n💡 FALL PREVENTION RECOMMENDATIONS:")
        print("   - Remove tripping hazards in home")
        print("   - Install grab bars in bathroom")
        print("   - Ensure adequate lighting, especially at night")
        print("   - Consider physical therapy for balance training")
        print("   - Review medications with doctor for possible alternatives")
    else:
        print("✓ No specific fall-risk medications identified")
    
    # Anticholinergic Burden
    print(f"\n🧠 ANTICHOLINERGIC BURDEN")
    print("-" * 80)
    print(f"Total Anticholinergic Score: {anticholinergic_score}")
    if anticholinergic_score >= 3:
        print("❌ HIGH - Significant risk of cognitive impairment, confusion, falls")
        print("   Action: Urgent medication review recommended")
    elif anticholinergic_score >= 2:
        print("⚠️  MODERATE - Monitor for cognitive changes")
    elif anticholinergic_score >= 1:
        print("⚠️  LOW - Minimal concern, but monitor")
    else:
        print("✓ NONE - No significant anticholinergic burden")
    
    if anticholinergic_contributors:
        print(f"\nContributing Medications:")
        for med, score in anticholinergic_contributors:
            print(f"  • {med} (score: {score})")
    
    # Cognitive Load Score
    print(f"\n🧮 MEDICATION COGNITIVE LOAD SCORE (MCLS)")
    print("-" * 80)
    print(f"Score: {mcls_score}")
    print(f"Burden Level: {mcls_burden}")
    print(f"Explanation: {mcls_explanation}")
    
    # Drug Interactions
    print(f"\n⚗️  DRUG INTERACTION RISK SCORE (DIRS)")
    print("-" * 80)
    print(f"Score: {dir_score}")
    print(f"Risk Level: {dir_risk}")
    
    if dir_triggers:
        print(f"\n⚠️  {len(dir_triggers)} INTERACTION(S) DETECTED:")
        for idx, (a, b, severity) in enumerate(dir_triggers, 1):
            interaction_detail = check_interaction(a, b)
            print(f"\n{idx}. {a.upper()} + {b.upper()}")
            print(f"   Severity: {severity.upper()}")
            if interaction_detail:
                print(f"   Details: {interaction_detail['description']}")
    else:
        print("✓ No interactions detected in database")
    
    # Daily Schedule
    print_daily_schedule(schedule)
    
    # Simplification Recommendations
    if simplification_recs:
        print(f"\n💡 SIMPLIFICATION RECOMMENDATIONS")
        print("="*80)
        for rec in simplification_recs:
            print(rec)
    
    # Overall Risk Summary
    print(f"\n🎯 OVERALL RISK SUMMARY")
    print("="*80)
    
    risk_factors = []
    if beers_violations:
        risk_factors.append(f"❌ {len(beers_violations)} Beers Criteria violation(s)")
    if fall_risk_category in ["HIGH", "MODERATE"]:
        risk_factors.append(f"⚠️  {fall_risk_category} fall risk")
    if anticholinergic_score >= 3:
        risk_factors.append(f"❌ High anticholinergic burden (score: {anticholinergic_score})")
    if adherence_prediction < 70:
        risk_factors.append(f"⚠️  Low predicted adherence ({adherence_prediction}%)")
    if total_pills >= 10:
        risk_factors.append(f"⚠️  High pill burden ({total_pills} pills/day)")
    if len(dir_triggers) >= 2:
        risk_factors.append(f"⚠️  Multiple drug interactions ({len(dir_triggers)})")
    
    if risk_factors:
        print("⚠️  KEY CONCERNS IDENTIFIED:")
        for factor in risk_factors:
            print(f"   {factor}")
        print("\n🏥 RECOMMENDATION: Comprehensive medication review with physician or clinical pharmacist STRONGLY advised")
    else:
        print("✓ Medication regimen appears reasonable for elderly patient")
        print("💡 Continue regular medication reviews (at least annually)")
    
    # Action Items
    print(f"\n📋 RECOMMENDED NEXT STEPS")
    print("="*80)
    print("1. Schedule medication review with physician or clinical pharmacist")
    print("2. Discuss Beers Criteria violations and possible alternatives")
    print("3. Implement fall prevention strategies if applicable")
    print("4. Consider simplification opportunities to improve adherence")
    print("5. Set up medication organizer and/or caregiver support if needed")
    print("6. Monitor for side effects, especially confusion, dizziness, falls")
    print("7. Review this assessment with all healthcare providers")
    
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
        "dir_score": dir_score,
        "dir_risk": dir_risk,
        "schedule": schedule,
        "simplification_recs": simplification_recs,
        "risk_factors": risk_factors
    }

def export_detailed_report(report_data, meds, dir_triggers):
    """Export comprehensive CSV report"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_filename = f"elderly_med_report_{timestamp}.csv"
    report_path = os.path.join(REPORTS_DIR, report_filename)  # Changed this line
    
    with open(report_path, mode="w", newline="", encoding="utf-8") as f:  # Changed this line
        writer = csv.writer(f)
        
        # Header
        writer.writerow(["ELDER MED MANAGER - COMPREHENSIVE REPORT"])
        writer.writerow(["Generated:", datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
        writer.writerow([])
        
        # Patient Info
        writer.writerow(["PATIENT INFORMATION"])
        writer.writerow(["Age", report_data["patient_info"]["age"]])
        writer.writerow(["Cognitive Impairment", "Yes" if report_data["patient_info"]["cognitive_impairment"] else "No"])
        writer.writerow(["Caregiver Present", "Yes" if report_data["patient_info"]["caregiver_present"] else "No"])
        writer.writerow([])
        
        # Medications
        writer.writerow(["CURRENT MEDICATIONS"])
        writer.writerow(["Medication", "Doses Per Day"])
        for med in meds:
            writer.writerow([med["name"], med["doses_per_day"]])
        writer.writerow([])
        
        # Summary Metrics
        writer.writerow(["BURDEN ASSESSMENT"])
        writer.writerow(["Metric", "Value", "Assessment"])
        writer.writerow(["Total Medications", report_data["total_meds"], ""])
        writer.writerow(["Total Pills Per Day", report_data["total_pills"], report_data["pill_burden_level"]])
        writer.writerow(["Predicted Adherence", f"{report_data['adherence_prediction']}%", ""])
        writer.writerow(["Fall Risk Score", f"{report_data['fall_risk_score']}/10", report_data["fall_risk_category"]])
        writer.writerow(["Anticholinergic Burden", report_data["anticholinergic_score"], ""])
        writer.writerow(["MCLS Score", report_data["mcls_score"], report_data["mcls_burden"]])
        writer.writerow(["DIRS Score", report_data["dir_score"], report_data["dir_risk"]])
        writer.writerow([])
        
        # Beers Criteria
        writer.writerow(["BEERS CRITERIA VIOLATIONS"])
        if report_data["beers_violations"]:
            writer.writerow(["Medication", "Category", "Risk Level", "Rationale", "Recommendation"])
            for violation in report_data["beers_violations"]:
                writer.writerow([
                    violation["drug"],
                    violation["details"]["category"],
                    violation["details"]["risk"],
                    violation["details"]["rationale"],
                    violation["details"]["recommendation"]
                ])
        else:
            writer.writerow(["No Beers Criteria violations detected"])
        writer.writerow([])
        
        # Daily Schedule
        writer.writerow(["DAILY MEDICATION SCHEDULE"])
        writer.writerow(["Time", "Medications"])
        for time_slot, medications in report_data["schedule"].items():
            med_list = ", ".join(medications) if medications else "(none)"
            writer.writerow([time_slot, med_list])
        writer.writerow([])
        
        # Interactions
        writer.writerow(["DRUG INTERACTIONS"])
        if dir_triggers:
            writer.writerow(["Drug 1", "Drug 2", "Severity", "Description"])
            for a, b, severity in dir_triggers:
                interaction_detail = check_interaction(a, b)
                desc = interaction_detail['description'] if interaction_detail else "N/A"
                writer.writerow([a, b, severity, desc])
        else:
            writer.writerow(["No interactions detected in database"])
        writer.writerow([])
        
        # Recommendations
        writer.writerow(["SIMPLIFICATION RECOMMENDATIONS"])
        for rec in report_data["simplification_recs"]:
            writer.writerow([rec])
        writer.writerow([])
        
        # Risk Summary
        writer.writerow(["KEY RISK FACTORS"])
        for factor in report_data["risk_factors"]:
            writer.writerow([factor])
        writer.writerow([])
        
        # Disclaimer
        writer.writerow(["DISCLAIMER"])
        writer.writerow(["This is an educational tool only. All medication changes must be made in consultation with healthcare professionals."])
    
    return report_path

def save_console_output_to_file(output_text):
    """Save console output to a text file in the reports folder"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"console_output_{timestamp}.txt"
    output_path = os.path.join(REPORTS_DIR, output_filename)
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(output_text)
    
    return output_path

def main():
    import sys
    from io import StringIO
    
    print(DISCLAIMER)
    
    # Get patient information (show these prompts directly)
    patient_info = get_patient_info()
    
    # Get medications (show these prompts directly)
    meds = []
    
    while True:
        try:
            num_meds = int(input("\nHow many medications is the patient taking? "))
            if num_meds <= 0:
                raise ValueError
            if num_meds > 25:
                print("⚠️  More than 25 medications is extremely high. Please verify count.")
                confirm = input("Continue? (yes/no): ").strip().lower()
                if confirm != "yes":
                    continue
            break
        except ValueError:
            print("Please enter a valid positive integer.")
    
    print("\n💡 TIP: Include ALL medications: prescriptions, over-the-counter, vitamins, supplements")
    print("💡 TIP: You can enter brand names (e.g., 'Tylenol') or generic names (e.g., 'acetaminophen')")
    
    for i in range(num_meds):
        print(f"\n{'='*60}")
        print(f"Medication {i+1} of {num_meds}")
        print('='*60)
        while True:
            name = input("Name: ").strip()
            if name:
                break
            print("Medication name cannot be empty.")
        while True:
            try:
                doses_per_day = int(input("How many times per day? ").strip())
                if doses_per_day <= 0:
                    raise ValueError
                if doses_per_day > 6:
                    print("⚠️  More than 6 times per day is unusual. Please verify.")
                    confirm = input("Continue? (yes/no): ").strip().lower()
                    if confirm != "yes":
                        continue
                break
            except ValueError:
                print("Please enter a valid positive integer.")
        
        meds.append({
            "name": name,
            "doses_per_day": doses_per_day,
            "sedative": False,
            "anticholinergic": False,
            "rxcui": None
        })
    
    # Create a string buffer to capture all output AFTER user input
    output_buffer = StringIO()
    
    # Redirect stdout to buffer (AFTER getting all user input)
    original_stdout = sys.stdout
    sys.stdout = output_buffer
    
    try:
        # Check interactions
        dir_triggers = filter_interactions(meds)
        
        # Calculate MCLS
        mcls_score, mcls_burden, mcls_explanation = calculate_mcls(meds)
        
        # Generate comprehensive report
        report_data = generate_comprehensive_report(
            patient_info, meds, dir_triggers, 
            mcls_score, mcls_burden, mcls_explanation
        )
        
        # Export to CSV
        report_file = export_detailed_report(report_data, meds, dir_triggers)
        
        print(f"\n{'='*80}")
        print(f"📄 Detailed report exported to: {report_file}")
        print("="*80)
        
        print("\n" + "="*80)
        print("⚠️  IMPORTANT REMINDERS")
        print("="*80)
        print("• Share this report with patient's healthcare team")
        print("• Do NOT make medication changes without professional consultation")
        print("• This tool is for educational and assessment purposes only")
        print("• Regular medication reviews are essential for elderly patients")
        print("="*80)
        
    finally:
        # Restore original stdout
        sys.stdout = original_stdout
        
        # Get the captured output
        console_output = output_buffer.getvalue()
        
        # Print it to console
        print(console_output)
        
        # Save it to file
        console_file = save_console_output_to_file(console_output)
        print(f"\n📄 Console output saved to: {console_file}")


if __name__ == "__main__":
    main()