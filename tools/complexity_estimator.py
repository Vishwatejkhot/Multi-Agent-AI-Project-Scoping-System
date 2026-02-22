def estimate_complexity(feature_count, ai_features, integrations):

    score = 0

  
    score += feature_count * 2

    
    if ai_features:
        score += 5

    score += integrations * 2

    if score < 15:
        level = "Low"
    elif score < 30:
        level = "Medium"
    else:
        level = "High"

    return {
        "score": round(score, 1),
        "level": level
    }