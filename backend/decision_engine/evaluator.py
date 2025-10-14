import re

def normalize_affix(affix: str) -> str:
    #standardize affix text for comparison
    affix = affix.lower()
    affix = re.sub(r"[^a-z0-9%+ ]", "", affix)
    affix = affix.replace("critical strike", "crit")
    return affix.strip()

def evaluate_item(ocr_lines: list, build_profile: dict):
    """evaluate an item's worth based on it's OCR'd text and a build profile
    uses a simple rule-based scoring system for MVP stage
    """
    if not ocr_lines:
        return {"decision": "UNKNOWN", "reason": "No OCR text found"}
    
    #extract item name (first line) and affix lines
    item_name = ocr_lines[0].strip()
    affixes = [line for line in ocr_lines[1:] if "+" in line or "%" in line]\
    
    #normalize
    norm_affixes = [normalize_affix(a) for a in affixes]
    preferred = [normalize_affix(a) for a in build_profile.get("preferred_affixes", [])]

    #match scoring
    matches = sum(1 for affix in norm_affixes if any(p in affix for p in preferred))
    score = matches / max(1, len(preferred))

    #apply thresholds
    if score >= 0.6:
        decision = "KEEP"
        reason = "Matches key build affixes"
    elif score >= 0.3:
        decision = "SALVAGE"
        reason = "Partially relevant affixes - may yield materials or Aspects"
    else:
        decision = "SELL"
        reason = "No relevant affixes detected"

    #return a structured result
    return {
        "item_name": item_name,
        "affixes": affixes, 
        "decision": decision,
        "match_score": round(score, 2),
        "reason": reason,
    }