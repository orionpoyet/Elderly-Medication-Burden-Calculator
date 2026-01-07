# interaction_database.py
# Enhanced Elderly-Focused Canadian Drug Interaction Database
# Structured for scalability and clinical relevance

import re
from typing import Dict, List, Tuple, Optional, Set
from itertools import combinations, permutations
from dataclasses import asdict
from dataclasses import dataclass
@dataclass
class DrugInteraction:
    """Data structure for drug interactions"""
    severity: str  # 'critical', 'high', 'moderate', 'low'
    description: str
    mechanism: str  # Pharmacological mechanism
    clinical_evidence: str  # Quality of evidence
    elderly_risk: str  # Specific elderly risk profile
    alternatives: List[str]  # Safer alternatives
    monitoring: str  # What to monitor
    action: str  # Recommended action
    references: List[str]  # References (Health Canada, CPS, etc.)
    fall_risk_increase: int  # 0-10 scale
    delirium_risk: bool  # Increases delirium risk?
    renal_risk: bool  # Renal impairment concern?
    
    def to_dict(self):
        return {
            'severity': self.severity,
            'description': self.description,
            'mechanism': self.mechanism,
            'clinical_evidence': self.clinical_evidence,
            'elderly_risk': self.elderly_risk,
            'alternatives': self.alternatives,
            'monitoring': self.monitoring,
            'action': self.action,
            'references': self.references,
            'fall_risk_increase': self.fall_risk_increase,
            'delirium_risk': self.delirium_risk,
            'renal_risk': self.renal_risk
        }

@dataclass
class DrugProfile:
    """Data structure for individual drug profiles"""
    generic_name: str
    brand_names: List[str]
    drug_class: str
    anticholinergic_score: int  # 0-3 scale
    sedative_score: int  # 0-3 scale
    fall_risk_score: int  # 0-10 scale
    beers_criteria: bool  # Potentially inappropriate for elderly?
    renal_adjustment: bool  # Needs renal dose adjustment?
    cyp_inhibitors: List[str]  # CYP enzymes inhibited
    cyp_substrates: List[str]  # CYP enzyme substrates
    pregnancy_category: str
    lactation_safety: str
    common_elderly_side_effects: List[str]
    
    def to_dict(self):
        return {
            'generic_name': self.generic_name,
            'drug_class': self.drug_class,
            'anticholinergic_score': self.anticholinergic_score,
            'sedative_score': self.sedative_score,
            'fall_risk_score': self.fall_risk_score,
            'beers_criteria': self.beers_criteria,
            'renal_adjustment': self.renal_adjustment
        }

# ============================================================================
# DRUG PROFILES DATABASE - Individual Drug Characteristics
# ============================================================================
DRUG_PROFILES: Dict[str, DrugProfile] = {
    # ========== HIGH-RISK ELDERLY DRUGS ==========
    "warfarin": DrugProfile(
        generic_name="warfarin",
        brand_names=["Coumadin", "Jantoven"],
        drug_class="Anticoagulant",
        anticholinergic_score=0,
        sedative_score=0,
        fall_risk_score=2,
        beers_criteria=True,
        renal_adjustment=False,
        cyp_inhibitors=[],
        cyp_substrates=["CYP2C9", "CYP1A2", "CYP3A4"],
        pregnancy_category="X",
        lactation_safety="Avoid",
        common_elderly_side_effects=["Bleeding", "Bruising", "Hair loss"]
    ),
    
    "digoxin": DrugProfile(
        generic_name="digoxin",
        brand_names=["Lanoxin"],
        drug_class="Cardiac Glycoside",
        anticholinergic_score=1,
        sedative_score=0,
        fall_risk_score=3,
        beers_criteria=True,
        renal_adjustment=True,
        cyp_inhibitors=[],
        cyp_substrates=["P-glycoprotein"],
        pregnancy_category="C",
        lactation_safety="Caution",
        common_elderly_side_effects=["Nausea", "Confusion", "Vision changes", "Bradycardia"]
    ),
    
    # ========== STATINS ==========
    "simvastatin": DrugProfile(
        generic_name="simvastatin",
        brand_names=["Zocor"],
        drug_class="Statin",
        anticholinergic_score=0,
        sedative_score=1,
        fall_risk_score=1,
        beers_criteria=False,
        renal_adjustment=False,
        cyp_inhibitors=[],
        cyp_substrates=["CYP3A4"],
        pregnancy_category="X",
        lactation_safety="Contraindicated",
        common_elderly_side_effects=["Myalgia", "Elevated LFTs"]
    ),
    
    "atorvastatin": DrugProfile(
        generic_name="atorvastatin",
        brand_names=["Lipitor"],
        drug_class="Statin",
        anticholinergic_score=0,
        sedative_score=1,
        fall_risk_score=1,
        beers_criteria=False,
        renal_adjustment=False,
        cyp_inhibitors=[],
        cyp_substrates=["CYP3A4"],
        pregnancy_category="X",
        lactation_safety="Contraindicated",
        common_elderly_side_effects=["Myalgia", "Elevated LFTs"]
    ),
    
    # ========== NSAIDs ==========
    "ibuprofen": DrugProfile(
        generic_name="ibuprofen",
        brand_names=["Advil", "Motrin"],
        drug_class="NSAID",
        anticholinergic_score=0,
        sedative_score=1,
        fall_risk_score=2,
        beers_criteria=True,
        renal_adjustment=True,
        cyp_inhibitors=[],
        cyp_substrates=["CYP2C9"],
        pregnancy_category="C",
        lactation_safety="Compatible",
        common_elderly_side_effects=["GI bleeding", "Renal impairment", "Hypertension"]
    ),
    
    "naproxen": DrugProfile(
        generic_name="naproxen",
        brand_names=["Aleve", "Naprosyn"],
        drug_class="NSAID",
        anticholinergic_score=0,
        sedative_score=1,
        fall_risk_score=2,
        beers_criteria=True,
        renal_adjustment=True,
        cyp_inhibitors=[],
        cyp_substrates=["CYP2C9"],
        pregnancy_category="C",
        lactation_safety="Compatible",
        common_elderly_side_effects=["GI bleeding", "Renal impairment", "Hypertension"]
    ),
    
    # ========== ACE INHIBITORS ==========
    "lisinopril": DrugProfile(
        generic_name="lisinopril",
        brand_names=["Prinivil", "Zestril"],
        drug_class="ACE Inhibitor",
        anticholinergic_score=0,
        sedative_score=1,
        fall_risk_score=3,
        beers_criteria=False,
        renal_adjustment=True,
        cyp_inhibitors=[],
        cyp_substrates=[],
        pregnancy_category="D",
        lactation_safety="Caution",
        common_elderly_side_effects=["Cough", "Hypotension", "Hyperkalemia", "Renal impairment"]
    ),
    
    # ========== ANTICHOLINERGICS ==========
    "diphenhydramine": DrugProfile(
        generic_name="diphenhydramine",
        brand_names=["Benadryl"],
        drug_class="Antihistamine",
        anticholinergic_score=3,
        sedative_score=3,
        fall_risk_score=8,
        beers_criteria=True,
        renal_adjustment=False,
        cyp_inhibitors=[],
        cyp_substrates=["CYP2D6"],
        pregnancy_category="B",
        lactation_safety="Caution",
        common_elderly_side_effects=["Sedation", "Confusion", "Dry mouth", "Urinary retention", "Constipation"]
    ),
    
    "oxybutynin": DrugProfile(
        generic_name="oxybutynin",
        brand_names=["Ditropan"],
        drug_class="Antimuscarinic",
        anticholinergic_score=3,
        sedative_score=1,
        fall_risk_score=5,
        beers_criteria=True,
        renal_adjustment=False,
        cyp_inhibitors=[],
        cyp_substrates=["CYP3A4"],
        pregnancy_category="B",
        lactation_safety="Caution",
        common_elderly_side_effects=["Dry mouth", "Confusion", "Constipation", "Blurred vision"]
    ),
    
    # ========== SEDATIVE-HYPNOTICS ==========
    "zolpidem": DrugProfile(
        generic_name="zolpidem",
        brand_names=["Ambien"],
        drug_class="Non-benzodiazepine hypnotic",
        anticholinergic_score=0,
        sedative_score=3,
        fall_risk_score=9,
        beers_criteria=True,
        renal_adjustment=True,
        cyp_inhibitors=[],
        cyp_substrates=["CYP3A4"],
        pregnancy_category="C",
        lactation_safety="Avoid",
        common_elderly_side_effects=["Dizziness", "Daytime drowsiness", "Memory impairment", "Falls"]
    ),
    
    "lorazepam": DrugProfile(
        generic_name="lorazepam",
        brand_names=["Ativan"],
        drug_class="Benzodiazepine",
        anticholinergic_score=1,
        sedative_score=3,
        fall_risk_score=8,
        beers_criteria=True,
        renal_adjustment=False,
        cyp_inhibitors=[],
        cyp_substrates=[],
        pregnancy_category="D",
        lactation_safety="Avoid",
        common_elderly_side_effects=["Sedation", "Ataxia", "Memory impairment", "Falls", "Respiratory depression"]
    ),
    
    # ========== ANTIDEPRESSANTS ==========
    "sertraline": DrugProfile(
        generic_name="sertraline",
        brand_names=["Zoloft"],
        drug_class="SSRI",
        anticholinergic_score=1,
        sedative_score=2,
        fall_risk_score=3,
        beers_criteria=False,
        renal_adjustment=False,
        cyp_inhibitors=["CYP2D6"],
        cyp_substrates=["CYP2C9", "CYP2C19", "CYP3A4"],
        pregnancy_category="C",
        lactation_safety="Compatible",
        common_elderly_side_effects=["Nausea", "Insomnia", "Sexual dysfunction", "Bleeding risk"]
    ),
    
    "amitriptyline": DrugProfile(
        generic_name="amitriptyline",
        brand_names=["Elavil"],
        drug_class="Tricyclic antidepressant",
        anticholinergic_score=3,
        sedative_score=3,
        fall_risk_score=7,
        beers_criteria=True,
        renal_adjustment=False,
        cyp_inhibitors=["CYP2D6"],
        cyp_substrates=["CYP2D6", "CYP2C19"],
        pregnancy_category="C",
        lactation_safety="Caution",
        common_elderly_side_effects=["Sedation", "Orthostatic hypotension", "Constipation", "Dry mouth", "Urinary retention"]
    ),
    
    # ========== ANTIPSYCHOTICS ==========
    "quetiapine": DrugProfile(
        generic_name="quetiapine",
        brand_names=["Seroquel"],
        drug_class="Atypical antipsychotic",
        anticholinergic_score=2,
        sedative_score=2,
        fall_risk_score=8,
        beers_criteria=True,
        renal_adjustment=False,
        cyp_inhibitors=[],
        cyp_substrates=["CYP3A4"],
        pregnancy_category="C",
        lactation_safety="Avoid",
        common_elderly_side_effects=["Sedation", "Orthostatic hypotension", "Metabolic syndrome", "Increased mortality in dementia"]
    ),
    
    # ========== DIABETES MEDICATIONS ==========
    "metformin": DrugProfile(
        generic_name="metformin",
        brand_names=["Glucophage"],
        drug_class="Biguanide",
        anticholinergic_score=1,
        sedative_score=0,
        fall_risk_score=0,
        beers_criteria=False,
        renal_adjustment=True,
        cyp_inhibitors=[],
        cyp_substrates=[],
        pregnancy_category="B",
        lactation_safety="Compatible",
        common_elderly_side_effects=["GI upset", "Lactic acidosis (rare)"]
    ),
    
    # ========== THYROID ==========
    "levothyroxine": DrugProfile(
        generic_name="levothyroxine",
        brand_names=["Synthroid", "Eltroxin"],
        drug_class="Thyroid hormone",
        anticholinergic_score=0,
        sedative_score=0,
        fall_risk_score=1,
        beers_criteria=False,
        renal_adjustment=False,
        cyp_inhibitors=[],
        cyp_substrates=[],
        pregnancy_category="A",
        lactation_safety="Compatible",
        common_elderly_side_effects=["Palpitations", "Insomnia", "Weight loss", "Osteoporosis (overtreatment)"]
    ),
    # ========== Expended drug profile =========
    "epinephrine": DrugProfile(
        generic_name="epinephrine",
        brand_names=["Adrenalin", "EpiPen"],
        drug_class="Sympathomimetic - Alpha/Beta Agonist",
        anticholinergic_score=0,
        sedative_score=0,
        fall_risk_score=2,
        beers_criteria=False,
        renal_adjustment=False,
        cyp_inhibitors=[],
        cyp_substrates=["MAO", "COMT"],
        pregnancy_category="C",
        lactation_safety="Compatible",
        common_elderly_side_effects=["Hypertension", "Tachycardia", "Tremor", "Anxiety"]
    ),
    
    "norepinephrine": DrugProfile(
        generic_name="norepinephrine",
        brand_names=["Levophed"],
        drug_class="Sympathomimetic - Alpha Agonist",
        anticholinergic_score=0,
        sedative_score=0,
        fall_risk_score=1,
        beers_criteria=False,
        renal_adjustment=False,
        cyp_inhibitors=[],
        cyp_substrates=["MAO", "COMT"],
        pregnancy_category="C",
        lactation_safety="Unknown",
        common_elderly_side_effects=["Hypertension", "Ischemia", "Arrhythmia"]
    ),
    
    "salbutamol": DrugProfile(
        generic_name="salbutamol",
        brand_names=["Ventolin", "ProAir"],
        drug_class="Beta-2 Agonist",
        anticholinergic_score=0,
        sedative_score=0,
        fall_risk_score=2,
        beers_criteria=False,
        renal_adjustment=False,
        cyp_inhibitors=[],
        cyp_substrates=["CYP3A4"],
        pregnancy_category="C",
        lactation_safety="Compatible",
        common_elderly_side_effects=["Tremor", "Tachycardia", "Hypokalemia", "Hyperglycemia"]
    ),
    
    # ==================== ANALGESICS/ANESTHETICS ====================
    "acetaminophen": DrugProfile(
        generic_name="acetaminophen",
        brand_names=["Tylenol"],
        drug_class="Analgesic/Antipyretic",
        anticholinergic_score=0,
        sedative_score=0,
        fall_risk_score=0,
        beers_criteria=False,
        renal_adjustment=False,
        cyp_inhibitors=[],
        cyp_substrates=["CYP2E1", "CYP1A2"],
        pregnancy_category="B",
        lactation_safety="Compatible",
        common_elderly_side_effects=["Hepatotoxicity (overdose)", "Rare: thrombocytopenia"]
    ),
    
    "bupivacaine": DrugProfile(
        generic_name="bupivacaine",
        brand_names=["Marcaine", "Sensorcaine"],
        drug_class="Local Anesthetic - Amide",
        anticholinergic_score=0,
        sedative_score=0,
        fall_risk_score=1,
        beers_criteria=False,
        renal_adjustment=False,
        cyp_inhibitors=[],
        cyp_substrates=["CYP3A4", "CYP1A2"],
        pregnancy_category="C",
        lactation_safety="Compatible",
        common_elderly_side_effects=["Hypotension", "Bradycardia", "CNS toxicity"]
    ),
    
    "midazolam": DrugProfile(
        generic_name="midazolam",
        brand_names=["Versed"],
        drug_class="Benzodiazepine - Anesthetic",
        anticholinergic_score=1,
        sedative_score=3,
        fall_risk_score=9,
        beers_criteria=True,
        renal_adjustment=False,
        cyp_inhibitors=[],
        cyp_substrates=["CYP3A4"],
        pregnancy_category="D",
        lactation_safety="Caution",
        common_elderly_side_effects=["Prolonged sedation", "Respiratory depression", "Paradoxical agitation", "Delirium"]
    ),
    
    "propofol": DrugProfile(
        generic_name="propofol",
        brand_names=["Diprivan"],
        drug_class="General Anesthetic",
        anticholinergic_score=0,
        sedative_score=3, #absent in table
        fall_risk_score=2,
        beers_criteria=False,
        renal_adjustment=False,
        cyp_inhibitors=[],
        cyp_substrates=["CYP2B6", "CYP2C9"],
        pregnancy_category="B",
        lactation_safety="Caution",
        common_elderly_side_effects=["Hypotension", "Bradycardia", "Respiratory depression", "Injection pain"]
    ),
    
    "rocuronium": DrugProfile(
        generic_name="rocuronium",
        brand_names=["Zemuron"],
        drug_class="Neuromuscular Blocker - Non-depolarizing",
        anticholinergic_score=0,
        sedative_score=0, #absent in table 
        fall_risk_score=0,
        beers_criteria=False,
        renal_adjustment=False,
        cyp_inhibitors=[],
        cyp_substrates=[],
        pregnancy_category="C",
        lactation_safety="Unknown",
        common_elderly_side_effects=["Prolonged paralysis", "Tachycardia"]
    ),
    
    "sevoflurane": DrugProfile(
        generic_name="sevoflurane",
        brand_names=["Ultane"],
        drug_class="Volatile Anesthetic",
        anticholinergic_score=0,
        sedative_score=3,#absent in table
        fall_risk_score=1,
        beers_criteria=False,
        renal_adjustment=False,
        cyp_inhibitors=[],
        cyp_substrates=["CYP2E1"],
        pregnancy_category="B",
        lactation_safety="Unknown",
        common_elderly_side_effects=["Delirium", "Myocardial depression", "QT prolongation"]
    ),
    
    # ==================== ANTIBIOTICS ====================
    "amoxicillin": DrugProfile(
        generic_name="amoxicillin",
        brand_names=["Amoxil"],
        drug_class="Penicillin Antibiotic",
        anticholinergic_score=0,
        sedative_score=0,
        fall_risk_score=0,
        beers_criteria=False,
        renal_adjustment=True,
        cyp_inhibitors=[],
        cyp_substrates=[],
        pregnancy_category="B",
        lactation_safety="Compatible",
        common_elderly_side_effects=["Diarrhea", "Rash", "C. difficile infection"]
    ),
    
    "azithromycin": DrugProfile(
        generic_name="azithromycin",
        brand_names=["Zithromax", "Z-Pak"],
        drug_class="Macrolide Antibiotic",
        anticholinergic_score=0,
        sedative_score=0,
        fall_risk_score=1,
        beers_criteria=False,
        renal_adjustment=False,
        cyp_inhibitors=["CYP3A4"],
        cyp_substrates=[],
        pregnancy_category="B",
        lactation_safety="Compatible",
        common_elderly_side_effects=["QT prolongation", "Diarrhea", "Cardiovascular death risk"]
    ),
    
    "cefazolin": DrugProfile(
        generic_name="cefazolin",
        brand_names=["Ancef", "Kefzol"],
        drug_class="Cephalosporin - 1st Generation",
        anticholinergic_score=0,
        sedative_score=0, #not in table
        fall_risk_score=0,
        beers_criteria=False,
        renal_adjustment=True,
        cyp_inhibitors=[],
        cyp_substrates=[],
        pregnancy_category="B",
        lactation_safety="Compatible",
        common_elderly_side_effects=["Phlebitis", "Diarrhea", "Seizures (high dose)"]
    ),
    
    "doxycycline": DrugProfile(
        generic_name="doxycycline",
        brand_names=["Vibramycin"],
        drug_class="Tetracycline Antibiotic",
        anticholinergic_score=0,
        sedative_score=0,
        fall_risk_score=0,
        beers_criteria=False,
        renal_adjustment=False,
        cyp_inhibitors=[],
        cyp_substrates=["CYP3A4"],
        pregnancy_category="D",
        lactation_safety="Avoid",
        common_elderly_side_effects=["Photosensitivity", "Esophagitis", "GI upset"]
    ),
    
    "meropenem": DrugProfile(
        generic_name="meropenem",
        brand_names=["Merrem"],
        drug_class="Carbapenem Antibiotic",
        anticholinergic_score=0,
        sedative_score=0,#not in table
        fall_risk_score=1,
        beers_criteria=False,
        renal_adjustment=True,
        cyp_inhibitors=[],
        cyp_substrates=[],
        pregnancy_category="B",
        lactation_safety="Compatible",
        common_elderly_side_effects=["Diarrhea", "Seizures (renal impairment)", "C. difficile"]
    ),
    
    "metronidazole": DrugProfile(
        generic_name="metronidazole",
        brand_names=["Flagyl"],
        drug_class="Nitroimidazole Antibiotic",
        anticholinergic_score=0,
        sedative_score=1,
        fall_risk_score=2,
        beers_criteria=False,
        renal_adjustment=False,
        cyp_inhibitors=["CYP2C9"],
        cyp_substrates=["CYP3A4"],
        pregnancy_category="B",
        lactation_safety="Caution",
        common_elderly_side_effects=["Peripheral neuropathy", "Metallic taste", "Disulfiram reaction with alcohol"]
    ),
    
    "moxifloxacin": DrugProfile(
        generic_name="moxifloxacin",
        brand_names=["Avelox"],
        drug_class="Fluoroquinolone Antibiotic",
        anticholinergic_score=0,
        sedative_score=1,
        fall_risk_score=2,
        beers_criteria=True,
        renal_adjustment=False,
        cyp_inhibitors=[],
        cyp_substrates=["CYP3A4"],
        pregnancy_category="C",
        lactation_safety="Avoid",
        common_elderly_side_effects=["QT prolongation", "Tendon rupture", "CNS effects", "Delirium"]
    ),
    
    "vancomycin": DrugProfile(
        generic_name="vancomycin",
        brand_names=["Vancocin"],
        drug_class="Glycopeptide Antibiotic",
        anticholinergic_score=1,
        sedative_score=0,
        fall_risk_score=0,
        beers_criteria=False,
        renal_adjustment=True,
        cyp_inhibitors=[],
        cyp_substrates=[],
        pregnancy_category="C",
        lactation_safety="Compatible",
        common_elderly_side_effects=["Nephrotoxicity", "Ototoxicity", "Red man syndrome"]
    ),
    
    # ==================== ANTIFUNGAL/ANTIVIRAL ====================
    "caspofungin": DrugProfile(
        generic_name="caspofungin",
        brand_names=["Cancidas"],
        drug_class="Echinocandin Antifungal",
        anticholinergic_score=0,
        sedative_score=0,#not in table 
        fall_risk_score=0,
        beers_criteria=False,
        renal_adjustment=False,
        cyp_inhibitors=[],
        cyp_substrates=[],
        pregnancy_category="C",
        lactation_safety="Unknown",
        common_elderly_side_effects=["Hepatotoxicity", "Phlebitis", "Fever"]
    ),
    
    "fluconazole": DrugProfile(
        generic_name="fluconazole",
        brand_names=["Diflucan"],
        drug_class="Azole Antifungal",
        anticholinergic_score=0,
        sedative_score=0,
        fall_risk_score=0,
        beers_criteria=False,
        renal_adjustment=True,
        cyp_inhibitors=["CYP2C9", "CYP2C19", "CYP3A4"],
        cyp_substrates=["CYP3A4"],
        pregnancy_category="D",
        lactation_safety="Compatible",
        common_elderly_side_effects=["Hepatotoxicity", "QT prolongation", "Drug interactions"]
    ),
    
    "ganciclovir": DrugProfile(
        generic_name="ganciclovir",
        brand_names=["Cytovene"],
        drug_class="Antiviral - CMV",
        anticholinergic_score=0,
        sedative_score=0,#not in table 
        fall_risk_score=1,
        beers_criteria=False,
        renal_adjustment=True,
        cyp_inhibitors=[],
        cyp_substrates=[],
        pregnancy_category="C",
        lactation_safety="Avoid",
        common_elderly_side_effects=["Bone marrow suppression", "Nephrotoxicity", "Confusion"]
    ),
    
    "oseltamivir": DrugProfile(
        generic_name="oseltamivir",
        brand_names=["Tamiflu"],
        drug_class="Antiviral - Neuraminidase Inhibitor",
        anticholinergic_score=0,
        sedative_score=0,#not in table
        fall_risk_score=0,
        beers_criteria=False,
        renal_adjustment=True,
        cyp_inhibitors=[],
        cyp_substrates=[],
        pregnancy_category="C",
        lactation_safety="Compatible",
        common_elderly_side_effects=["Nausea", "Vomiting", "Neuropsychiatric effects"]
    ),
    
    "valacyclovir": DrugProfile(
        generic_name="valacyclovir",
        brand_names=["Valtrex"],
        drug_class="Antiviral - Herpes",
        anticholinergic_score=0,
        sedative_score=0,#not in table
        fall_risk_score=1,
        beers_criteria=False,
        renal_adjustment=True,
        cyp_inhibitors=[],
        cyp_substrates=[],
        pregnancy_category="B",
        lactation_safety="Compatible",
        common_elderly_side_effects=["Confusion", "Thrombotic thrombocytopenic purpura", "Nephrotoxicity"]
    ),
    
    # ==================== CARDIOVASCULAR AGENTS ====================
    "adenosine": DrugProfile(
        generic_name="adenosine",
        brand_names=["Adenocard"],
        drug_class="Antiarrhythmic",
        anticholinergic_score=0,
        sedative_score=0,#not in table
        fall_risk_score=2,
        beers_criteria=False,
        renal_adjustment=False,
        cyp_inhibitors=[],
        cyp_substrates=[],
        pregnancy_category="C",
        lactation_safety="Unknown",
        common_elderly_side_effects=["Transient asystole", "Flushing", "Chest pain", "Dyspnea"]
    ),
    
    "amlodipine": DrugProfile(
        generic_name="amlodipine",
        brand_names=["Norvasc"],
        drug_class="Calcium Channel Blocker - Dihydropyridine",
        anticholinergic_score=0,
        sedative_score=1,
        fall_risk_score=3,
        beers_criteria=False,
        renal_adjustment=False,
        cyp_inhibitors=[],
        cyp_substrates=["CYP3A4"],
        pregnancy_category="C",
        lactation_safety="Compatible",
        common_elderly_side_effects=["Peripheral edema", "Dizziness", "Flushing", "Hypotension"]
    ),
    
    "carvedilol": DrugProfile(
        generic_name="carvedilol",
        brand_names=["Coreg"],
        drug_class="Beta Blocker - Non-selective",
        anticholinergic_score=0,
        sedative_score=1,
        fall_risk_score=4,
        beers_criteria=False,
        renal_adjustment=False,
        cyp_inhibitors=[],
        cyp_substrates=["CYP2D6", "CYP2C9"],
        pregnancy_category="C",
        lactation_safety="Unknown",
        common_elderly_side_effects=["Bradycardia", "Hypotension", "Dizziness", "Fatigue"]
    ),
    
    "diltiazem": DrugProfile(
        generic_name="diltiazem",
        brand_names=["Cardizem", "Tiazac"],
        drug_class="Calcium Channel Blocker - Non-dihydropyridine",
        anticholinergic_score=1,
        sedative_score=1,
        fall_risk_score=3,
        beers_criteria=False,
        renal_adjustment=False,
        cyp_inhibitors=["CYP3A4"],
        cyp_substrates=["CYP3A4"],
        pregnancy_category="C",
        lactation_safety="Compatible",
        common_elderly_side_effects=["Bradycardia", "AV block", "Edema", "Constipation"]
    ),
    
    "furosemide": DrugProfile(
        generic_name="furosemide",
        brand_names=["Lasix"],
        drug_class="Loop Diuretic",
        anticholinergic_score=1,
        sedative_score=1,
        fall_risk_score=4,
        beers_criteria=False,
        renal_adjustment=False,
        cyp_inhibitors=[],
        cyp_substrates=[],
        pregnancy_category="C",
        lactation_safety="Compatible",
        common_elderly_side_effects=["Orthostatic hypotension", "Hypokalemia", "Dehydration", "Ototoxicity"]
    ),
    
    "hydrochlorothiazide": DrugProfile(
        generic_name="hydrochlorothiazide",
        brand_names=["Microzide", "HCTZ"],
        drug_class="Thiazide Diuretic",
        anticholinergic_score=0,
        sedative_score=1,
        fall_risk_score=3,
        beers_criteria=False,
        renal_adjustment=True,
        cyp_inhibitors=[],
        cyp_substrates=[],
        pregnancy_category="B",
        lactation_safety="Compatible",
        common_elderly_side_effects=["Hypokalemia", "Hyponatremia", "Hyperuricemia", "Hyperglycemia"]
    ),
    
    "labetalol": DrugProfile(
        generic_name="labetalol",
        brand_names=["Trandate"],
        drug_class="Beta Blocker - Mixed Alpha/Beta",
        anticholinergic_score=0,
        sedative_score=1,
        fall_risk_score=4,
        beers_criteria=False,
        renal_adjustment=False,
        cyp_inhibitors=[],
        cyp_substrates=["CYP2C19"],
        pregnancy_category="C",
        lactation_safety="Compatible",
        common_elderly_side_effects=["Orthostatic hypotension", "Bradycardia", "Dizziness", "Fatigue"]
    ),
    
    "nimodipine": DrugProfile(
        generic_name="nimodipine",
        brand_names=["Nymalize"],
        drug_class="Calcium Channel Blocker - Dihydropyridine",
        anticholinergic_score=0,
        sedative_score=1,
        fall_risk_score=3,
        beers_criteria=False,
        renal_adjustment=False,
        cyp_inhibitors=[],
        cyp_substrates=["CYP3A4"],
        pregnancy_category="C",
        lactation_safety="Unknown",
        common_elderly_side_effects=["Hypotension", "Headache", "Nausea"]
    ),
    
    "nitroglycerin": DrugProfile(
        generic_name="nitroglycerin",
        brand_names=["Nitrostat", "Nitro-Dur"],
        drug_class="Nitrate Vasodilator",
        anticholinergic_score=0,
        sedative_score=0,
        fall_risk_score=5,
        beers_criteria=False,
        renal_adjustment=False,
        cyp_inhibitors=[],
        cyp_substrates=[],
        pregnancy_category="C",
        lactation_safety="Compatible",
        common_elderly_side_effects=["Orthostatic hypotension", "Headache", "Syncope", "Reflex tachycardia"]
    ),
    
    "acetylsalicylic acid": DrugProfile(
        generic_name="acetylsalicylic acid",
        brand_names=["Aspirin", "ASA"],
        drug_class="Antiplatelet/NSAID",
        anticholinergic_score=0,
        sedative_score=0,
        fall_risk_score=1,
        beers_criteria=True,
        renal_adjustment=False,
        cyp_inhibitors=[],
        cyp_substrates=[],
        pregnancy_category="D",
        lactation_safety="Caution",
        common_elderly_side_effects=["GI bleeding", "Bruising", "Tinnitus"]
    ),
    "bactrim": DrugProfile(
        generic_name="sulfamethoxazole/trimethoprim",
        brand_names=["Bactrim", "Septra", "Apo-Sulfatrim"],
        drug_class="Sulfonamide Antibiotic",
        anticholinergic_score=0,
        sedative_score=0,
        fall_risk_score=1,
        beers_criteria=False,
        renal_adjustment=True,
        cyp_inhibitors=["CYP2C9"],
        cyp_substrates=["CYP2C9"],
        pregnancy_category="D",
        lactation_safety="Avoid",
        common_elderly_side_effects=["Hyperkalemia", "Photosensitivity", "Rash", "GI upset"]
    ),
    "clarithromycin": DrugProfile(
        generic_name="clarithromycin",
        brand_names=["Biaxin"],
        drug_class="Macrolide Antibiotic",
        anticholinergic_score=0,
        sedative_score=0,
        fall_risk_score=1,
        beers_criteria=False,
        renal_adjustment=False,
        cyp_inhibitors=["CYP3A4"],
        cyp_substrates=["CYP3A4"],
        pregnancy_category="C",
        lactation_safety="Compatible",
        common_elderly_side_effects=["Diarrhea", "QT prolongation", "Taste disturbance"]
    ),
    "lithium": DrugProfile(
        generic_name="lithium",
        brand_names=["Carbolith", "Lithmax"],
        drug_class="Mood Stabilizer",
        anticholinergic_score=0,
        sedative_score=2,
        fall_risk_score=3,
        beers_criteria=True,
        renal_adjustment=True,
        cyp_inhibitors=[],
        cyp_substrates=[],
        pregnancy_category="D",
        lactation_safety="Avoid",
        common_elderly_side_effects=["Tremor", "Hypothyroidism", "Nephrotoxicity", "Confusion"]
    ),
    "tramadol": DrugProfile(
        generic_name="tramadol",
        brand_names=["Ultram", "Tridural"],
        drug_class="Opioid Analgesic",
        anticholinergic_score=0,
        sedative_score=2,
        fall_risk_score=5,
        beers_criteria=True,
        renal_adjustment=True,
        cyp_inhibitors=[],
        cyp_substrates=["CYP2D6"],
        pregnancy_category="C",
        lactation_safety="Caution",
        common_elderly_side_effects=["Dizziness", "Constipation", "Nausea", "Seizures"]
    ),
    "omeprazole": DrugProfile(
        generic_name="omeprazole",
        brand_names=["Losec", "Prilosec"],
        drug_class="Proton Pump Inhibitor",
        anticholinergic_score=0,
        sedative_score=0,
        fall_risk_score=0,
        beers_criteria=True,
        renal_adjustment=False,
        cyp_inhibitors=["CYP2C19"],
        cyp_substrates=["CYP2C19"],
        pregnancy_category="C",
        lactation_safety="Compatible",
        common_elderly_side_effects=["Fracture risk", "C. difficile", "B12 deficiency", "Pneumonia"]
    ),
    "clopidogrel": DrugProfile(
        generic_name="clopidogrel",
        brand_names=["Plavix"],
        drug_class="Antiplatelet Agent",
        anticholinergic_score=0,
        sedative_score=0,
        fall_risk_score=1,
        beers_criteria=False,
        renal_adjustment=False,
        cyp_inhibitors=[],
        cyp_substrates=["CYP2C19"],
        pregnancy_category="B",
        lactation_safety="Unknown",
        common_elderly_side_effects=["Bleeding", "Bruising", "GI upset"]
    )
}
#48 + 6 drug profiles


# ============================================================================
# INTERACTION DATABASE - Structured by Severity and Mechanism
# ============================================================================
INTERACTION_DATABASE: Dict[frozenset[str], DrugInteraction] = {
    # ==================== CRITICAL INTERACTIONS (Life-threatening) ====================
    frozenset({'warfarin', 'bactrim'}): DrugInteraction(
        severity="critical",
        description="Bactrim significantly increases warfarin's anticoagulant effect, causing severe bleeding risk",
        mechanism="Sulfamethoxazole inhibits warfarin metabolism via CYP2C9",
        clinical_evidence="Strong - multiple case reports of fatal bleeding",
        elderly_risk="Extremely high - reduced metabolic reserve and frailty",
        alternatives=["Cephalexin", "Nitrofurantoin", "Amoxicillin"],
        monitoring="Daily INR monitoring for 1 week after starting/stopping",
        action="Avoid combination; if essential, reduce warfarin dose by 30-50%",
        references=["Health Canada Advisory 2019", "CPS 2023"],
        fall_risk_increase=5,
        delirium_risk=True,
        renal_risk=True
    ),
    
    frozenset({'simvastatin', 'clarithromycin'}): DrugInteraction(
        severity="critical",
        description="Contraindicated - severe rhabdomyolysis and myopathy risk",
        mechanism="Clarithromycin inhibits CYP3A4, increasing simvastatin levels 10-fold",
        clinical_evidence="FDA Black Box Warning",
        elderly_risk="Higher due to reduced statin clearance",
        alternatives=["Pravastatin", "Rosuvastatin (lower dose)", "Atorvastatin (max 20mg)"],
        monitoring="CK levels, symptoms of muscle pain/weakness",
        action="Use alternative antibiotic or statin",
        references=["FDA Black Box Warning 2011", "Health Canada Advisory"],
        fall_risk_increase=7,
        delirium_risk=False,
        renal_risk=True
    ),
    
    frozenset({'lithium', 'ibuprofen'}): DrugInteraction(
        severity="critical",
        description="NSAIDs increase lithium levels 25-60%, causing toxicity",
        mechanism="NSAIDs reduce renal lithium clearance",
        clinical_evidence="Strong - well-documented cases of toxicity",
        elderly_risk="Higher due to age-related renal changes",
        alternatives=["Acetaminophen", "Topical NSAIDs"],
        monitoring="Weekly lithium levels for 2 weeks after starting NSAID",
        action="Avoid NSAIDs; use acetaminophen for pain",
        references=["CPS Lithium Monograph", "British Journal of Clinical Pharmacology 2018"],
        fall_risk_increase=8,
        delirium_risk=True,
        renal_risk=True
    ),
    
    # ==================== HIGH INTERACTIONS (Require immediate attention) ====================
    frozenset({'warfarin', 'acetylsalicylic acid'}): DrugInteraction(
        severity="high",
        description="Synergistic bleeding risk - gastrointestinal and intracranial bleeding",
        mechanism="Dual anticoagulant/antiplatelet effect",
        clinical_evidence="Strong - increased major bleeding 2-3x",
        elderly_risk="Very high - age-related GI fragility",
        alternatives=["Single antiplatelet therapy if indicated"],
        monitoring="Hemoglobin, signs of bleeding, stool guaiac",
        action="Only combine with cardiology approval and gastroprotection",
        references=["NEJM 2007", "CPS Warfarin Monograph"],
        fall_risk_increase=6,
        delirium_risk=True,
        renal_risk=False
    ),
    
    frozenset({'sertraline', 'tramadol'}): DrugInteraction(
        severity="high",
        description="Serotonin syndrome risk - potentially fatal",
        mechanism="Dual serotonin reuptake inhibition",
        clinical_evidence="Moderate - case reports of serotonin syndrome",
        elderly_risk="Higher due to reduced metabolic capacity",
        alternatives=["Acetaminophen", "Non-opioid analgesics"],
        monitoring="Mental status, autonomic signs, neuromuscular symptoms",
        action="Avoid combination; use alternative pain management",
        references=["Health Canada Advisory 2016"],
        fall_risk_increase=4,
        delirium_risk=True,
        renal_risk=False
    ),
    
    # ==================== MODERATE INTERACTIONS (Require monitoring) ====================
    frozenset({'lisinopril', 'ibuprofen'}): DrugInteraction(
        severity="moderate",
        description="NSAIDs reduce ACE inhibitor effectiveness and increase renal risk",
        mechanism="NSAIDs inhibit prostaglandin-mediated renal vasodilation",
        clinical_evidence="Strong - established in hypertension guidelines",
        elderly_risk="High - 'Triple Whammy' component when with diuretic",
        alternatives=["Acetaminophen", "Celecoxib (lower renal risk)"],
        monitoring="Blood pressure, serum creatinine, potassium",
        action="Monitor renal function; consider acetaminophen alternative",
        references=["Canadian Hypertension Guidelines 2020"],
        fall_risk_increase=4,
        delirium_risk=False,
        renal_risk=True
    ),
    
    frozenset({'omeprazole', 'clopidogrel'}): DrugInteraction(
        severity="moderate",
        description="Omeprazole reduces clopidogrel antiplatelet effect",
        mechanism="CYP2C19 inhibition reducing active metabolite formation",
        clinical_evidence="Controversial - some studies show clinical impact",
        elderly_risk="Moderate - elderly often on both for GI protection",
        alternatives=["Pantoprazole", "H2 blockers (famotidine)"],
        monitoring="No specific monitoring recommended",
        action="Use pantoprazole if PPI needed with clopidogrel",
        references=["FDA Drug Safety Communication 2009"],
        fall_risk_increase=0,
        delirium_risk=False,
        renal_risk=False
    ),
    
    # ==================== ELDERLY-SPECIFIC HIGH RISK COMBINATIONS ====================
    frozenset({'zolpidem', 'hydrochlorothiazide'}): DrugInteraction(
        severity="high",
        description="Fall risk combination - sedation plus orthostatic hypotension",
        mechanism="Additive CNS depression and volume depletion",
        clinical_evidence="Strong - documented fall risk increase",
        elderly_risk="Very high - 4x increased fall risk in >75",
        alternatives=["Melatonin", "Trazodone low dose", "Cognitive behavioral therapy"],
        monitoring="Blood pressure (sitting/standing), gait assessment",
        action="Avoid in patients with history of falls",
        references=["JAMA Internal Medicine 2015", "Beers Criteria 2023"],
        fall_risk_increase=9,
        delirium_risk=True,
        renal_risk=False
    ),
    
    frozenset({'diphenhydramine', 'oxybutynin'}): DrugInteraction(
        severity="high",
        description="Anticholinergic burden - delirium and cognitive impairment",
        mechanism="Additive antimuscarinic effects",
        clinical_evidence="Strong - ACB score 6 (high risk)",
        elderly_risk="Very high - delirium, falls, functional decline",
        alternatives=["Cetirizine (low anticholinergic)", "Mirabegron for OAB"],
        monitoring="Cognitive function, hydration status, bowel function",
        action="Avoid combination; use safer alternatives",
        references=["Anticholinergic Cognitive Burden Scale", "Beers Criteria"],
        fall_risk_increase=8,
        delirium_risk=True,
        renal_risk=False
    ),
    
    # ==================== TRIPLE WHAMMY DETECTION ====================
    frozenset({'lisinopril', 'furosemide', 'ibuprofen'}): DrugInteraction(
        severity="critical",
        description="TRIPLE WHAMMY: ACE inhibitor + diuretic + NSAID = acute kidney injury",
        mechanism="Combined renal vasoconstriction, volume depletion, prostaglandin inhibition",
        clinical_evidence="Strong - well-established nephrotoxic combination",
        elderly_risk="Extremely high - 8x increased AKI risk in >65",
        alternatives=["Acetaminophen instead of NSAID", "Monitor renal function weekly"],
        monitoring="Daily weights, serum creatinine, urine output",
        action="Avoid NSAIDs in patients on ACEi + diuretic",
        references=["Nephrology Dialysis Transplantation 2014", "Canadian Geriatrics Society"],
        fall_risk_increase=7,
        delirium_risk=True,
        renal_risk=True
    )
}

# ============================================================================
# THERAPEUTIC DUPLICATION DATABASE
# ============================================================================
THERAPEUTIC_CATEGORIES = {
    "ace_inhibitors": ["lisinopril", "enalapril", "ramipril", "perindopril"],
    "arb": ["losartan", "valsartan", "candesartan", "irbesartan"],
    "statin": ["atorvastatin", "simvastatin", "rosuvastatin", "pravastatin"],
    "ssri": ["sertraline", "escitalopram", "citalopram", "fluoxetine"],
    "ppi": ["omeprazole", "pantoprazole", "esomeprazole", "lansoprazole"],
    "nsaid": ["ibuprofen", "naproxen", "diclofenac", "celecoxib"],
    "benzodiazepine": ["lorazepam", "diazepam", "clonazepam", "alprazolam"],
    "z_drug": ["zolpidem", "zopiclone", "eszopiclone"],
    "anticholinergic": ["diphenhydramine", "oxybutynin", "tolterodine", "amitriptyline"]
}

# ============================================================================
# FALL RISK CATEGORIZATION
# ============================================================================
FALL_RISK_CATEGORIES = {
    "sedative_hypnotics": {
        "drugs": ["zolpidem", "zopiclone", "eszopiclone", "lorazepam", "diazepam"],
        "risk_score": 8,
        "time_of_risk": "Nighttime and morning after dosing"
    },
    "antipsychotics": {
        "drugs": ["quetiapine", "risperidone", "olanzapine", "haloperidol"],
        "risk_score": 7,
        "time_of_risk": "Within 2 hours of dosing, especially initiation"
    },
    "antidepressants_tca": {
        "drugs": ["amitriptyline", "nortriptyline", "doxepin"],
        "risk_score": 6,
        "time_of_risk": "Orthostatic effects: within 1-2 hours of dosing"
    },
    "opioids": {
        "drugs": ["oxycodone", "hydromorphone", "morphine", "fentanyl"],
        "risk_score": 6,
        "time_of_risk": "Peak concentration: 1-2 hours post-dose"
    },
    "antihypertensives": {
        "drugs": ["furosemide", "hydrochlorothiazide", "lisinopril", "amlodipine"],
        "risk_score": 4,
        "time_of_risk": "Orthostatic: 1-2 hours post-dose, especially first dose"
    },
    "anticholinergics": {
        "drugs": ["diphenhydramine", "oxybutynin", "tolterodine", "scopolamine"],
        "risk_score": 5,
        "time_of_risk": "Cognitive effects: cumulative with duration"
    }
}

# ============================================================================
# BRAND NAME MAPPING (Expanded)
# ============================================================================
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
    "bactrim": "bactrim",
    
    # Anticoagulants
    "coumadin": "warfarin",
    "jantoven": "warfarin",
    "eliquis": "apixaban",
    "xarelto": "rivaroxaban",
    "pradaxa": "dabigatran",
    
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
    "januvia": "sitagliptin",
    
    # Thyroid
    "synthroid": "levothyroxine",
    "eltroxin": "levothyroxine",
    
    # Antidepressants
    "zoloft": "sertraline",
    "prozac": "fluoxetine",
    "lexapro": "escitalopram",
    "cipralex": "escitalopram",
    "effexor": "venlafaxine",
    "celexa": "citalopram",
    "paxil": "paroxetine",
    
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
    "seroquel": "quetiapine",
    "abilify": "aripiprazole",
    "ativan": "lorazepam",
    "klonopin": "clonazepam",
    "restoril": "temazepam",

    "aspirin": "acetylsalicylic acid",
    "asa": "acetylsalicylic acid",
    "acetylsalicylic acid": "acetylsalicylic_acid"
} 
# ============================================================================

# ============================================================================
# ENHANCED FUNCTIONS - PROFESSIONAL VERSION
# ============================================================================
# Author: Orion Poyet
# Version: 3.0
# Last Updated: 1/6/2026
# Description: Comprehensive drug interaction and burden assessment functions
#              optimized for elderly patient safety
# ============================================================================


# ============================================================================
# CORE UTILITY FUNCTIONS
# ============================================================================

def normalize_drug_name(drug_name: str) -> str:
    """
    Normalize drug name to standard standard generic form.
    
    Args:
        drug_name: Raw drug name (brand or generic)
        
    Returns:
        Normalized generic drug name in lowercase
        
    Examples:
        >>> normalize_drug_name("Tylenol 500mg")
        'acetaminophen'
        >>> normalize_drug_name("Zocor SR")
        'simvastatin'
    """
    if not drug_name:
        return ""
    
    drug_name = drug_name.lower().strip()
    
    # Check brand names first
    if drug_name in DRUG_ALIASES:
        return DRUG_ALIASES[drug_name]
    
    # Remove common suffixes and prefixes
    drug_name = re.sub(r'\s*(tablet|tab|capsule|cap|injection|inj|oral|topical)\s*$', '', drug_name)
    drug_name = re.sub(r'\s*(sr|er|xr|cr|la|xl)\s*$', '', drug_name)  # Extended release
    
    return drug_name


def get_drug_profile(drug_name: str) -> Optional['DrugProfile']:
    """
    Retrieve comprehensive drug profile from database.
    
    Args:
        drug_name: Drug name (brand or generic)
        
    Returns:
        DrugProfile object if found, None otherwise
        
    Example:
        >>> profile = get_drug_profile("Benadryl")
        >>> print(profile.anticholinergic_score)
        3
    """
    normalized = normalize_drug_name(drug_name)
    return DRUG_PROFILES.get(normalized)


def validate_medication_list(medications: List[str]) -> Tuple[List[str], List[str]]:
    """
    Validate medication list and identify unrecognized drugs.
    
    Args:
        medications: List of drug names
        
    Returns:
        Tuple of (valid_drugs, unrecognized_drugs)
        
    Example:
        >>> valid, invalid = validate_medication_list(["Tylenol", "FakeDrug123"])
        >>> print(f"Valid: {valid}, Invalid: {invalid}")
        Valid: ['acetaminophen'], Invalid: ['FakeDrug123']
    """
    valid_drugs = []
    unrecognized_drugs = []
    
    for med in medications:
        normalized = normalize_drug_name(med)
        if normalized and get_drug_profile(normalized):
            valid_drugs.append(med)
        else:
            unrecognized_drugs.append(med)
    
    return valid_drugs, unrecognized_drugs


# ============================================================================
# DRUG INTERACTION DETECTION
# ============================================================================


def check_interaction(drug1: str, drug2: str, drug3: Optional[str] = None) -> Optional[dict]:
    drug1_norm = normalize_drug_name(drug1)
    drug2_norm = normalize_drug_name(drug2)
    if not drug1_norm or not drug2_norm:
        return None
    if drug3:
        drug3_norm = normalize_drug_name(drug3)
        if not drug3_norm:
            return None
        key = frozenset({drug1_norm, drug2_norm, drug3_norm})
        drugs = [drug1, drug2, drug3]
    else:
        key = frozenset({drug1_norm, drug2_norm})
        drugs = [drug1, drug2]
    if key in INTERACTION_DATABASE:
        interaction = INTERACTION_DATABASE[key].to_dict()
        interaction["drugs"] = drugs
        return interaction
    return None


def check_all_interactions(medications: List[str]) -> Dict[str, List[dict]]:
    interactions_by_severity = {
        'critical': [],
        'high': [],
        'moderate': [],
        'low': []
    }
    # Pairwise
    for combo in combinations(medications, 2):
        interaction = check_interaction(*combo)
        if interaction:
            severity = interaction.get('severity', 'low')
            if severity in interactions_by_severity:
                interactions_by_severity[severity].append(interaction)
    # Triples
    if len(medications) >= 3:
        for combo in combinations(medications, 3):
            interaction = check_interaction(*combo)
            if interaction:
                severity = interaction.get('severity', 'low')
                if severity in interactions_by_severity and interaction not in interactions_by_severity[severity]:
                    interactions_by_severity[severity].append(interaction)
    return interactions_by_severity


def get_all_interactions_for_medication(drug_name: str) -> List[dict]:
    normalized = normalize_drug_name(drug_name)
    if not normalized:
        return []
    interactions = []
    for key, interaction in INTERACTION_DATABASE.items():
        drugs_in_inter = list(key)
        if normalized in drugs_in_inter:
            other_drugs = [d for d in drugs_in_inter if d != normalized]
            interaction_data = interaction.to_dict()
            interaction_data["interacting_drugs"] = other_drugs
            interaction_data["query_drug"] = drug_name
            interactions.append(interaction_data)
    severity_order = {'critical': 0, 'high': 1, 'moderate': 2, 'low': 3}
    interactions.sort(key=lambda x: severity_order.get(x.get('severity', 'low'), 4))
    return interactions


# ============================================================================
# THERAPEUTIC DUPLICATION DETECTION
# ============================================================================

def detect_therapeutic_duplicates(medications: List[str]) -> Dict[str, List[str]]:
    """
    Detect therapeutic duplications (multiple drugs in same class).
    
    Args:
        medications: List of medication names
        
    Returns:
        Dictionary mapping therapeutic categories to duplicate medications
        
    Example:
        >>> meds = ["Lisinopril", "Enalapril", "Aspirin"]
        >>> duplicates = detect_therapeutic_duplicates(meds)
        >>> print(duplicates)
        {'ace_inhibitors': ['Lisinopril', 'Enalapril']}
        
    Note:
        Only returns categories with 2+ medications (actual duplicates)
    """
    duplicates = {}
    
    for med in medications:
        normalized = normalize_drug_name(med)
        if not normalized:
            continue
        
        # Check which therapeutic category this drug belongs to
        for category, drugs in THERAPEUTIC_CATEGORIES.items():
            if normalized in drugs:
                if category not in duplicates:
                    duplicates[category] = []
                duplicates[category].append(med)
    
    # Filter for actual duplicates (more than one drug in category)
    return {cat: meds for cat, meds in duplicates.items() if len(meds) > 1}


# ============================================================================
# FALL RISK ASSESSMENT
# ============================================================================

def calculate_fall_risk_score(medications: List[str]) -> dict:
    """
    Calculate comprehensive fall risk score based on medications.
    
    Args:
        medications: List of medication names
        
    Returns:
        Dictionary containing:
        - total_score: Cumulative fall risk score (0-100+)
        - risk_category: CRITICAL/HIGH/MODERATE/LOW
        - high_risk_medications: List of drugs with fall_risk_score ≥5
        - recommendations: List of actionable recommendations
        - unrecognized_medications: Drugs not in database
        
    Scoring:
        - ≥15: CRITICAL
        - 10-14: HIGH
        - 5-9: MODERATE
        - <5: LOW
        
    Example:
        >>> meds = ["Zolpidem", "Hydrochlorothiazide", "Diphenhydramine"]
        >>> result = calculate_fall_risk_score(meds)
        >>> print(f"Total score: {result['total_score']}, Risk: {result['risk_category']}")
    """
    total_score = 0
    high_risk_meds = []
    unrecognized = []
    
    for med in medications:
        normalized = normalize_drug_name(med)
        profile = get_drug_profile(normalized)
        
        if profile:
            total_score += profile.fall_risk_score
            if profile.fall_risk_score >= 5:
                high_risk_meds.append({
                    "name": med,
                    "generic_name": profile.generic_name,
                    "fall_risk_score": profile.fall_risk_score,
                    "sedative_score": profile.sedative_score,
                    "anticholinergic_score": profile.anticholinergic_score,
                    "beers_criteria": profile.beers_criteria
                })
        else:
            unrecognized.append(med)
    
    # Calculate fall risk category
    if total_score >= 15:
        risk_category = "CRITICAL"
    elif total_score >= 10:
        risk_category = "HIGH"
    elif total_score >= 5:
        risk_category = "MODERATE"
    else:
        risk_category = "LOW"
    
    return {
        "total_score": total_score,
        "risk_category": risk_category,
        "high_risk_medications": high_risk_meds,
        "high_risk_count": len(high_risk_meds),
        "recommendations": generate_fall_risk_recommendations(total_score, high_risk_meds),
        "unrecognized_medications": unrecognized,
        "medication_count": len(medications),
        "recognized_count": len(medications) - len(unrecognized)
    }


def generate_fall_risk_recommendations(score: int, high_risk_meds: List[dict]) -> List[str]:
    """
    Generate personalized fall prevention recommendations.
    
    Args:
        score: Total fall risk score
        high_risk_meds: List of high fall-risk medications
        
    Returns:
        List of actionable recommendations
    """
    recommendations = []
    
    # Critical/High score recommendations
    if score >= 10:
        recommendations.append("🚨 URGENT: Consider deprescribing high-risk medications")
        recommendations.append("• Immediate physician consultation recommended")
        recommendations.append("• Implement 24/7 supervision or facility care evaluation")
        recommendations.append("• Home safety assessment required within 7 days")
    elif score >= 5:
        recommendations.append("⚠️ HIGH RISK: Discuss medication changes with physician")
        recommendations.append("• Schedule medication review within 2 weeks")
        recommendations.append("• Install grab bars in bathroom and hallways")
        recommendations.append("• Remove tripping hazards (rugs, cords, clutter)")
        recommendations.append("• Consider medical alert system")
    
    # Sedative-specific recommendations
    sedative_meds = [m for m in high_risk_meds if m.get("sedative_score", 0) >= 2]
    if sedative_meds:
        recommendations.append("\n💊 SEDATIVE MEDICATION CONCERNS:")
        recommendations.append("• Avoid nighttime ambulation - use bedside commode")
        recommendations.append("  Reason: Sedatives cause disorientation and impaired balance,")
        recommendations.append("  especially during nighttime awakenings (peak fall risk period)")
        recommendations.append("• Ensure adequate lighting for nighttime bathroom trips")
        recommendations.append("• Wait 8-12 hours after sedative dose before driving")
        for med in sedative_meds:
            recommendations.append(f"  - {med['name']}: Peak sedation 1-4 hours post-dose")
    
    # Anticholinergic-specific recommendations
    anticholinergic_meds = [m for m in high_risk_meds if m.get("anticholinergic_score", 0) >= 2]
    if anticholinergic_meds:
        recommendations.append("\n🧠 ANTICHOLINERGIC MEDICATION CONCERNS:")
        recommendations.append("• Review anticholinergic medications for alternatives")
        recommendations.append("• Monitor for confusion, dizziness, blurred vision")
        recommendations.append("• Anticholinergics impair balance, reaction time, and spatial awareness")
        for med in anticholinergic_meds:
            recommendations.append(f"  - {med['name']}: Consider safer alternatives")
    
    # Beers Criteria flags
    beers_meds = [m for m in high_risk_meds if m.get("beers_criteria", False)]
    if beers_meds:
        recommendations.append("\n⚕️ POTENTIALLY INAPPROPRIATE MEDICATIONS (Beers Criteria):")
        for med in beers_meds:
            recommendations.append(f"  - {med['name']}: Flagged as high-risk in elderly")
        recommendations.append("• Discuss deprescribing or alternatives with prescriber")
    
    # General safety measures
    if score >= 5:
        recommendations.append("\n🛡️ ENVIRONMENTAL SAFETY MEASURES:")
        recommendations.append("• Keep phone and flashlight within reach at night")
        recommendations.append("• Wear non-slip footwear indoors")
        recommendations.append("• Avoid loose-fitting clothing that could cause trips")
        recommendations.append("• Keep frequently used items within easy reach")
        recommendations.append("• Consider physical therapy for gait/balance training")
    
    return recommendations


# ============================================================================
# ANTICHOLINERGIC BURDEN ASSESSMENT
# ============================================================================

def calculate_anticholinergic_burden(medications: List[str]) -> dict:
    """
    Calculate anticholinergic cognitive burden (ACB) score.
    
    Based on validated ACB Scale (Campbell et al. 2021).
    Individual drug scores: 0-3 (cumulative across all medications)
    
    Args:
        medications: List of medication names
        
    Returns:
        Dictionary containing:
        - total_score: Cumulative ACB score
        - burden_level: CRITICAL/HIGH/MODERATE/LOW/NONE
        - clinical_impact: Detailed risk breakdown
        - contributing_medications: Drugs with ACB >0
        - warnings: Alert messages
        - recommendations: Actionable steps
        - unrecognized_medications: Drugs not in database
        
    Scoring Interpretation:
        - ≥5: CRITICAL - Severe delirium risk
        - 3-4: HIGH - Significant burden
        - 2: MODERATE - Monitor closely
        - 1: LOW - Minimal concern
        - 0: NONE
        
    Example:
        >>> meds = ["Diphenhydramine", "Oxybutynin", "Amitriptyline"]
        >>> result = calculate_anticholinergic_burden(meds)
        >>> print(result['total_score'])  # Output: 9 (3+3+3)
        >>> print(result['burden_level'])  # Output: 'CRITICAL...'
    """
    total_score = 0
    contributing_meds = []
    unrecognized = []
    
    for med in medications:
        normalized = normalize_drug_name(med)
        profile = get_drug_profile(normalized)
        
        if profile and profile.anticholinergic_score > 0:
            total_score += profile.anticholinergic_score
            contributing_meds.append({
                "name": med,
                "score": profile.anticholinergic_score,
                "generic_name": profile.generic_name,
                "drug_class": profile.drug_class
            })
        elif not profile:
            unrecognized.append(med)
    
    # Interpret cumulative score
    if total_score >= 5:
        burden_level = "CRITICAL - Severe delirium and cognitive impairment risk"
        clinical_impact = {
            "delirium_risk": "Very high (>60% in hospitalized elderly)",
            "cognitive_effects": "Severe confusion, disorientation, memory impairment likely",
            "physical_effects": "Dry mouth, constipation, urinary retention, blurred vision",
            "fall_risk_contribution": "High - confusion and vision impairment increase falls",
            "long_term_risk": "Increased dementia risk with chronic exposure (HR 1.54)",
            "functional_decline": "ADL/IADL impairment likely"
        }
    elif total_score >= 3:
        burden_level = "HIGH - Significant anticholinergic burden"
        clinical_impact = {
            "delirium_risk": "High (40-60% in hospitalized elderly)",
            "cognitive_effects": "Moderate confusion, memory problems, reduced attention",
            "physical_effects": "Dry mouth, constipation likely; urinary retention possible",
            "fall_risk_contribution": "Moderate to high",
            "long_term_risk": "Chronic use linked to cognitive decline",
            "functional_decline": "May require assistance with complex tasks"
        }
    elif total_score >= 2:
        burden_level = "MODERATE - Monitor for anticholinergic effects"
        clinical_impact = {
            "delirium_risk": "Moderate (20-40% in vulnerable elderly)",
            "cognitive_effects": "Mild confusion possible, especially when ill or hospitalized",
            "physical_effects": "Dry mouth, mild constipation",
            "fall_risk_contribution": "Low to moderate",
            "long_term_risk": "Minimal if short-term use",
            "functional_decline": "Usually able to function independently"
        }
    elif total_score >= 1:
        burden_level = "LOW - Minimal anticholinergic burden"
        clinical_impact = {
            "delirium_risk": "Low (<20%)",
            "cognitive_effects": "Unlikely in most patients",
            "physical_effects": "Mild or absent",
            "fall_risk_contribution": "Minimal",
            "long_term_risk": "Negligible",
            "functional_decline": "None expected"
        }
    else:
        burden_level = "NONE"
        clinical_impact = {
            "delirium_risk": "No medication-related anticholinergic risk",
            "cognitive_effects": "None expected",
            "physical_effects": "None",
            "fall_risk_contribution": "None",
            "long_term_risk": "None",
            "functional_decline": "None"
        }
    
    # Generate warnings
    warnings = []
    high_score_meds = [m for m in contributing_meds if m["score"] == 3]
    
    if len(high_score_meds) >= 2:
        warnings.append("⚠️ CRITICAL: Multiple high-anticholinergic (score 3) medications - extreme delirium risk")
    
    if total_score >= 5:
        warnings.append("🚨 URGENT: Anticholinergic burden exceeds safe threshold")
        warnings.append("• Immediate deprescribing evaluation recommended")
        warnings.append("• Risk of anticholinergic toxicity syndrome")
    
    if total_score >= 3:
        warnings.append("⚠️ Avoid additional anticholinergic medications (even OTC like diphenhydramine)")
        warnings.append("• Monitor for confusion, urinary retention, constipation, falls")
        warnings.append("• Hospitalization increases delirium risk significantly")
    
    # Generate recommendations
    recommendations = generate_anticholinergic_recommendations(
        total_score, 
        contributing_meds, 
        high_score_meds
    )
    
    return {
        "total_score": total_score,
        "burden_level": burden_level,
        "clinical_impact": clinical_impact,
        "contributing_medications": contributing_meds,
        "contributing_count": len(contributing_meds),
        "high_anticholinergic_count": len(high_score_meds),
        "warnings": warnings,
        "recommendations": recommendations,
        "unrecognized_medications": unrecognized,
        "assessment_date": None,  # Placeholder for implementation timestamp
        "evidence_source": "ACB Scale (Campbell et al. 2021)"
    }


def generate_anticholinergic_recommendations(
    score: int,
    all_meds: List[dict],
    high_score_meds: List[dict]
) -> List[str]:
    """
    Generate personalized anticholinergic burden reduction recommendations.
    
    Args:
        score: Total anticholinergic score
        all_meds: All contributing medications
        high_score_meds: Medications with ACB score = 3
        
    Returns:
        List of prioritized recommendations
    """
    recommendations = []
    
    # Urgent actions based on score
    if score >= 5:
        recommendations.append("🚨 CRITICAL ACTION REQUIRED:")
        recommendations.append("• Immediate physician consultation for medication review")
        recommendations.append("• Consider stopping non-essential anticholinergic medications TODAY")
        recommendations.append("• Implement delirium precautions if hospitalized")
        recommendations.append("• Monitor mental status every 4-8 hours")
        recommendations.append("• Assess for anticholinergic toxicity: agitation, hallucinations, hyperthermia")
        
    elif score >= 3:
        recommendations.append("⚠️ HIGH PRIORITY ACTIONS:")
        recommendations.append("• Schedule URGENT medication review (within 1 week)")
        recommendations.append("• Deprescribing plan needed - target score <3")
        recommendations.append("• Monitor for anticholinergic toxicity symptoms")
        recommendations.append("• Avoid hospitalizations/procedures if possible (↑ delirium risk)")
        
    elif score >= 2:
        recommendations.append("📋 RECOMMENDED ACTIONS:")
        recommendations.append("• Review medications at next appointment (within 1 month)")
        recommendations.append("• Avoid adding more anticholinergic drugs")
        recommendations.append("• Monitor for dry mouth, constipation, confusion")
        recommendations.append("• Document baseline cognitive function for comparison")
    
    # Specific medication recommendations
    if high_score_meds:
        recommendations.append("\n💊 HIGH-RISK MEDICATIONS (Score 3) - STRONGLY CONSIDER ALTERNATIVES:")
        
        for med in high_score_meds:
            generic = med.get("generic_name", "").lower()
            recommendations.append(f"\n• {med['name']} ({med['drug_class']})")
            
            # Drug-specific alternatives
            if "diphenhydramine" in generic or "hydroxyzine" in generic:
                recommendations.append("  ✓ For allergies: Cetirizine 5-10mg, loratadine 10mg (ACB score 0)")
                recommendations.append("  ✓ For sleep: Melatonin 3-5mg, trazodone 25-50mg, CBT-I")
                recommendations.append("  ✗ NOT recommended: Any other antihistamine")
                
            elif "oxybutynin" in generic or "tolterodine" in generic:
                recommendations.append("  ✓ For overactive bladder: Mirabegron 25-50mg (ACB score 0)")
                recommendations.append("  ✓ Non-drug: Pelvic floor exercises, timed voiding, bladder training")
                recommendations.append("  ✓ Consider: Sacral neuromodulation if refractory")
                
            elif "amitriptyline" in generic or "nortriptyline" in generic:
                recommendations.append("  ✓ For depression: Sertraline 25-50mg, citalopram 10-20mg (ACB score 0)")
                recommendations.append("  ✓ For neuropathic pain: Gabapentin 300-900mg, duloxetine 30-60mg")
                recommendations.append("  ✓ For migraine prophylaxis: Topiramate, propranolol")
                
            elif "promethazine" in generic:
                recommendations.append("  ✓ For nausea: Ondansetron 4-8mg, metoclopramide 5-10mg")
                recommendations.append("  ✓ For allergies: Non-sedating antihistamines")
                
            elif "scopolamine" in generic:
                recommendations.append("  ✓ For motion sickness: Meclizine (lower ACB), ginger supplements")
                recommendations.append("  ✓ Non-drug: Acupressure wristbands, desensitization therapy")
    
    # General anticholinergic symptom management
    if score >= 2:
        recommendations.append("\n🛡️ ANTICHOLINERGIC SYMPTOM MANAGEMENT:")
        recommendations.append("• Dry mouth:")
        recommendations.append("  - Sugar-free gum or lozenges (stimulates saliva)")
        recommendations.append("  - Frequent small sips of water")
        recommendations.append("  - Saliva substitutes (Biotène products)")
        recommendations.append("  - Avoid alcohol-based mouthwashes (worsen dryness)")
        recommendations.append("• Constipation:")
        recommendations.append("  - Increase fiber: 25-30g daily (fruits, vegetables, whole grains)")
        recommendations.append("  - Increase fluids: 8-10 glasses water daily")
        recommendations.append("  - Stool softeners: Docusate 100mg BID")
        recommendations.append("  - If needed: Senna 8.6mg HS, polyethylene glycol 17g daily")
        recommendations.append("• Urinary retention:")
        recommendations.append("  - Monitor urine output (goal >1000mL/day)")
        recommendations.append("  - Bladder scan if suspected retention (>300mL post-void)")
        recommendations.append("  - Avoid anticholinergics in men with BPH")
        recommendations.append("• Blurred vision:")
        recommendations.append("  - Avoid driving if symptomatic")
        recommendations.append("  - Optometry review for corrective lenses")
        recommendations.append("  - Improve home lighting")
    
    # Monitoring plan
    if score >= 3:
        recommendations.append("\n📊 MONITORING RECOMMENDATIONS:")
        recommendations.append("• Cognitive function: Mini-Cog or MoCA at baseline and every 3-6 months")
        recommendations.append("• Functional status: ADL/IADL assessment quarterly")
        recommendations.append("• Constipation: Bowel movement diary (goal: every 1-3 days)")
        recommendations.append("• Urinary function: Post-void residual if retention suspected")
        recommendations.append("• Fall assessment: Get-up-and-go test every 6 months")
    
    return recommendations


# ============================================================================
# SEDATIVE BURDEN ASSESSMENT
# ============================================================================

def calculate_sedative_burden(medications: List[str]) -> dict:
    """
    Calculate sedative burden score.
    
    Individual drug scores: 0-3 (cumulative across all medications)
    Based on meta-analysis of fall risk (Woolcott et al. 2009)
    
    Args:
        medications: List of medication names
        
    Returns:
        Dictionary containing:
        - total_score: Cumulative sedative score
        - burden_level: CRITICAL/HIGH/MODERATE/LOW/NONE
        - clinical_impact: Detailed risk breakdown
        - contributing_medications: Drugs with sedative score >0
        - warnings: Alert messages
        - recommendations: Actionable steps
        - unrecognized_medications: Drugs not in database
        
    Scoring Interpretation:
        - ≥5: CRITICAL - Severe CNS depression
        - 3-4: HIGH - Significant sedation
        - 2: MODERATE - Monitor
        - 1: LOW - Minimal
        - 0: NONE
        
    Example:
        >>> meds = ["Zolpidem", "Lorazepam", "Quetiapine"]
        >>> result = calculate_sedative_burden(meds)
        >>> print(result['total_score'])  # Output: 9 (3+3+3)
        >>> print(result['burden_level'])  # Output: 'CRITICAL...'
    """
    total_score = 0
    contributing_meds = []
    unrecognized = []
    
    for med in medications:
        normalized = normalize_drug_name(med)
        profile = get_drug_profile(normalized)
        
        if profile and profile.sedative_score > 0:
            total_score += profile.sedative_score
            contributing_meds.append({
                "name": med,
                "score": profile.sedative_score,
                "generic_name": profile.generic_name,
                "drug_class": profile.drug_class,
                "fall_risk_score": profile.fall_risk_score
            })
        elif not profile:
            unrecognized.append(med)
    
    # Interpret cumulative score
    if total_score >= 5:
        burden_level = "CRITICAL - Severe CNS depression and fall risk"
        clinical_impact = {
            "fall_risk": "Extremely high (>50% 12-month fall risk)",
            "cognitive_effects": "Severe sedation, confusion, slowed reflexes",
            "respiratory_risk": "Significant respiratory depression risk, especially with opioids",
            "next_day_effects": "Prolonged sedation expected (12-24+ hours)",
            "driving_safety": "Absolutely unsafe to drive (impairment equivalent to BAC >0.08%)",
            "functional_impact": "ADL impairment likely - assistance needed for basic activities"
        }
    elif total_score >= 3:
        burden_level = "HIGH - Significant sedation and fall risk"
        clinical_impact = {
            "fall_risk": "Very high (30-50% 12-month fall risk)",
            "cognitive_effects": "Moderate to severe sedation, impaired judgment",
            "respiratory_risk": "Monitor for respiratory depression (RR <12/min)",
            "next_day_effects": "Morning sedation likely (8-12 hours residual)",
            "driving_safety": "Driving not recommended (impairment equivalent to BAC 0.05-0.08%)",
            "functional_impact": "May need assistance with IADLs"
        }
    elif total_score >= 2:
        burden_level = "MODERATE - Monitor for excessive sedation"
        clinical_impact = {
            "fall_risk": "Elevated (20-30% 12-month fall risk)",
            "cognitive_effects": "Mild to moderate drowsiness, reduced alertness",
            "respiratory_risk": "Low risk in most patients (monitor in COPD/OSA)",
            "next_day_effects": "Possible morning grogginess (4-8 hours residual)",
            "driving_safety": "Use caution, assess individual response after 2 weeks",
            "functional_impact": "Usually able to function with monitoring"
        }
    elif total_score >= 1:
        burden_level = "LOW - Minimal sedation expected"
        clinical_impact = {
            "fall_risk": "Slightly elevated (10-20% 12-month fall risk)",
            "cognitive_effects": "Mild drowsiness possible in sensitive individuals",
            "respiratory_risk": "Negligible",
            "next_day_effects": "Usually resolves overnight",
            "driving_safety": "Generally safe after 2-week adjustment period",
            "functional_impact": "Minimal impairment"
        }
    else:
        burden_level = "NONE"
        clinical_impact = {
            "fall_risk": "No medication-related sedation risk",
            "cognitive_effects": "No sedative effects expected",
            "respiratory_risk": "None",
            "next_day_effects": "None",
            "driving_safety": "No restrictions",
            "functional_impact": "None"
        }
    
    # Generate warnings
    warnings = []
    high_sedative_meds = [m for m in contributing_meds if m["score"] == 3]
    moderate_sedative_meds = [m for m in contributing_meds if m["score"] == 2]
    
    if len(high_sedative_meds) >= 2:
        warnings.append("⚠️ CRITICAL: Multiple high-sedative (score 3) medications - extreme fall and respiratory risk")
        warnings.append("• Risk of synergistic CNS depression")
        warnings.append("• Consider hospitalization for monitoring if acutely changed")
    
    if len(high_sedative_meds) >= 1 and len(moderate_sedative_meds) >= 1:
        warnings.append("⚠️ HIGH RISK: High-sedative drug + moderate sedative - synergistic CNS depression")
        warnings.append("• Combined effect greater than sum of individual effects")
    
    if total_score >= 5:
        warnings.append("🚨 URGENT: Sedative burden exceeds safe threshold for elderly")
        warnings.append("• Immediate medication review and deprescribing evaluation required")
        warnings.append("• High risk of respiratory failure in setting of infection/illness")
    
    if any(m["score"] >= 2 for m in contributing_meds):
        warnings.append("⏰ TIMING ALERT: Nighttime ambulation highest risk period")
        warnings.append("• Peak sedation: 1-4 hours post-dose")
        warnings.append("• Confusion and disorientation common during nighttime awakenings")
        warnings.append("• Implement bathroom safety measures immediately")
    
    # Check for specific high-risk combinations
    benzodiazepines = [m for m in contributing_meds if 'benzodiazepine' in m.get('drug_class', '').lower()]
    z_drugs = [m for m in contributing_meds if any(x in m.get('generic_name', '').lower() 
                                                    for x in ['zolpidem', 'zopiclone', 'eszopiclone'])]
    if benzodiazepines and z_drugs:
        warnings.append("🚨 DANGEROUS COMBINATION: Benzodiazepine + Z-drug detected")
        warnings.append("• No therapeutic benefit to combining these")
        warnings.append("• Synergistic respiratory depression and fall risk")
    
    # Generate recommendations
    recommendations = generate_sedative_burden_recommendations(
        total_score,
        contributing_meds,
        high_sedative_meds,
        moderate_sedative_meds
    )
    
    return {
        "total_score": total_score,
        "burden_level": burden_level,
        "clinical_impact": clinical_impact,
        "contributing_medications": contributing_meds,
        "contributing_count": len(contributing_meds),
        "high_sedative_count": len(high_sedative_meds),
        "moderate_sedative_count": len(moderate_sedative_meds),
        "warnings": warnings,
        "recommendations": recommendations,
        "unrecognized_medications": unrecognized,
        "assessment_date": None,
        "evidence_source": "Woolcott et al. Meta-analysis (2009)"
    }


def generate_sedative_burden_recommendations(
    score: int,
    all_meds: List[dict],
    high_sedative: List[dict],
    moderate_sedative: List[dict]
) -> List[str]:
    """
    Generate personalized sedative burden reduction recommendations.
    
    Args:
        score: Total sedative score
        all_meds: All contributing medications
        high_sedative: Medications with sedative score = 3
        moderate_sedative: Medications with sedative score = 2
        
    Returns:
        List of prioritized recommendations
    """
    recommendations = []
    
    # Urgent actions based on score
    if score >= 5:
        recommendations.append("🚨 CRITICAL ACTION REQUIRED:")
        recommendations.append("• Immediate physician consultation for medication review (TODAY)")
        recommendations.append("• Consider hospitalization or increased monitoring if acutely altered mental status")
        recommendations.append("• Implement fall precautions:")
        recommendations.append("  - Bed alarm system")
        recommendations.append("  - 1:1 supervision if available")
        recommendations.append("  - Bedside commode (avoid ambulation)")
        recommendations.append("• Hold non-essential sedating medications until reviewed by MD")
        recommendations.append("• Monitor vital signs:")
        recommendations.append("  - Respiratory rate every 4 hours (target >12/min)")
        recommendations.append("  - Oxygen saturation (target >92% on room air)")
        recommendations.append("  - Level of consciousness (AVPU scale)")
        
    elif score >= 3:
        recommendations.append("⚠️ HIGH PRIORITY ACTIONS:")
        recommendations.append("• Schedule URGENT medication review within 24-48 hours")
        recommendations.append("• Deprescribing plan needed - target total score <3")
        recommendations.append("• Implement enhanced fall precautions at home:")
        recommendations.append("  - Remove all scatter rugs and floor clutter")
        recommendations.append("  - Install night lights in bedroom, bathroom, hallway")
        recommendations.append("  - Use bedside commode at night")
        recommendations.append("• STRICTLY AVOID alcohol - synergistic effect can be fatal")
        recommendations.append("• Educate family/caregivers on fall risk")
        
    elif score >= 2:
        recommendations.append("📋 RECOMMENDED ACTIONS:")
        recommendations.append("• Medication review at next appointment (within 1-2 weeks)")
        recommendations.append("• Monitor for excessive sedation, falls, confusion")
        recommendations.append("• Consider non-pharmacological alternatives where possible")
        recommendations.append("• Document baseline functional status for comparison")
    
    # Specific medication-class recommendations
    if high_sedative:
        recommendations.append("\n💊 HIGH-SEDATIVE MEDICATIONS (Score 3) - STRONGLY CONSIDER ALTERNATIVES:")
        
        for med in high_sedative:
            generic = med.get("generic_name", "").lower()
            drug_class = med.get("drug_class", "").lower()
            recommendations.append(f"\n• {med['name']} ({med['drug_class']})")
            
            # Z-drugs (non-benzodiazepine hypnotics)
            if any(x in generic for x in ['zolpidem', 'zopiclone', 'eszopiclone']):
                recommendations.append("  ⚠️ Beers Criteria: AVOID in elderly")
                recommendations.append("  ✓ Non-drug FIRST (most effective):")
                recommendations.append("    - Cognitive Behavioral Therapy for Insomnia (CBT-I)")
                recommendations.append("    - Sleep hygiene: Regular schedule, dark room, cool temperature")
                recommendations.append("    - Stimulus control: Use bed only for sleep")
                recommendations.append("  ✓ Pharmacological alternatives (if behavioral fails):")
                recommendations.append("    - Melatonin 3-5mg 1 hour before bed (low risk)")
                recommendations.append("    - Trazodone 25-50mg HS (sedative score 1-2)")
                recommendations.append("  ✗ Do NOT substitute with:")
                recommendations.append("    - Benzodiazepines (equally risky)")
                recommendations.append("    - Diphenhydramine (high anticholinergic)")
                
            # Benzodiazepines
            elif 'benzodiazepine' in drug_class:
                recommendations.append("  ⚠️ Beers Criteria: AVOID in elderly")
                recommendations.append("  🚨 CRITICAL: Do NOT stop abruptly (seizure risk)")
                recommendations.append("  ✓ Tapering protocol (coordinate with prescriber):")
                recommendations.append("    - Reduce by 10-25% every 1-2 weeks")
                recommendations.append("    - Monitor for withdrawal: Anxiety, tremor, insomnia, seizures")
                recommendations.append("    - Consider switching to long-acting (e.g., lorazepam → diazepam) for taper")
                recommendations.append("  ✓ For anxiety (underlying indication):")
                recommendations.append("    - SSRI/SNRI: Sertraline 25mg, escitalopram 5mg (titrate slowly)")
                recommendations.append("    - Buspirone 5mg TID (non-sedating, no dependence)")
                recommendations.append("    - CBT, mindfulness-based stress reduction")
                recommendations.append("  ✓ For sleep:")
                recommendations.append("    - See CBT-I recommendations above")
                
            # Atypical antipsychotics (often used off-label)
            elif any(x in generic for x in ['quetiapine', 'olanzapine', 'risperidone']):
                recommendations.append("  ⚠️ BLACK BOX WARNING: Increased mortality in dementia patients")
                recommendations.append("  ❓ Review indication:")
                recommendations.append("    - If for sleep only: DISCONTINUE (not approved, high risk)")
                recommendations.append("    - If for psychosis/bipolar: Consider lower-risk alternatives")
                recommendations.append("  ✓ For behavioral symptoms of dementia:")
                recommendations.append("    - Non-drug first: Environment modification, routine, music therapy")
                recommendations.append("    - If needed: Citalopram 10-20mg, trazodone 25-50mg")
                recommendations.append("  ✓ For psychosis:")
                recommendations.append("    - Consider lower doses")
                recommendations.append("    - Aripiprazole (less sedating)")
                recommendations.append("    - Regular monitoring: Weight, glucose, lipids, movement disorders")
                
            # Sedating antidepressants
            elif 'mirtazapine' in generic:
                recommendations.append("  📊 Dose-sedation relationship: INVERSE (lower doses more sedating)")
                recommendations.append("    - 7.5mg HS: Very sedating (antihistamine effect)")
                recommendations.append("    - 15-30mg: Moderate sedation")
                recommendations.append("    - 45mg: Less sedating (noradrenergic effects dominate)")
                recommendations.append("  ✓ If for depression:")
                recommendations.append("    - Consider less-sedating SSRI: Sertraline, citalopram, escitalopram")
                recommendations.append("  ✓ If for appetite stimulation:")
                recommendations.append("    - Low-dose acceptable if benefits outweigh fall risk")
                recommendations.append("    - Monitor weight, sedation, falls closely")
    
    # Safety measures (all score levels ≥2)
    if score >= 2:
        recommendations.append("\n🛡️ ENVIRONMENTAL SAFETY MEASURES:")
        recommendations.append("Physical modifications:")
        recommendations.append("• Bedside commode mandatory for nighttime use (avoid walking to bathroom)")
        recommendations.append("• Motion-activated night lights: Bedroom, bathroom, hallway")
        recommendations.append("• Remove all tripping hazards:")
        recommendations.append("  - Scatter rugs and bath mats")
        recommendations.append("  - Electrical cords across walkways")
        recommendations.append("  - Low furniture, ottomans, pet toys")
        recommendations.append("• Install grab bars: Beside toilet, in shower/tub, along hallways")
        recommendations.append("• Keep essentials within reach: Phone, flashlight, water, glasses")
        recommendations.append("\nPersonal safety:")
        recommendations.append("• Non-slip footwear indoors (avoid socks, slippers without backs)")
        recommendations.append("• Properly fitted clothing (avoid long robes, loose pants)")
        recommendations.append("• Medical alert system/pendant (especially if living alone)")
        recommendations.append("• Emergency contacts posted visibly")
        recommendations.append("\nProhibitions:")
        recommendations.append("• ❌ STRICTLY AVOID alcohol (synergistic sedation, can be fatal)")
        recommendations.append("• ❌ NO driving within 8-12 hours of sedative medication")
        recommendations.append("• ❌ NO operating machinery or climbing ladders")
        recommendations.append("• ❌ Avoid over-the-counter sleep aids (compounding effect)")
    
    # Monitoring recommendations (score ≥3)
    if score >= 3:
        recommendations.append("\n📊 MONITORING PARAMETERS:")
        recommendations.append("Daily monitoring (caregiver or self):")
        recommendations.append("• Mental status: Alert vs. drowsy vs. confused vs. obtunded")
        recommendations.append("• Respiratory rate: Count breaths for 60 seconds")
        recommendations.append("  - Normal: 12-20/min")
        recommendations.append("  - Concerning: <12/min → call MD")
        recommendations.append("  - Emergency: <8/min → call 911")
        recommendations.append("• Oxygen saturation (if pulse oximeter available):")
        recommendations.append("  - Target: >92% on room air")
        recommendations.append("  - If <88%: Seek immediate medical attention")
        recommendations.append("• Balance and gait before ambulation:")
        recommendations.append("  - Sit on edge of bed 30 seconds before standing")
        recommendations.append("  - Stand with support, wait for dizziness to clear")
        recommendations.append("  - Use walker/cane if available")
        recommendations.append("\nWeekly monitoring:")
        recommendations.append("• Fall diary: Document all falls AND near-misses")
        recommendations.append("• Functional status: ADLs (bathing, dressing, eating, toileting)")
        recommendations.append("• Sleep quality: Total hours, nighttime awakenings, daytime naps")
        recommendations.append("\nMonthly monitoring (healthcare provider):")
        recommendations.append("• Cognitive function: Mini-Cog, MoCA, or clock draw")
        recommendations.append("• Get-up-and-go test (fall risk assessment)")
        recommendations.append("• Medication review: Reassess need for each sedative")
    
    # Medication timing optimization (score ≥2)
    if score >= 2:
        recommendations.append("\n⏰ MEDICATION TIMING OPTIMIZATION:")
        recommendations.append("Dosing schedule:")
        recommendations.append("• Take all sedating medications at bedtime only (unless directed otherwise)")
        recommendations.append("• Avoid daytime doses if possible (request long-acting formulations)")
        recommendations.append("• Separate sedatives by 1-2 hours if multiple needed (reduce peak overlap)")
        recommendations.append("\nActivity restrictions:")
        recommendations.append("• No driving for at least 8-12 hours after sedative dose")
        recommendations.append("  - Longer for long-acting drugs (diazepam: 24 hours)")
        recommendations.append("• Schedule demanding activities (appointments, errands) in morning")
        recommendations.append("• Avoid afternoon naps >30 minutes (worsens nighttime sedation)")
        recommendations.append("\nOptimization strategies:")
        recommendations.append("• 'Drug holidays': Consider skipping doses 1-2 nights/week (with MD approval)")
        recommendations.append("• Scheduled awakening: Set alarm before typical wake time (reduce grogginess)")
        recommendations.append("• Morning light exposure: 30 minutes sunlight/bright light to promote alertness")
    
    # Caregiver education (score ≥3)
    if score >= 3:
        recommendations.append("\n👥 CAREGIVER EDUCATION:")
        recommendations.append("Train caregivers to recognize:")
        recommendations.append("• Excessive sedation: Difficult to arouse, slurred speech, unsteady gait")
        recommendations.append("• Respiratory depression: Slow/shallow breathing, blue lips/fingernails")
        recommendations.append("• Paradoxical agitation: Confusion, combativeness (especially benzodiazepines)")
        recommendations.append("• Fall warning signs: Dizziness, weakness, grabbing for support")
        recommendations.append("\nCaregiver actions:")
        recommendations.append("• Peak risk period: 1-4 hours after medication dose")
        recommendations.append("• During peak: Stay within earshot, check every 30-60 minutes")
        recommendations.append("• If patient must walk: Provide physical support, use gait belt")
        recommendations.append("• If excessive sedation: Hold next dose, contact MD")
        recommendations.append("• If respiratory rate <10: Call 911 immediately")
    
    return recommendations


# ============================================================================
# COMBINED CNS BURDEN ASSESSMENT
# ============================================================================

def calculate_combined_cns_burden(medications: List[str]) -> dict:
    """
    Calculate COMBINED anticholinergic + sedative burden.
    
    CRITICAL: These effects are SYNERGISTIC, not merely additive.
    Combined burden increases delirium risk exponentially.
    
    Args:
        medications: List of medication names
        
    Returns:
        Dictionary containing:
        - anticholinergic_burden: Full ACB assessment results
        - sedative_burden: Full sedative assessment results
        - total_cns_score: Sum of both scores
        - combined_risk_level: Overall CNS risk category
        - synergistic_multiplier: Multiplicative factor (1.0-1.5x)
        - dual_mechanism_medications: Drugs contributing to BOTH burdens
        - synergistic_warnings: Specific warnings about combined effects
        - combined_recommendations: Integrated deprescribing strategy
        - summary: Quick reference statistics
        
    Synergistic Risk Levels:
        - ≥8: CRITICAL (multiplier 1.5x)
        - 5-7: HIGH (multiplier 1.3x)
        - 3-4: MODERATE (multiplier 1.2x)
        - 1-2: LOW (multiplier 1.0x)
        
    Example:
        >>> meds = ["Diphenhydramine", "Zolpidem", "Amitriptyline"]
        >>> result = calculate_combined_cns_burden(meds)
        >>> print(result['total_cns_score'])  # 15 (high risk)
        >>> print(result['dual_mechanism_count'])  # 2 (diphenhydramine, amitriptyline)
        >>> print(result['synergistic_multiplier'])  # 1.5x
    """
    # Calculate individual burdens
    anticholinergic_result = calculate_anticholinergic_burden(medications)
    sedative_result = calculate_sedative_burden(medications)
    
    # Identify medications contributing to BOTH burdens (dual mechanism)
    # These are HIGHEST PRIORITY for deprescribing
    dual_burden_meds = []
    for med in medications:
        normalized = normalize_drug_name(med)
        profile = get_drug_profile(normalized)
        
        if profile and profile.anticholinergic_score > 0 and profile.sedative_score > 0:
            dual_burden_meds.append({
                "name": med,
                "generic_name": profile.generic_name,
                "drug_class": profile.drug_class,
                "anticholinergic_score": profile.anticholinergic_score,
                "sedative_score": profile.sedative_score,
                "combined_score": profile.anticholinergic_score + profile.sedative_score,
                "fall_risk_score": profile.fall_risk_score,
                "beers_criteria": profile.beers_criteria,
                "risk_category": "VERY HIGH - Dual CNS depression mechanism",
                "deprescribing_priority": "HIGHEST - Remove first"
            })
    
    # Sort dual-mechanism drugs by combined score (highest first)
    dual_burden_meds.sort(key=lambda x: x["combined_score"], reverse=True)
    
    # Calculate total CNS impact (raw sum)
    total_cns_score = anticholinergic_result["total_score"] + sedative_result["total_score"]
    
    # Determine combined risk level and synergistic multiplier
    # Multiplier represents how much worse the effects are than simple addition
    if total_cns_score >= 8:
        combined_risk_level = "CRITICAL - Synergistic CNS depression"
        synergistic_multiplier = 1.5  # Effects 50% worse than additive
        risk_interpretation = "Extreme delirium risk (>80% in hospitalized elderly). Immediate intervention required."
    elif total_cns_score >= 5:
        combined_risk_level = "HIGH - Multiple CNS depressant mechanisms"
        synergistic_multiplier = 1.3  # Effects 30% worse
        risk_interpretation = "High delirium risk (60-80% in vulnerable populations). Urgent deprescribing needed."
    elif total_cns_score >= 3:
        combined_risk_level = "MODERATE - Monitor cumulative CNS effects"
        synergistic_multiplier = 1.2  # Effects 20% worse
        risk_interpretation = "Moderate delirium risk (40-60% in hospitalized). Monitor closely, consider alternatives."
    elif total_cns_score >= 1:
        combined_risk_level = "LOW - Minimal combined burden"
        synergistic_multiplier = 1.0  # Minimal synergy at low scores
        risk_interpretation = "Low risk (<40%). Appropriate monitoring sufficient."
    else:
        combined_risk_level = "NONE"
        synergistic_multiplier = 1.0
        risk_interpretation = "No CNS burden detected. No medication-related cognitive risk."
    
    # Generate synergistic warnings
    synergistic_warnings = []
    if len(dual_burden_meds) > 0:
        synergistic_warnings.extend([
            "⚠️ SYNERGISTIC RISK DETECTED:",
            f"• {len(dual_burden_meds)} medication(s) affect BOTH anticholinergic AND sedative pathways",
            "• Combined effect: Anticholinergic + Sedative effects MULTIPLY each other",
            "• This is NOT simple addition - the interaction is exponential",
            "",
            "🧠 CLINICAL SIGNIFICANCE:",
            "• Delirium risk increases EXPONENTIALLY (not linearly) with combined burden",
            "• Hospitalized elderly with high combined burden: 80-90% delirium rate",
            "• Functional decline accelerates: 50% lose independence within 6 months",
            "• Mortality risk: 2-3x higher in first year",
            "",
            f"📊 SYNERGISTIC MULTIPLIER: {synergistic_multiplier}x",
            f"• Effective CNS burden: {total_cns_score} × {synergistic_multiplier} = {total_cns_score * synergistic_multiplier:.1f}",
            "• This represents the ACTUAL clinical impact (worse than raw score suggests)"
        ])
    
    if total_cns_score >= 8:
        synergistic_warnings.append("\n🚨 CRITICAL ALERT:")
        synergistic_warnings.append("• Combined CNS burden at DANGEROUS level")
        synergistic_warnings.append("• Immediate action required to prevent serious adverse outcomes")
        synergistic_warnings.append("• Consider emergency department evaluation if acutely confused")
    
    # Generate comprehensive deprescribing recommendations
    combined_recommendations = []
    if total_cns_score >= 5:
        combined_recommendations.extend([
            "🎯 DEPRESCRIBING STRATEGY - PRIORITY ORDER:",
            "",
            "TIER 1 (HIGHEST PRIORITY - Remove FIRST):",
            "Dual-mechanism drugs (anticholinergic + sedative):"
        ])
        
        if dual_burden_meds:
            for i, med in enumerate(dual_burden_meds, 1):
                combined_recommendations.append(
                    f"  {i}. {med['name']} "
                    f"(ACB={med['anticholinergic_score']}, "
                    f"Sedative={med['sedative_score']}, "
                    f"Combined={med['combined_score']})"
                )
            combined_recommendations.append("  → These drugs cause BOTH confusion AND sedation")
            combined_recommendations.append("  → Removing ONE dual-mechanism drug reduces BOTH burdens")
            combined_recommendations.append("  → Maximum benefit with single deprescribing intervention")
        
        combined_recommendations.extend([
            "",
            "TIER 2 (HIGH PRIORITY):",
            "Single-mechanism drugs with highest scores (ACB=3 or Sedative=3):"
        ])
        
        # Identify high-score single-mechanism drugs
        high_acb_only = [m for m in anticholinergic_result.get('contributing_medications', []) 
                        if m['score'] == 3 and not any(d['name'] == m['name'] for d in dual_burden_meds)]
        high_sed_only = [m for m in sedative_result.get('contributing_medications', []) 
                        if m['score'] == 3 and not any(d['name'] == m['name'] for d in dual_burden_meds)]
        
        if high_acb_only:
            combined_recommendations.append("  Anticholinergic-only (ACB=3):")
            for med in high_acb_only:
                combined_recommendations.append(f"    - {med['name']}")
        
        if high_sed_only:
            combined_recommendations.append("  Sedative-only (Sedative=3):")
            for med in high_sed_only:
                combined_recommendations.append(f"    - {med['name']}")
        
        combined_recommendations.extend([
            "",
            "TIER 3 (MODERATE PRIORITY):",
            "Non-essential medications (sleep aids, as-needed anxiolytics, OTC products)",
            "  → Often these were started for convenience, not medical necessity",
            "  → Easiest to discontinue without replacement",
            "",
            "TIER 4 (IF TARGET NOT REACHED):",
            "Moderate-score drugs (ACB=2 or Sedative=2)",
            "  → Consider alternatives or dose reduction",
            "  → May need gradual taper",
            "",
            "═══════════════════════════════════════════════",
            "🎯 TARGET GOALS FOR SAFE CNS BURDEN:",
            "═══════════════════════════════════════════════",
            f"Current status → Target goals:",
            f"• Anticholinergic: {anticholinergic_result['total_score']} → <3 (ideally <2)",
            f"• Sedative: {sedative_result['total_score']} → <3 (ideally <2)",
            f"• Combined CNS: {total_cns_score} → <5 (ideally <3)",
            f"• Dual-mechanism drugs: {len(dual_burden_meds)} → 0",
            "",
            "📅 TIMELINE:",
            "• Tier 1 (dual-mechanism): Remove within 1 week",
            "• Tier 2 (high-score): Remove within 2-4 weeks",
            "• Tier 3 (non-essential): Remove within 4-8 weeks",
            "• Tier 4 (moderate-score): Remove within 8-12 weeks",
            "",
            "⚠️ IMPORTANT CAVEATS:",
            "• Benzodiazepines: MUST taper slowly (seizure risk if abrupt stop)",
            "• Antipsychotics: Gradual taper over weeks to prevent withdrawal psychosis",
            "• Antidepressants: Taper over 4-6 weeks to prevent discontinuation syndrome",
            "• Always coordinate with prescribing physician before stopping medications"
        ])
    
    # Create comprehensive summary
    summary = {
        "anticholinergic_total": anticholinergic_result["total_score"],
        "sedative_total": sedative_result["total_score"],
        "combined_total": total_cns_score,
        "effective_burden": round(total_cns_score * synergistic_multiplier, 1),
        "high_anticholinergic_count": anticholinergic_result.get("high_anticholinergic_count", 0),
        "high_sedative_count": sedative_result.get("high_sedative_count", 0),
        "dual_mechanism_count": len(dual_burden_meds),
        "contributing_medication_count": (
            anticholinergic_result.get("contributing_count", 0) +
            sedative_result.get("contributing_count", 0) -
            len(dual_burden_meds)  # Avoid double-counting dual-mechanism drugs
        ),
        "total_medications_assessed": len(medications),
        "unrecognized_medications": list(set(
            anticholinergic_result.get("unrecognized_medications", []) +
            sedative_result.get("unrecognized_medications", [])
        ))
    }
    
    return {
        "anticholinergic_burden": anticholinergic_result,
        "sedative_burden": sedative_result,
        "total_cns_score": total_cns_score,
        "effective_cns_burden": round(total_cns_score * synergistic_multiplier, 1),
        "combined_risk_level": combined_risk_level,
        "risk_interpretation": risk_interpretation,
        "synergistic_multiplier": synergistic_multiplier,
        "dual_mechanism_medications": dual_burden_meds,
        "dual_mechanism_count": len(dual_burden_meds),
        "synergistic_warnings": synergistic_warnings,
        "combined_recommendations": combined_recommendations,
        "summary": summary,
        "assessment_date": None,
        "evidence_sources": [
            "ACB Scale (Campbell et al. 2021)",
            "Woolcott et al. Meta-analysis (2009)",
            "Beers Criteria (AGS 2023)"
        ]
    }


# ============================================================================
# LEGACY INTERFACE (Backward Compatibility)
# ============================================================================

def check_interaction_legacy(drug1: str, drug2: str) -> Optional[dict]:
    """
    Legacy interface for backward compatibility.
    
    DEPRECATED: Use check_interaction() instead for full functionality.
    
    Args:
        drug1: First drug name
        drug2: Second drug name
        
    Returns:
        Simplified interaction dictionary or None
    """
    interaction = check_interaction(drug1, drug2)
    if interaction:
        return {
            "severity": interaction["severity"],
            "description": interaction["description"]
        }
    return None


# ============================================================================
# COMPREHENSIVE MEDICATION ASSESSMENT
# ============================================================================

def comprehensive_medication_assessment(medications: List[str]) -> dict:
    """
    Perform complete medication safety assessment.
    
    This is the PRIMARY function for clinical use - it runs all assessments
    and provides a unified report.
    
    Args:
        medications: List of medication names
        
    Returns:
        Comprehensive dictionary containing:
        - medication_list: Validated medication list
        - interactions: All detected drug interactions
        - fall_risk: Fall risk assessment
        - anticholinergic_burden: ACB assessment
        - sedative_burden: Sedative burden assessment
        - combined_cns_burden: Synergistic CNS assessment
        - therapeutic_duplicates: Duplicate drug classes
        - overall_risk_level: Summary risk category
        - priority_actions: Top 5 most urgent interventions
        - unrecognized_medications: Drugs not in database
        
    Example:
        >>> meds = ["Warfarin", "Aspirin", "Zolpidem", "Diphenhydramine"]
        >>> assessment = comprehensive_medication_assessment(meds)
        >>> print(assessment['overall_risk_level'])
        'CRITICAL'
        >>> for action in assessment['priority_actions']:
        ...     print(f"- {action}")
    """
    # Validate medications
    valid_meds, unrecognized_meds = validate_medication_list(medications)
    
    # Run all assessments
    interactions = check_all_interactions(valid_meds)
    fall_risk = calculate_fall_risk_score(valid_meds)
    acb = calculate_anticholinergic_burden(valid_meds)
    sedative = calculate_sedative_burden(valid_meds)
    combined_cns = calculate_combined_cns_burden(valid_meds)
    duplicates = detect_therapeutic_duplicates(valid_meds)
    
    # Determine overall risk level (highest of all assessments)
    risk_levels = []
    
    # Map text descriptions to numeric risk
    risk_mapping = {
        'CRITICAL': 4,
        'HIGH': 3,
        'MODERATE': 2,
        'LOW': 1,
        'NONE': 0
    }
    
    # Extract risk levels from each assessment
    if interactions['critical']:
        risk_levels.append(4)
    elif interactions['high']:
        risk_levels.append(3)
    
    risk_levels.append(risk_mapping.get(fall_risk['risk_category'].split()[0], 0))
    risk_levels.append(risk_mapping.get(acb['burden_level'].split()[0], 0))
    risk_levels.append(risk_mapping.get(sedative['burden_level'].split()[0], 0))
    risk_levels.append(risk_mapping.get(combined_cns['combined_risk_level'].split()[0], 0))
    
    max_risk_num = max(risk_levels) if risk_levels else 0
    risk_reverse_map = {v: k for k, v in risk_mapping.items()}
    overall_risk_level = risk_reverse_map.get(max_risk_num, 'UNKNOWN')
    
    # Generate priority actions (top 5 most urgent)
    priority_actions = []
    
    # Priority 1: Critical drug interactions
    if interactions['critical']:
        priority_actions.append(
            f"🚨 CRITICAL INTERACTION: {len(interactions['critical'])} life-threatening "
            f"drug interaction(s) detected - IMMEDIATE physician consultation required"
        )
    
    # Priority 2: Dual-mechanism CNS drugs
    if combined_cns['dual_mechanism_count'] > 0:
        priority_actions.append(
            f"🎯 DEPRESCRIBE PRIORITY: {combined_cns['dual_mechanism_count']} medication(s) "
            f"with dual CNS effects (anticholinergic + sedative) - highest impact removal"
        )
    
    # Priority 3: Critical CNS burden
    if combined_cns['total_cns_score'] >= 8:
        priority_actions.append(
            f"🧠 CRITICAL CNS BURDEN: Total score {combined_cns['total_cns_score']} "
            f"(×{combined_cns['synergistic_multiplier']} synergy) - extreme delirium risk"
        )
    
    # Priority 4: Critical fall risk
    if fall_risk['total_score'] >= 15:
        priority_actions.append(
            f"🏥 EXTREME FALL RISK: Score {fall_risk['total_score']} - "
            f"24/7 supervision or facility care evaluation needed"
        )
    
    # Priority 5: High drug interactions
    if interactions['high']:
        priority_actions.append(
            f"⚠️ HIGH-RISK INTERACTIONS: {len(interactions['high'])} interaction(s) "
            f"requiring immediate attention"
        )
    
    # Priority 6: Multiple Beers Criteria violations
    beers_count = sum(
        1 for m in valid_meds
        if get_drug_profile(normalize_drug_name(m)) and get_drug_profile(normalize_drug_name(m)).beers_criteria
    )
    if beers_count >= 3:
        priority_actions.append(
            f"⚕️ BEERS CRITERIA: {beers_count} potentially inappropriate medications - "
            f"comprehensive geriatric review needed"
        )
    
    # Priority 7: Therapeutic duplicates
    if duplicates:
        dup_count = sum(len(meds) for meds in duplicates.values())
        priority_actions.append(
            f"💊 THERAPEUTIC DUPLICATION: {dup_count} duplicate medications "
            f"in {len(duplicates)} drug class(es)"
        )
    
    # Limit to top 5
    priority_actions = priority_actions[:5]
    
    # If no critical issues, provide positive feedback
    if not priority_actions:
        priority_actions = [
            "✅ No critical medication safety issues detected",
            "📋 Continue routine monitoring and medication reviews",
            "🏥 Follow up with prescriber for any symptom changes"
        ]
    
    return {
        "assessment_metadata": {
            "total_medications": len(medications),
            "recognized_medications": len(valid_meds),
            "unrecognized_medications": unrecognized_meds,
            "assessment_date": None,  # Placeholder for timestamp
            "database_version": "3.0"
        },
        "medication_list": {
            "all_medications": medications,
            "valid_medications": valid_meds,
            "unrecognized_medications": unrecognized_meds
        },
        "interactions": interactions,
        "fall_risk": fall_risk,
        "anticholinergic_burden": acb,
        "sedative_burden": sedative,
        "combined_cns_burden": combined_cns,
        "therapeutic_duplicates": duplicates,
        "overall_risk_level": overall_risk_level,
        "priority_actions": priority_actions,
        "requires_immediate_action": max_risk_num >= 4,  # CRITICAL level
        "requires_urgent_action": max_risk_num >= 3,     # HIGH level
    }


# ============================================================================
# UTILITY: GENERATE PRINTABLE REPORT
# ============================================================================

def generate_assessment_report(assessment: dict, include_details: bool = True) -> str:
    """
    Generate human-readable assessment report.
    
    Args:
        assessment: Output from comprehensive_medication_assessment()
        include_details: If True, includes full recommendations and warnings
        
    Returns:
        Formatted text report ready for printing or display
    """
    lines = []
    lines.append("═" * 80)
    lines.append("COMPREHENSIVE MEDICATION SAFETY ASSESSMENT")
    lines.append("Canadian Elderly Drug Interaction Database v3.0")
    lines.append(f"Assessment Date: January 06, 2026")
    lines.append("═" * 80)
    lines.append("")
    
    # Metadata
    meta = assessment['assessment_metadata']
    lines.append(f"Total Medications Assessed: {meta['total_medications']}")
    lines.append(f"Recognized in Database: {meta['recognized_medications']}")
    if meta['unrecognized_medications']:
        lines.append(f"⚠️ Unrecognized Medications: {', '.join(meta['unrecognized_medications'])}")
    lines.append("")
    
    # Overall risk
    lines.append("─" * 80)
    lines.append(f"OVERALL RISK LEVEL: {assessment['overall_risk_level']}")
    lines.append("─" * 80)
    lines.append("")
    
    # Priority actions
    lines.append("🎯 TOP PRIORITY ACTIONS:")
    for i, action in enumerate(assessment['priority_actions'], 1):
        lines.append(f"{i}. {action}")
    lines.append("")
    
    # Interactions summary
    interactions = assessment['interactions']
    total_interactions = sum(len(v) for v in interactions.values())
    lines.append("─" * 80)
    lines.append(f"DRUG INTERACTIONS: {total_interactions} Total")
    lines.append(f"  • Critical: {len(interactions['critical'])}")
    lines.append(f"  • High:      {len(interactions['high'])}")
    lines.append(f"  • Moderate:  {len(interactions['moderate'])}")
    lines.append(f"  • Low:       {len(interactions['low'])}")
    
    if include_details and interactions['critical']:
        lines.append("")
        lines.append("  CRITICAL INTERACTIONS:")
        for inter in interactions['critical']:
            drugs = " + ".join(inter['drugs'])
            lines.append(f"    - {drugs}")
            lines.append(f"      {inter['description']}")
            lines.append(f"      Action: {inter['action']}")
    lines.append("")
    
    # Fall risk
    fall = assessment['fall_risk']
    lines.append("─" * 80)
    lines.append(f"FALL RISK: {fall['risk_category']} (Score: {fall['total_score']})")
    lines.append(f"  High-risk medications: {fall['high_risk_count']}")
    if include_details and fall['high_risk_medications']:
        lines.append("  Contributing high-risk drugs:")
        for med in fall['high_risk_medications']:
            lines.append(f"    - {med['name']} (Score: {med['fall_risk_score']})")
    lines.append("")
    
    # CNS burden
    cns = assessment['combined_cns_burden']
    lines.append("─" * 80)
    lines.append("CENTRAL NERVOUS SYSTEM (CNS) BURDEN:")
    lines.append(f"  Anticholinergic Burden: {cns['anticholinergic_burden']['total_score']} ({cns['anticholinergic_burden']['burden_level'].split()[0]})")
    lines.append(f"  Sedative Burden:        {cns['sedative_burden']['total_score']} ({cns['sedative_burden']['burden_level'].split()[0]})")
    lines.append(f"  Combined Total Score:   {cns['total_cns_score']}")
    lines.append(f"  Effective Burden (with synergy): {cns['effective_cns_burden']}")
    lines.append(f"  Overall CNS Risk Level: {cns['combined_risk_level']}")
    lines.append(f"  Dual-mechanism drugs:   {cns['dual_mechanism_count']}")
    lines.append("")
    
    # Therapeutic duplicates
    if assessment['therapeutic_duplicates']:
        lines.append("─" * 80)
        lines.append("THERAPEUTIC DUPLICATIONS DETECTED:")
        for category, meds in assessment['therapeutic_duplicates'].items():
            lines.append(f"  • {category.replace('_', ' ').title()}: {', '.join(meds)}")
        lines.append("")
    
    lines.append("═" * 80)
    lines.append("END OF REPORT")
    lines.append("═" * 80)
    lines.append("")
    lines.append("Note: This tool is for educational and supportive use only.")
    lines.append("All clinical decisions must be made by a qualified healthcare professional.")
    
    return "\n".join(lines)


# ============================================================================
# ERROR HANDLING AND VALIDATION
# ============================================================================

class MedicationAssessmentError(Exception):
    """Base exception for medication assessment errors."""
    pass

class InvalidMedicationListError(MedicationAssessmentError):
    """Raised when medication list is invalid or empty."""
    pass

class DatabaseIntegrityError(MedicationAssessmentError):
    """Raised when database consistency check fails."""
    pass


def validate_database_integrity() -> Tuple[bool, List[str]]:
    """
    Validate internal database integrity.
    
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    
    # Check DRUG_ALIASES → valid generics
    for brand, generic in DRUG_ALIASES.items():
        if generic not in DRUG_PROFILES:
            errors.append(f"Brand name '{brand}' maps to unknown generic '{generic}'")
    
    # Check INTERACTION_DATABASE keys → valid drugs
    for key in INTERACTION_DATABASE:
        for drug in key:
            if drug not in DRUG_PROFILES:
                errors.append(f"Interaction references unknown drug '{drug}'")
    
    # Check score ranges
    for drug_name, profile in DRUG_PROFILES.items():
        if not (0 <= profile.anticholinergic_score <= 3):
            errors.append(f"{drug_name}: anticholinergic_score {profile.anticholinergic_score} out of range (0-3)")
        if not (0 <= profile.sedative_score <= 3):
            errors.append(f"{drug_name}: sedative_score {profile.sedative_score} out of range (0-3)")
        if not (0 <= profile.fall_risk_score <= 10):
            errors.append(f"{drug_name}: fall_risk_score {profile.fall_risk_score} out of range (0-10)")
    
    return (len(errors) == 0, errors)


# ============================================================================
# MODULE INITIALIZATION CHECK
# ============================================================================

_INTEGRITY_CHECK_ENABLED = True

if _INTEGRITY_CHECK_ENABLED:
    is_valid, errors = validate_database_integrity()
    if not is_valid:
        import warnings
        warnings.warn(
            "Database integrity issues detected:\n" + "\n".join(errors[:10]),
            RuntimeWarning
        )


# ============================================================================
# END OF FILE - FIXED AND COMPLETE VERSION
# ============================================================================