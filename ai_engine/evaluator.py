# ai_engine/evaluator.py

def evaluate_document(text):
    issues = []

    if len(text.strip()) == 0:
        return {
            "status": "failed",
            "message": "Document is empty",
            "grammar_issues": 0
        }

    # Simple grammar check placeholder: counts double spaces as errors
    grammar_issues = text.count("  ")

    return {
        "status": "success",
        "message": "Evaluation Complete",
        "grammar_issues": grammar_issues
    }
