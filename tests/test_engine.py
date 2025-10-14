from backend.decision_engine.evaluator import evaluate_item

def test_evaluate_item():
    ocr_lines = ["Sacred Longsword", "+12 Strength", "+5% Crit Damage", "+2% Resistance"]
    build_profile = {
        "class": "Barbarian",
        "preferred_affixes": ["strength", "crit damage", "resistance"]
    }

    result = evaluate_item(ocr_lines, build_profile)

    assert result["decision"] in ["KEEP", "SELL", "SALVAGE"]
    assert "match_score" in result
    print("\n[DEBUG] Evaluation:", result)
