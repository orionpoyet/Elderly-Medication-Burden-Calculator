# elderly_med_burden.py
# Elder-Specific Medication Burden Assessment

# ==================================================================================
# BEERS CRITERIA - Potentially Inappropriate Medications for Elderly
# ==================================================================================
# Based on 2023 AGS Beers Criteria

BEERS_CRITERIA = {
    # Anticholinergics - HIGH RISK
    "diphenhydramine": {
        "category": "Anticholinergic",
        "risk": "high",
        "rationale": "Highly anticholinergic; cognitive impairment, delirium, falls",
        "recommendation": "Avoid. Consider non-sedating antihistamines"
    },
    "dimenhydrinate": {
        "category": "Anticholinergic",
        "risk": "high",
        "rationale": "Anticholinergic effects, falls risk",
        "recommendation": "Avoid"
    },
    
    # Benzodiazepines - HIGH RISK
    "diazepam": {
        "category": "Benzodiazepine",
        "risk": "high",
        "rationale": "Increased fall risk, cognitive impairment, delirium. Long half-life",
        "recommendation": "Avoid. If needed for anxiety, consider short-acting alternatives"
    },
    "alprazolam": {
        "category": "Benzodiazepine",
        "risk": "high",
        "rationale": "Fall risk, cognitive impairment, dependence",
        "recommendation": "Avoid. Consider non-benzodiazepine alternatives"
    },
    "lorazepam": {
        "category": "Benzodiazepine",
        "risk": "moderate",
        "rationale": "Sedation and fall risk, but shorter-acting than diazepam",
        "recommendation": "Use with caution, lowest dose, shortest duration"
    },
    "clonazepam": {
        "category": "Benzodiazepine",
        "risk": "high",
        "rationale": "Long half-life, prolonged sedation, falls",
        "recommendation": "Avoid"
    },
    
    # First-generation antihistamines
    "hydroxyzine": {
        "category": "Anticholinergic",
        "risk": "high",
        "rationale": "Anticholinergic, sedation, confusion",
        "recommendation": "Avoid"
    },
    
    # Sedative-hypnotics
    "zolpidem": {
        "category": "Sedative-Hypnotic",
        "risk": "moderate",
        "rationale": "Fall risk, confusion, especially at doses >5mg",
        "recommendation": "Avoid doses >5mg. Consider sleep hygiene first"
    },
    "zopiclone": {
        "category": "Sedative-Hypnotic",
        "risk": "moderate",
        "rationale": "Fall risk, daytime sedation",
        "recommendation": "Use cautiously, short-term only"
    },
    
    # NSAIDs - chronic use
    "indomethacin": {
        "category": "NSAID",
        "risk": "high",
        "rationale": "Most CNS adverse effects of all NSAIDs; GI bleeding, kidney injury",
        "recommendation": "Avoid"
    },
    "ketorolac": {
        "category": "NSAID",
        "risk": "high",
        "rationale": "Increased GI bleeding and acute kidney injury",
        "recommendation": "Avoid"
    },
    
    # Muscle relaxants
    "cyclobenzaprine": {
        "category": "Muscle Relaxant",
        "risk": "high",
        "rationale": "Anticholinergic effects, sedation, fall risk",
        "recommendation": "Avoid"
    },
    
    # Antipsychotics (for behavioral problems)
    "haloperidol": {
        "category": "Antipsychotic",
        "risk": "high",
        "rationale": "Increased mortality in dementia; extrapyramidal effects",
        "recommendation": "Avoid except for schizophrenia or bipolar. Black box warning"
    },
    "quetiapine": {
        "category": "Antipsychotic",
        "risk": "moderate",
        "rationale": "Increased mortality in dementia, falls, sedation",
        "recommendation": "Use only for approved indications, lowest dose"
    },
    "olanzapine": {
        "category": "Antipsychotic",
        "risk": "moderate",
        "rationale": "Increased mortality in dementia, metabolic effects",
        "recommendation": "Avoid for behavioral problems of dementia"
    },
    
    # Tricyclic antidepressants
    "amitriptyline": {
        "category": "Tricyclic Antidepressant",
        "risk": "high",
        "rationale": "Highly anticholinergic, sedating, orthostatic hypotension",
        "recommendation": "Avoid. Consider SSRI/SNRI instead"
    },
}

# ==================================================================================
# FALL RISK MEDICATIONS
# ==================================================================================
FALL_RISK_DRUGS = {
    # Sedatives/Hypnotics
    "diazepam": "high",
    "alprazolam": "high",
    "lorazepam": "moderate",
    "zolpidem": "moderate",
    "zopiclone": "moderate",
    "clonazepam": "high",
    
    # Antipsychotics
    "haloperidol": "high",
    "quetiapine": "moderate",
    "olanzapine": "moderate",
    "risperidone": "moderate",
    
    # Antidepressants (especially sedating)
    "amitriptyline": "high",
    "mirtazapine": "moderate",
    "trazodone": "moderate",
    
    # Antihistamines
    "diphenhydramine": "high",
    "dimenhydrinate": "high",
    "hydroxyzine": "high",
    
    # Antihypertensives (orthostatic hypotension risk)
    "doxazosin": "moderate",
    "prazosin": "moderate",
    "terazosin": "moderate",
    
    # Opioids
    "morphine": "moderate",
    "oxycodone": "moderate",
    "hydromorphone": "moderate",
    "tramadol": "moderate",
    "codeine": "moderate",
    
    # Muscle relaxants
    "cyclobenzaprine": "high",
    "baclofen": "moderate",
}

# ==================================================================================
# ANTICHOLINERGIC BURDEN - Drug-specific scores
# ==================================================================================
ANTICHOLINERGIC_BURDEN = {
    # Score 3 (High)
    "amitriptyline": 3,
    "diphenhydramine": 3,
    "hydroxyzine": 3,
    "oxybutynin": 3,
    "tolterodine": 3,
    
    # Score 2 (Moderate)
    "cyclobenzaprine": 2,
    "paroxetine": 2,
    
    # Score 1 (Low)
    "codeine": 1,
    "colchicine": 1,
    "digoxin": 1,
    "furosemide": 1,
    "ranitidine": 1,
    "warfarin": 1,
}

def calculate_anticholinergic_burden(meds):
    """Calculate total anticholinergic burden score"""
    total_score = 0
    contributors = []
    
    for med in meds:
        drug_name = med["name"].lower().strip()
        score = ANTICHOLINERGIC_BURDEN.get(drug_name, 0)
        if score > 0:
            total_score += score
            contributors.append((med["name"], score))
    
    return total_score, contributors

def assess_beers_criteria(meds):
    """Check for potentially inappropriate medications per Beers Criteria"""
    beers_violations = []
    
    for med in meds:
        drug_name = med["name"].lower().strip()
        if drug_name in BEERS_CRITERIA:
            beers_violations.append({
                "drug": med["name"],
                "details": BEERS_CRITERIA[drug_name]
            })
    
    return beers_violations

def calculate_fall_risk(meds, patient_age):
    """Calculate fall risk based on medication profile"""
    fall_risk_score = 0
    fall_risk_meds = []
    
    # Base risk increases with age
    if patient_age >= 80:
        fall_risk_score += 2
    elif patient_age >= 75:
        fall_risk_score += 1
    
    for med in meds:
        drug_name = med["name"].lower().strip()
        if drug_name in FALL_RISK_DRUGS:
            risk_level = FALL_RISK_DRUGS[drug_name]
            if risk_level == "high":
                fall_risk_score += 3
            elif risk_level == "moderate":
                fall_risk_score += 2
            fall_risk_meds.append((med["name"], risk_level))
    
    # Categorize overall fall risk
    if fall_risk_score >= 7:
        fall_risk_category = "HIGH"
    elif fall_risk_score >= 4:
        fall_risk_category = "MODERATE"
    elif fall_risk_score >= 1:
        fall_risk_category = "LOW"
    else:
        fall_risk_category = "MINIMAL"
    
    return fall_risk_score, fall_risk_category, fall_risk_meds

def generate_daily_schedule(meds, custom_times=None):
    """
    Generate visual daily medication schedule
    
    Args:
        meds: List of medication dictionaries
        custom_times: Optional dict with custom timing preferences
                     {"morning": "08:00", "noon": "12:00", "evening": "18:00", "bedtime": "22:00"}
    
    Returns:
        Dictionary with time slots as keys and medication lists as values
    """
    # Default times if not provided
    default_times = {
        "morning": "08:00",
        "noon": "12:00", 
        "evening": "18:00",
        "bedtime": "22:00"
    }
    
    # Use custom times if provided, otherwise use defaults
    times = custom_times if custom_times else default_times
    
    # Create schedule with custom times
    schedule = {
        f"Morning ({times['morning']})": [],
        f"Noon ({times['noon']})": [],
        f"Evening ({times['evening']})": [],
        f"Bedtime ({times['bedtime']})": []
    }
    
    # Map to keys for easier access
    time_keys = list(schedule.keys())
    
    # Simple heuristic: distribute based on doses per day
    for med in meds:
        doses = med["doses_per_day"]
        if doses == 1:
            # Once daily - morning
            schedule[time_keys[0]].append(med["name"])
        elif doses == 2:
            # Twice daily - morning and evening
            schedule[time_keys[0]].append(med["name"])
            schedule[time_keys[2]].append(med["name"])
        elif doses == 3:
            # Three times daily - morning, noon, evening
            schedule[time_keys[0]].append(med["name"])
            schedule[time_keys[1]].append(med["name"])
            schedule[time_keys[2]].append(med["name"])
        elif doses >= 4:
            # Four or more times daily - all slots
            schedule[time_keys[0]].append(med["name"])
            schedule[time_keys[1]].append(med["name"])
            schedule[time_keys[2]].append(med["name"])
            schedule[time_keys[3]].append(med["name"])
    
    return schedule

def calculate_pill_burden(meds):
    """Calculate total pills per day"""
    total_pills_per_day = sum(med["doses_per_day"] for med in meds)
    total_medications = len(meds)
    
    # Categorize burden
    if total_pills_per_day >= 15:
        burden_level = "VERY HIGH"
        concern = "Extremely difficult to manage - high risk of non-adherence"
    elif total_pills_per_day >= 10:
        burden_level = "HIGH"
        concern = "Challenging regimen - consider simplification"
    elif total_pills_per_day >= 6:
        burden_level = "MODERATE"
        concern = "Manageable but benefits from organization"
    else:
        burden_level = "LOW"
        concern = "Reasonable medication burden"
    
    return total_pills_per_day, total_medications, burden_level, concern

def predict_adherence(meds, patient_age, cognitive_impairment=False):
    """Predict medication adherence based on complexity"""
    # Start with base adherence of 100%
    adherence_score = 100.0
    
    total_pills = sum(med["doses_per_day"] for med in meds)
    num_meds = len(meds)
    
    # Reduce adherence based on complexity
    adherence_score -= (num_meds - 1) * 3  # Each additional med reduces by 3%
    adherence_score -= (total_pills - num_meds) * 2  # Multiple daily doses reduce adherence
    
    # Age factor
    if patient_age >= 80:
        adherence_score -= 10
    elif patient_age >= 75:
        adherence_score -= 5
    
    # Cognitive impairment
    if cognitive_impairment:
        adherence_score -= 20
    
    # Count unique timing requirements
    timing_complexity = 0
    for med in meds:
        if med["doses_per_day"] >= 3:
            timing_complexity += 2
        elif med["doses_per_day"] == 2:
            timing_complexity += 1
    
    adherence_score -= timing_complexity * 2
    
    # Cap between 0-100%
    adherence_score = max(0, min(100, adherence_score))
    
    return round(adherence_score, 1)

def generate_simplification_recommendations(meds):
    """Suggest ways to simplify medication regimen"""
    recommendations = []
    
    # Check for medications that could be once-daily
    for med in meds:
        if med["doses_per_day"] >= 3:
            recommendations.append(
                f"🔄 {med['name']}: Currently {med['doses_per_day']}x daily. "
                f"Ask doctor about extended-release formulation for once-daily dosing."
            )
    
    # Check for high pill burden
    total_pills = sum(med["doses_per_day"] for med in meds)
    if total_pills >= 10:
        recommendations.append(
            f"⚠️  Total daily pill burden is {total_pills}. Consider medication review to identify "
            "drugs that could be discontinued or combined."
        )
    
    # Check for potentially unnecessary medications
    if len(meds) >= 8:
        recommendations.append(
            "📋 With 8+ medications, consider comprehensive medication review (deprescribing assessment) "
            "to identify medications that may no longer be necessary."
        )
    
    return recommendations

def calculate_memory_actions_per_day(meds):
    """Calculate how many times per day patient must remember to take medications"""
    timing_slots = set()
    
    for med in meds:
        doses = med["doses_per_day"]
        if doses == 1:
            timing_slots.add("morning")
        elif doses == 2:
            timing_slots.add("morning")
            timing_slots.add("evening")
        elif doses == 3:
            timing_slots.add("morning")
            timing_slots.add("noon")
            timing_slots.add("evening")
        elif doses >= 4:
            timing_slots.add("morning")
            timing_slots.add("noon")
            timing_slots.add("evening")
            timing_slots.add("bedtime")
    
    return len(timing_slots)