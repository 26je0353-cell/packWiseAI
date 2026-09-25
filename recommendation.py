"""
PackWise AI - Recommendation Engine
====================================
This is a transparent, rule-based weighted-scoring model — NOT a black-box
machine-learning classifier. Every score can be fully decomposed back into
its contributing factors, which is what the `reasons` list in each result
shows. This keeps the logic explainable and easy for students to present
to judges.

SCORING MODEL
-------------
For each material, we compute a 0-100 compatibility_score as a weighted sum
of "need vs. supply" matches:

  need vs supply factors (each 0-1):
    oxygen_match     = (oxygen_sensitivity / 5)   * (material.oxygen_barrier / 5)
    moisture_match    = (moisture_sensitivity / 5) * (material.moisture_barrier / 5)
    light_match        = (light_sensitivity / 5)    * (material.light_barrier / 5)
    grease_match       = (fat_content / 5)          * (material.grease_resistance / 5)

  preference factors (each 0-1):
    cost_match         = (cost_priority / 5) * ((6 - material.cost_level) / 5)
    sustainability_match = (sustainability_priority / 5) * (material.sustainability_level / 5)

  environmental stress adjustment (small, explainable bonus/penalty):
    If storage humidity/temperature are high, moisture & oxygen match are
    slightly boosted in importance (their weights increase), since a good
    barrier matters even more under harsh storage conditions.

Each factor is multiplied by a fixed importance weight and summed, then
normalised to a 0-100 scale. Weights are declared as constants below so
they are easy to explain and tune.
"""
from typing import List, Dict, Any

# Fixed, explainable importance weights. Sensitivity/barrier factors carry
# more weight than soft preferences (cost/sustainability) because they
# directly determine whether the food survives its shelf life.
WEIGHTS = {
    "oxygen": 1.2,
    "moisture": 1.3,
    "light": 0.9,
    "grease": 1.0,
    "cost": 0.7,
    "sustainability": 0.7,
    "form": 0.6,
}

# Preferred packaging "form factor" per food category — a mild, explainable
# nudge so e.g. a rigid glass jar isn't ranked above a flexible pouch for a
# bag-of-chips product, without hard-excluding any material.
FOOD_CATEGORY_PREFERRED_FORMS = {
    "Snacks & Confectionery": ["flexible_film"],
    "Beverages": ["flexible_film", "rigid_container"],
    "Dairy & Meats": ["rigid_container", "flexible_film"],
    "Fresh Produce": ["flexible_film"],
    "Bakery & Cereals": ["flexible_film", "rigid_container"],
    "Sauces & Condiments": ["rigid_container"],
}


def _stress_multiplier(storage_temp_c: float, relative_humidity: float) -> Dict[str, float]:
    """Return small multipliers (>=1.0) that increase the importance of
    moisture/oxygen barrier when storage conditions are harsh. Kept simple
    and bounded so the effect is explainable, not a hidden black box."""
    moisture_mult = 1.0
    oxygen_mult = 1.0
    if relative_humidity >= 75:
        moisture_mult += 0.25
    elif relative_humidity >= 60:
        moisture_mult += 0.10

    if storage_temp_c >= 32:
        oxygen_mult += 0.15
        moisture_mult += 0.10
    elif storage_temp_c >= 28:
        oxygen_mult += 0.08

    return {"moisture": moisture_mult, "oxygen": oxygen_mult}


def score_material(food_params: Dict[str, Any], material: Dict[str, Any]) -> Dict[str, Any]:
    moisture_sensitivity = food_params["moisture_sensitivity"]
    oxygen_sensitivity = food_params["oxygen_sensitivity"]
    light_sensitivity = food_params["light_sensitivity"]
    fat_content = food_params["fat_content"]
    cost_priority = food_params["cost_priority"]
    sustainability_priority = food_params["sustainability_priority"]
    storage_temp_c = food_params["storage_temperature_c"]
    relative_humidity = food_params["relative_humidity"]

    stress = _stress_multiplier(storage_temp_c, relative_humidity)

    oxygen_match = (oxygen_sensitivity / 5) * (material["oxygen_barrier"] / 5)
    moisture_match = (moisture_sensitivity / 5) * (material["moisture_barrier"] / 5)
    light_match = (light_sensitivity / 5) * (material["light_barrier"] / 5)
    grease_match = (fat_content / 5) * (material["grease_resistance"] / 5)
    cost_match = (cost_priority / 5) * ((6 - material["cost_level"]) / 5)
    sustainability_match = (sustainability_priority / 5) * (material["sustainability_level"] / 5)

    preferred_forms = FOOD_CATEGORY_PREFERRED_FORMS.get(food_params.get("food_category", ""), None)
    if preferred_forms is None:
        form_match = 0.8  # unknown category — neutral, slightly-below-full credit
    elif material.get("material_form") in preferred_forms:
        form_match = 1.0
    else:
        form_match = 0.4

    weighted_sum = (
        oxygen_match * WEIGHTS["oxygen"] * stress["oxygen"]
        + moisture_match * WEIGHTS["moisture"] * stress["moisture"]
        + light_match * WEIGHTS["light"]
        + grease_match * WEIGHTS["grease"]
        + cost_match * WEIGHTS["cost"]
        + sustainability_match * WEIGHTS["sustainability"]
        + form_match * WEIGHTS["form"]
    )

    max_possible = (
        WEIGHTS["oxygen"] * stress["oxygen"]
        + WEIGHTS["moisture"] * stress["moisture"]
        + WEIGHTS["light"]
        + WEIGHTS["grease"]
        + WEIGHTS["cost"]
        + WEIGHTS["sustainability"]
        + WEIGHTS["form"]
    )

    compatibility_score = round((weighted_sum / max_possible) * 100, 1)

    # Build human-readable, transparent reasons for this score.
    reasons = []
    factor_checks = [
        ("moisture", moisture_sensitivity, material["moisture_barrier"], "moisture barrier"),
        ("oxygen", oxygen_sensitivity, material["oxygen_barrier"], "oxygen barrier"),
        ("light", light_sensitivity, material["light_barrier"], "light barrier"),
        ("grease/fat", fat_content, material["grease_resistance"], "grease resistance"),
    ]
    for label, need, supply, prop_name in factor_checks:
        if need >= 4 and supply >= 4:
            reasons.append(
                f"High {label} sensitivity ({need}/5) is well matched by this material's strong {prop_name} ({supply}/5)."
            )
        elif need >= 4 and supply <= 2:
            reasons.append(
                f"Caution: {label} sensitivity is high ({need}/5) but this material's {prop_name} is only {supply}/5."
            )

    if cost_priority >= 4:
        if material["cost_level"] <= 2:
            reasons.append(f"Matches your cost priority — this is a lower-cost material ({material['cost_level']}/5 cost tier).")
        elif material["cost_level"] >= 4:
            reasons.append(f"Note: cost priority is high but this material is in a higher cost tier ({material['cost_level']}/5).")

    if sustainability_priority >= 4:
        if material["sustainability_level"] >= 4:
            reasons.append(f"Matches your sustainability priority — rated {material['sustainability_level']}/5 for sustainability.")
        elif material["sustainability_level"] <= 2:
            reasons.append(f"Note: sustainability priority is high but this material scores only {material['sustainability_level']}/5.")

    if form_match == 1.0 and preferred_forms is not None:
        form_label = "flexible pouch/film" if material.get("material_form") == "flexible_film" else "rigid container"
        reasons.append(f"Packaging form ({form_label}) is a typical fit for the '{food_params.get('food_category')}' category.")
    elif form_match == 0.4:
        form_label = "flexible pouch/film" if material.get("material_form") == "flexible_film" else "rigid container"
        reasons.append(f"Less typical form factor: this is a {form_label}, which is less common for '{food_params.get('food_category')}' products.")

    if not reasons:
        reasons.append("Balanced, moderate fit across barrier, cost and sustainability requirements.")

    return {
        "material_id": material["id"],
        "material_name": material["name"],
        "short_code": material["short_code"],
        "material_form": material.get("material_form", "flexible_film"),
        "compatibility_score": compatibility_score,
        "oxygen_barrier": material["oxygen_barrier"],
        "moisture_barrier": material["moisture_barrier"],
        "light_barrier": material["light_barrier"],
        "grease_resistance": material["grease_resistance"],
        "mechanical_strength": material["mechanical_strength"],
        "heat_resistance": material["heat_resistance"],
        "cost_level": material["cost_level"],
        "sustainability_level": material["sustainability_level"],
        "recyclable": bool(material["recyclable"]),
        "compostable": bool(material["compostable"]),
        "data_status": material["data_status"],
        "example_applications": material["example_applications"],
        "advantages": material["advantages"],
        "limitations": material["limitations"],
        "reasons": reasons,
    }


def recommend_top_materials(food_params: Dict[str, Any], all_materials: List[Dict[str, Any]], top_n: int = 3) -> List[Dict[str, Any]]:
    """Score every material and return the top_n ranked results."""
    scored = [score_material(food_params, m) for m in all_materials]
    scored.sort(key=lambda r: r["compatibility_score"], reverse=True)
    return scored[:top_n]
