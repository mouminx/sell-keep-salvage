from fastapi import FastAPI, UploadFile, File
from backend.decision_engine.evaluator import evaluate_item
from backend.build_parser.scraper import parse_build
from backend.ocr.parser import extract_text
from backend.decision_engine.leveling_evaluator import evaluate_leveling_item

app = FastAPI()


@app.get("/")
def root():
    return {"status": "Sell/Keep/Salvage API running"}


@app.post("/evaluate")
def evaluate(item_data: dict, build_profile: dict):
    """Evaluate an item against a build profile."""
    return {"result": evaluate_item(item_data, build_profile)}


@app.post("/test-ocr")
async def test_ocr(file: UploadFile = File(...)):
    """Extract text from uploaded image."""
    temp_path = f"data/{file.filename}"
    try:
        with open(temp_path, "wb") as f:
            f.write(await file.read())

        text_lines = extract_text(temp_path)
        if not isinstance(text_lines, list):
            text_lines = []
    except Exception as e:
        # Always return error in predictable format for tests
        return {"error": str(e)}

    return {"lines": text_lines}

@app.post("/evaluate-leveling")
def evaluate_leveling(item_data: dict):
    #evaluate an item based on leveling priorities (focus on damage, speed, etc)

    ocr_lines = item_data.get("ocr_lines", [])
    focus = item_data.get("focus", [])
    result = evaluate_leveling_item(ocr_lines, focus)
    return {"result": result}
