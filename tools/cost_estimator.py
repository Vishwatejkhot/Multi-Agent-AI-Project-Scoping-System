def estimate_cost(complexity, country="US"):

    base_cost = {
        "Low": (15000, 40000),
        "Medium": (50000, 120000),
        "High": (120000, 300000)
    }

    COUNTRY_MULTIPLIERS = {
        "US": 1.0,
        "UK": 0.9,
        "Germany": 0.95,
        "India": 0.4,
        "Canada": 0.85,
        "Australia": 0.9,
        "UAE": 0.8
    }

    low, high = base_cost.get(complexity, (15000, 40000))
    multiplier = COUNTRY_MULTIPLIERS.get(country, 1.0)

    return {
        "base_currency": "USD",
        "low_usd": int(low * multiplier),
        "high_usd": int(high * multiplier)
    }