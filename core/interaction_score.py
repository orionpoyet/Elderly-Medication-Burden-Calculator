# core/interaction_score.py

def calculate_dir_score_from_list(interactions):
    """
    Calculate DIRS from a list of tuples:
    [(drugA, drugB, severity), ...]
    
    Returns:
        score (int): weighted score based on severity
        risk_level (str): 'Low', 'Moderate', 'High'
    """
    if not interactions:
        return 0, "Low"

    severity_weights = {
        "high": 3,
        "moderate": 2,
        "low": 1,
        "unknown": 1
    }

    score = 0
    for a, b, severity in interactions:
        score += severity_weights.get(severity.lower(), 1)

    # Define risk levels
    if score >= 10:
        risk_level = "High"
    elif score >= 4:
        risk_level = "Moderate"
    else:
        risk_level = "Low"

    return score, risk_level
