from backend.decision_engine.leveling_evaluator import evaluate_leveling_item

def test_evaluate_leveling_item():
    ocr_lines = [
        "Sacred Sword",
        "+12 Damage",
        "+5% Movement Speed",
        "+10% Fire Resistance"
    ]
    focus = ["damage", "movement speed"]

    result = evaluate_leveling_item(ocr_lines, focus)

    assert "decision" in result
    assert "match_score" in result
    assert result["decision"] in ["KEEP", "SALVAGE", "SELL"]

    print("\n[DEBUG]", result)