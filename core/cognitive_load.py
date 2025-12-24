# core/cognitive_load.py

def calculate_mcls(med_list):
    """
    Calculate the Medication Cognitive Load Score (MCLS).

    Args:
        med_list: list of dicts, each dict with:
            - name: medication name (str)
            - doses_per_day: int
            - sedative: bool
            - anticholinergic: bool

    Returns:
        mcls_score: numeric total
        burden_level: 'LOW', 'MODERATE', 'HIGH'
        explanation: plain-language explanation
    """

    mcls_score = 0
    explanation_parts = []

    num_meds = len(med_list)
    mcls_score += num_meds * 2  # Polypharmacy load
    if num_meds > 1:
        explanation_parts.append(f"{num_meds} medications")

    # Track sedatives and anticholinergics
    sedatives = 0
    antichols = 0
    total_doses = 0

    for med in med_list:
        doses = med.get("doses_per_day", 1)
        total_doses += doses
        mcls_score += doses  # Dosing complexity

        if med.get("sedative", False):
            mcls_score += 7
            sedatives += 1
        if med.get("anticholinergic", False):
            mcls_score += 5
            antichols += 1

    if total_doses > num_meds:
        explanation_parts.append(f"total of {total_doses} daily doses")

    if sedatives > 0:
        explanation_parts.append(f"{sedatives} sedative(s)")
    if antichols > 0:
        explanation_parts.append(f"{antichols} anticholinergic(s)")

    # Synergy penalty
    if sedatives >= 2:
        mcls_score += 10
        explanation_parts.append("sedative synergy penalty applied")

    # Determine burden level
    if mcls_score <= 7:
        burden_level = "LOW"
    elif 8 <= mcls_score <= 15:
        burden_level = "MODERATE"
    else:
        burden_level = "HIGH"

    explanation = "Cognitive burden due to " + ", ".join(explanation_parts) if explanation_parts else "Low cognitive burden"

    return mcls_score, burden_level, explanation
