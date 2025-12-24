# interaction_database.py
# Comprehensive Canadian Drug Interaction Database
# Based on top prescribed medications in Canada 2024 and clinically significant interactions

INTERACTION_DATABASE = {
    # ==================================================================================
    # ANTICOAGULANT INTERACTIONS (Warfarin)
    # ==================================================================================
    ("warfarin", "bactrim"): {
        "severity": "high",
        "description": "Bactrim significantly increases warfarin's anticoagulant effect, increasing bleeding risk"
    },
    ("warfarin", "sulfamethoxazole"): {
        "severity": "high",
        "description": "Sulfamethoxazole increases warfarin effect, major bleeding risk"
    },
    ("warfarin", "trimethoprim"): {
        "severity": "high",
        "description": "Trimethoprim potentiates anticoagulant effect of warfarin"
    },
    ("warfarin", "aspirin"): {
        "severity": "high",
        "description": "Increased bleeding risk - avoid combination unless specifically indicated"
    },
    ("warfarin", "ibuprofen"): {
        "severity": "high",
        "description": "NSAIDs significantly increase bleeding risk with warfarin"
    },
    ("warfarin", "naproxen"): {
        "severity": "high",
        "description": "NSAIDs increase bleeding risk with warfarin"
    },
    ("warfarin", "diclofenac"): {
        "severity": "high",
        "description": "NSAIDs increase bleeding risk with warfarin"
    },
    ("warfarin", "amoxicillin"): {
        "severity": "moderate",
        "description": "May alter INR, monitor closely and adjust warfarin dose if needed"
    },
    ("warfarin", "ciprofloxacin"): {
        "severity": "high",
        "description": "Fluoroquinolones may enhance anticoagulant effect significantly"
    },
    ("warfarin", "levofloxacin"): {
        "severity": "moderate",
        "description": "May enhance anticoagulant effect, monitor INR"
    },
    ("warfarin", "clarithromycin"): {
        "severity": "high",
        "description": "Macrolide antibiotics increase warfarin effect, bleeding risk"
    },
    ("warfarin", "azithromycin"): {
        "severity": "moderate",
        "description": "May increase warfarin effect, monitor INR"
    },
    ("warfarin", "metronidazole"): {
        "severity": "high",
        "description": "Significantly enhances anticoagulant effect"
    },
    
    # ==================================================================================
    # STATIN INTERACTIONS (Rosuvastatin, Atorvastatin, Simvastatin)
    # ==================================================================================
    ("rosuvastatin", "gemfibrozil"): {
        "severity": "high",
        "description": "Significantly increases risk of rhabdomyolysis and myopathy"
    },
    ("atorvastatin", "gemfibrozil"): {
        "severity": "high",
        "description": "Major risk of rhabdomyolysis - avoid combination"
    },
    ("simvastatin", "gemfibrozil"): {
        "severity": "high",
        "description": "Contraindicated - severe risk of rhabdomyolysis"
    },
    ("simvastatin", "clarithromycin"): {
        "severity": "high",
        "description": "Contraindicated - severe myopathy/rhabdomyolysis risk"
    },
    ("atorvastatin", "clarithromycin"): {
        "severity": "moderate",
        "description": "May increase statin levels, monitor for muscle pain"
    },
    ("rosuvastatin", "clarithromycin"): {
        "severity": "moderate",
        "description": "May increase statin exposure, use lowest effective dose"
    },
    ("simvastatin", "erythromycin"): {
        "severity": "high",
        "description": "Contraindicated - increases myopathy risk"
    },
    ("simvastatin", "itraconazole"): {
        "severity": "high",
        "description": "Contraindicated - severe interaction via CYP3A4"
    },
    ("simvastatin", "ketoconazole"): {
        "severity": "high",
        "description": "Contraindicated - severe CYP3A4 inhibition"
    },
    ("simvastatin", "verapamil"): {
        "severity": "moderate",
        "description": "Limit simvastatin to 10mg daily with verapamil"
    },
    ("atorvastatin", "verapamil"): {
        "severity": "moderate",
        "description": "May increase atorvastatin levels, monitor"
    },
    ("simvastatin", "diltiazem"): {
        "severity": "moderate",
        "description": "Limit simvastatin to 10mg daily with diltiazem"
    },
    ("simvastatin", "amlodipine"): {
        "severity": "moderate",
        "description": "Limit simvastatin to 20mg daily with amlodipine"
    },
    ("atorvastatin", "cyclosporine"): {
        "severity": "high",
        "description": "Significantly increases statin levels - use lowest dose"
    },
    ("rosuvastatin", "cyclosporine"): {
        "severity": "high",
        "description": "Contraindicated or use lowest dose with close monitoring"
    },
    
    # ==================================================================================
    # NSAID INTERACTIONS (Ibuprofen, Naproxen, Diclofenac)
    # ==================================================================================
    ("ibuprofen", "aspirin"): {
        "severity": "moderate",
        "description": "Increased GI bleeding risk; ibuprofen may reduce cardioprotective effect of aspirin"
    },
    ("naproxen", "aspirin"): {
        "severity": "moderate",
        "description": "Increased GI bleeding risk; may reduce aspirin's cardioprotective effect"
    },
    ("ibuprofen", "naproxen"): {
        "severity": "moderate",
        "description": "Avoid combining NSAIDs - increased GI bleeding and kidney injury risk"
    },
    ("diclofenac", "aspirin"): {
        "severity": "moderate",
        "description": "Increased bleeding risk, avoid combination"
    },
    
    # NSAIDs with ACE Inhibitors - "Triple Whammy" components
    ("ibuprofen", "lisinopril"): {
        "severity": "moderate",
        "description": "NSAIDs reduce ACE inhibitor effectiveness and increase kidney injury risk"
    },
    ("ibuprofen", "enalapril"): {
        "severity": "moderate",
        "description": "NSAIDs blunt antihypertensive effect and increase renal risk"
    },
    ("ibuprofen", "ramipril"): {
        "severity": "moderate",
        "description": "NSAIDs reduce blood pressure control and increase kidney injury risk"
    },
    ("naproxen", "lisinopril"): {
        "severity": "moderate",
        "description": "Reduces ACE inhibitor effectiveness, nephrotoxic combination"
    },
    ("naproxen", "enalapril"): {
        "severity": "moderate",
        "description": "NSAIDs antagonize ACE inhibitor effects"
    },
    ("naproxen", "ramipril"): {
        "severity": "moderate",
        "description": "Blunts antihypertensive effect, renal risk"
    },
    ("diclofenac", "lisinopril"): {
        "severity": "moderate",
        "description": "NSAIDs reduce ACE inhibitor effectiveness"
    },
    ("diclofenac", "enalapril"): {
        "severity": "moderate",
        "description": "Antagonizes antihypertensive effect"
    },
    ("diclofenac", "ramipril"): {
        "severity": "moderate",
        "description": "Reduces blood pressure control"
    },
    
    # NSAIDs with Diuretics - Part of "Triple Whammy"
    ("ibuprofen", "furosemide"): {
        "severity": "moderate",
        "description": "NSAIDs reduce diuretic effectiveness and increase kidney injury risk"
    },
    ("ibuprofen", "hydrochlorothiazide"): {
        "severity": "moderate",
        "description": "Reduces diuretic effect, increases blood pressure"
    },
    ("naproxen", "furosemide"): {
        "severity": "moderate",
        "description": "Antagonizes diuretic effect, nephrotoxic"
    },
    ("naproxen", "hydrochlorothiazide"): {
        "severity": "moderate",
        "description": "Reduces antihypertensive effect of thiazides"
    },
    ("diclofenac", "furosemide"): {
        "severity": "moderate",
        "description": "Reduces diuretic effectiveness"
    },
    ("diclofenac", "hydrochlorothiazide"): {
        "severity": "moderate",
        "description": "Blunts antihypertensive effect"
    },
    
    # NSAIDs with ARBs
    ("ibuprofen", "losartan"): {
        "severity": "moderate",
        "description": "NSAIDs reduce ARB effectiveness and increase renal risk"
    },
    ("naproxen", "losartan"): {
        "severity": "moderate",
        "description": "Reduces antihypertensive effect, nephrotoxic"
    },
    ("ibuprofen", "valsartan"): {
        "severity": "moderate",
        "description": "NSAIDs antagonize ARB effect"
    },
    ("naproxen", "valsartan"): {
        "severity": "moderate",
        "description": "Reduces blood pressure control"
    },
    
    # NSAIDs with Lithium
    ("ibuprofen", "lithium"): {
        "severity": "high",
        "description": "NSAIDs increase lithium levels significantly - risk of toxicity"
    },
    ("naproxen", "lithium"): {
        "severity": "high",
        "description": "Increases lithium levels, monitor closely"
    },
    ("diclofenac", "lithium"): {
        "severity": "high",
        "description": "Elevates lithium levels, toxicity risk"
    },
    
    # ==================================================================================
    # ACE INHIBITOR INTERACTIONS
    # ==================================================================================
    ("lisinopril", "spironolactone"): {
        "severity": "moderate",
        "description": "Increased risk of hyperkalemia - monitor potassium levels"
    },
    ("enalapril", "spironolactone"): {
        "severity": "moderate",
        "description": "Hyperkalemia risk - monitor potassium closely"
    },
    ("ramipril", "spironolactone"): {
        "severity": "moderate",
        "description": "Additive hyperkalemia risk"
    },
    ("lisinopril", "losartan"): {
        "severity": "moderate",
        "description": "Dual RAAS blockade - increased hypotension, hyperkalemia, renal dysfunction risk"
    },
    ("enalapril", "valsartan"): {
        "severity": "moderate",
        "description": "Dual RAAS blockade generally not recommended"
    },
    ("ramipril", "losartan"): {
        "severity": "moderate",
        "description": "Avoid dual ACE/ARB therapy"
    },
    ("lisinopril", "lithium"): {
        "severity": "moderate",
        "description": "ACE inhibitors increase lithium levels - monitor"
    },
    ("enalapril", "lithium"): {
        "severity": "moderate",
        "description": "May elevate lithium levels, toxicity risk"
    },
    ("ramipril", "lithium"): {
        "severity": "moderate",
        "description": "Increases lithium concentration"
    },
    
    # ==================================================================================
    # ANTIDIABETIC INTERACTIONS (Metformin, Ozempic/Semaglutide, Jardiance/Empagliflozin)
    # ==================================================================================
    ("metformin", "furosemide"): {
        "severity": "moderate",
        "description": "Diuretics may impair kidney function, increasing metformin levels"
    },
    ("metformin", "hydrochlorothiazide"): {
        "severity": "low",
        "description": "May affect blood glucose control"
    },
    # SGLT2 inhibitors with diuretics
    ("empagliflozin", "furosemide"): {
        "severity": "moderate",
        "description": "Additive diuretic effect - monitor for dehydration and hypotension"
    },
    ("empagliflozin", "hydrochlorothiazide"): {
        "severity": "moderate",
        "description": "Increased risk of volume depletion"
    },
    
    # ==================================================================================
    # SSRI/SNRI INTERACTIONS (Sertraline, Escitalopram, Venlafaxine)
    # ==================================================================================
    ("sertraline", "tramadol"): {
        "severity": "high",
        "description": "Increased risk of serotonin syndrome - life-threatening"
    },
    ("escitalopram", "tramadol"): {
        "severity": "high",
        "description": "Serotonin syndrome risk - avoid combination"
    },
    ("venlafaxine", "tramadol"): {
        "severity": "high",
        "description": "Severe serotonin syndrome risk"
    },
    ("fluoxetine", "tramadol"): {
        "severity": "high",
        "description": "Serotonin syndrome - contraindicated"
    },
    ("sertraline", "ibuprofen"): {
        "severity": "moderate",
        "description": "SSRIs with NSAIDs increase GI bleeding risk"
    },
    ("escitalopram", "ibuprofen"): {
        "severity": "moderate",
        "description": "Increased bleeding risk - monitor"
    },
    ("sertraline", "aspirin"): {
        "severity": "moderate",
        "description": "Increased bleeding risk with antiplatelet agents"
    },
    ("escitalopram", "aspirin"): {
        "severity": "moderate",
        "description": "Additive bleeding risk"
    },
    ("fluoxetine", "aspirin"): {
        "severity": "moderate",
        "description": "SSRIs increase bleeding tendency"
    },
    ("sertraline", "warfarin"): {
        "severity": "moderate",
        "description": "SSRIs may potentiate warfarin effect"
    },
    ("escitalopram", "warfarin"): {
        "severity": "moderate",
        "description": "Monitor INR closely with combination"
    },
    
    # ==================================================================================
    # BETA BLOCKER INTERACTIONS (Metoprolol, Atenolol, Carvedilol)
    # ==================================================================================
    ("metoprolol", "verapamil"): {
        "severity": "moderate",
        "description": "May cause excessive bradycardia or heart block - monitor closely"
    },
    ("metoprolol", "diltiazem"): {
        "severity": "moderate",
        "description": "Risk of severe bradycardia and AV block"
    },
    ("atenolol", "verapamil"): {
        "severity": "moderate",
        "description": "Additive negative chronotropic effects"
    },
    ("atenolol", "diltiazem"): {
        "severity": "moderate",
        "description": "May cause excessive heart rate slowing"
    },
    ("carvedilol", "verapamil"): {
        "severity": "moderate",
        "description": "Bradycardia and heart failure worsening risk"
    },
    ("carvedilol", "diltiazem"): {
        "severity": "moderate",
        "description": "Excessive cardiac depression possible"
    },
    
    # ==================================================================================
    # DIGOXIN INTERACTIONS
    # ==================================================================================
    ("digoxin", "furosemide"): {
        "severity": "moderate",
        "description": "Loop diuretics cause hypokalemia increasing digoxin toxicity risk"
    },
    ("digoxin", "hydrochlorothiazide"): {
        "severity": "moderate",
        "description": "Thiazides cause hypokalemia, predisposing to digoxin toxicity"
    },
    ("digoxin", "spironolactone"): {
        "severity": "moderate",
        "description": "May increase digoxin levels, monitor"
    },
    ("digoxin", "clarithromycin"): {
        "severity": "high",
        "description": "Macrolides significantly increase digoxin levels - toxicity risk"
    },
    ("digoxin", "amiodarone"): {
        "severity": "high",
        "description": "Amiodarone doubles digoxin levels - reduce digoxin dose by 50%"
    },
    ("digoxin", "verapamil"): {
        "severity": "moderate",
        "description": "Increases digoxin levels, reduce digoxin dose"
    },
    
    # ==================================================================================
    # THYROID HORMONE INTERACTIONS (Synthroid/Levothyroxine - #1 in Canada!)
    # ==================================================================================
    ("levothyroxine", "omeprazole"): {
        "severity": "moderate",
        "description": "PPIs may decrease levothyroxine absorption - separate dosing by 4+ hours"
    },
    ("levothyroxine", "pantoprazole"): {
        "severity": "moderate",
        "description": "PPIs reduce levothyroxine absorption"
    },
    ("levothyroxine", "calcium"): {
        "severity": "moderate",
        "description": "Calcium supplements reduce levothyroxine absorption - separate by 4 hours"
    },
    ("levothyroxine", "iron"): {
        "severity": "moderate",
        "description": "Iron supplements impair absorption - take 4 hours apart"
    },
    ("levothyroxine", "warfarin"): {
        "severity": "moderate",
        "description": "Thyroid hormones may potentiate warfarin - monitor INR"
    },
    
    # ==================================================================================
    # PROTON PUMP INHIBITOR INTERACTIONS
    # ==================================================================================
    ("omeprazole", "clopidogrel"): {
        "severity": "moderate",
        "description": "Omeprazole reduces clopidogrel effectiveness - use pantoprazole instead"
    },
    ("pantoprazole", "warfarin"): {
        "severity": "low",
        "description": "Monitor INR when initiating or stopping PPI"
    },
    
    # ==================================================================================
    # FLUOROQUINOLONE + CATION INTERACTIONS
    # ==================================================================================
    ("ciprofloxacin", "calcium"): {
        "severity": "moderate",
        "description": "Calcium reduces fluoroquinolone absorption - separate by 2-6 hours"
    },
    ("levofloxacin", "calcium"): {
        "severity": "moderate",
        "description": "Divalent cations impair absorption"
    },
    ("ciprofloxacin", "iron"): {
        "severity": "moderate",
        "description": "Iron reduces ciprofloxacin absorption significantly"
    },
    ("levofloxacin", "iron"): {
        "severity": "moderate",
        "description": "Separate iron and fluoroquinolone by several hours"
    },
    ("ciprofloxacin", "magnesium"): {
        "severity": "moderate",
        "description": "Antacids with magnesium reduce absorption"
    },
    ("levofloxacin", "magnesium"): {
        "severity": "moderate",
        "description": "Avoid concurrent administration with antacids"
    },
    
    # ==================================================================================
    # BENZODIAZEPINE INTERACTIONS
    # ==================================================================================
    ("diazepam", "clarithromycin"): {
        "severity": "moderate",
        "description": "CYP3A4 inhibitors increase benzodiazepine levels - sedation risk"
    },
    ("alprazolam", "ketoconazole"): {
        "severity": "high",
        "description": "Contraindicated - severe increase in alprazolam levels"
    },
    
    # ==================================================================================
    # MISCELLANEOUS IMPORTANT INTERACTIONS
    # ==================================================================================
    ("allopurinol", "azathioprine"): {
        "severity": "high",
        "description": "Allopurinol increases azathioprine toxicity - reduce azathioprine dose by 75%"
    },
    ("phenytoin", "warfarin"): {
        "severity": "moderate",
        "description": "Complex interaction - monitor INR closely"
    },
    ("carbamazepine", "clarithromycin"): {
        "severity": "high",
        "description": "Clarithromycin increases carbamazepine levels - toxicity risk"
    },
    ("theophylline", "ciprofloxacin"): {
        "severity": "high",
        "description": "Fluoroquinolones significantly increase theophylline levels"
    },
}

# ==================================================================================
# DRUG NAME NORMALIZATION - Handle brand names and variations
# ==================================================================================
DRUG_ALIASES = {
    # Antibiotics
    "sulfamethoxazole/trimethoprim": "bactrim",
    "sulfamethoxazole trimethoprim": "bactrim",
    "tmp/smx": "bactrim",
    "cotrimoxazole": "bactrim",
    "septra": "bactrim",
    "apo-sulfatrim": "bactrim",
    "biaxin": "clarithromycin",
    "zithromax": "azithromycin",
    "z-pak": "azithromycin",
    "cipro": "ciprofloxacin",
    "levaquin": "levofloxacin",
    "flagyl": "metronidazole",
    "amoxil": "amoxicillin",
    
    # Anticoagulants
    "coumadin": "warfarin",
    "jantoven": "warfarin",
    
    # Statins
    "lipitor": "atorvastatin",
    "crestor": "rosuvastatin",
    "zocor": "simvastatin",
    "pravachol": "pravastatin",
    "lescol": "fluvastatin",
    "livalo": "pitavastatin",
    
    # NSAIDs
    "advil": "ibuprofen",
    "motrin": "ibuprofen",
    "aleve": "naproxen",
    "naprosyn": "naproxen",
    "voltaren": "diclofenac",
    "celebrex": "celecoxib",
    
    # Acetaminophen
    "tylenol": "acetaminophen",
    "paracetamol": "acetaminophen",
    
    # Antihypertensives
    "prinivil": "lisinopril",
    "zestril": "lisinopril",
    "vasotec": "enalapril",
    "altace": "ramipril",
    "cozaar": "losartan",
    "diovan": "valsartan",
    "norvasc": "amlodipine",
    "cardizem": "diltiazem",
    "calan": "verapamil",
    "isoptin": "verapamil",
    "lopressor": "metoprolol",
    "toprol": "metoprolol",
    "tenormin": "atenolol",
    "coreg": "carvedilol",
    
    # Diuretics
    "lasix": "furosemide",
    "hydrodiuril": "hydrochlorothiazide",
    "hctz": "hydrochlorothiazide",
    "aldactone": "spironolactone",
    
    # Diabetes medications
    "glucophage": "metformin",
    "ozempic": "semaglutide",
    "jardiance": "empagliflozin",
    
    # Thyroid
    "synthroid": "levothyroxine",
    "eltroxin": "levothyroxine",
    
    # Antidepressants
    "zoloft": "sertraline",
    "prozac": "fluoxetine",
    "lexapro": "escitalopram",
    "cipralex": "escitalopram",
    "effexor": "venlafaxine",
    
    # PPIs
    "prilosec": "omeprazole",
    "losec": "omeprazole",
    "nexium": "esomeprazole",
    "pantoloc": "pantoprazole",
    "tecta": "pantoprazole",
    "prevacid": "lansoprazole",
    
    # Others
    "plavix": "clopidogrel",
    "lanoxin": "digoxin",
    "cordarone": "amiodarone",
    "ultram": "tramadol",
    "valium": "diazepam",
    "xanax": "alprazolam",
    "zyloprim": "allopurinol",
    "dilantin": "phenytoin",
    "tegretol": "carbamazepine",
}

def normalize_drug_name(drug_name):
    """Normalize drug name to standard form"""
    drug_name = drug_name.lower().strip()
    return DRUG_ALIASES.get(drug_name, drug_name)

def check_interaction(drug1, drug2):
    """Check if two drugs interact"""
    drug1 = normalize_drug_name(drug1)
    drug2 = normalize_drug_name(drug2)
    
    # Check both orderings
    interaction = INTERACTION_DATABASE.get((drug1, drug2))
    if not interaction:
        interaction = INTERACTION_DATABASE.get((drug2, drug1))
    
    return interaction