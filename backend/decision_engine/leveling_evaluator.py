import re

def normalize_affix(affix: str) -> str:
    #standardize affix text for comparison
    affix = affix.lower()
    affix = re.sub(r"[^a-z0-9\s%+]", "", affix)
    return affix.strip()

def evaluate_leveling_item(ocr_lines: list[str], focus: list[str]) -> dict:
    #evaluate an item based on player-selected focus areas during leveling
    #example focus: ["damage", "movement speed", "defense"]
    if not ocr_lines:
        return {"decision": "UNKOWN", "reason": "No OCR text found"}
    
    item_name = ocr_lines[0].strip()
    affixes = [line for line in ocr_lines[1:] if "+" in line or "%" in line]

    norm_affixes = [normalize_affix(a) for a in affixes]
    norm_focus = [normalize_affix(f) for f in focus]

    #simple match sorting
    matches = sum(1 for a in norm_affixes if any(f in a for f in norm_focus))
    score = matches / max(1, len(norm_focus))

    if score >= 0.6:
        decision, reason = "KEEP", "Strong alignment with focus stats"
    elif score >= 0.3:
        decision, reason = "SALVAGE", "Somewhat relevant affixes"
    else:
        decision, reason = "SELL", "Low alignment with focus"

    return {
        "item_name": item_name,
        "affixes": affixes,
        "decision": decision,
        "match_score": round(score, 2),
        "reason": reason,
    }