# ai_engine/evaluator.py

from textblob import TextBlob

def evaluate_document(text):
    """
    Evaluates a PDF's text for grammar issues using TextBlob.
    
    Args:
        text (str): Extracted text from PDF.
    
    Returns:
        dict: Contains status, message, number of grammar issues, and suggestions.
    """
    if len(text.strip()) == 0:
        # If PDF has no readable text
        return {
            "status": "failed",
            "message": "Document is empty",
            "grammar_issues": 0,
            "suggestions": []
        }

    # Create a TextBlob object
    blob = TextBlob(text)

    # Corrected text using TextBlob's spell and grammar correction
    corrected_text = blob.correct()

    # Split original and corrected texts into words
    original_words = text.split()
    corrected_words = corrected_text.split()

    # Count differences as grammar issues
    grammar_issues = 0
    suggestions = []

    for i, word in enumerate(original_words):
        if i < len(corrected_words) and word != corrected_words[i]:
            grammar_issues += 1
            suggestions.append(f"{word} → {corrected_words[i]}")

    # Limit suggestions to first 10 to avoid long output
    suggestions = suggestions[:10]

    return {
        "status": "success",
        "message": "Evaluation Complete",
        "grammar_issues": grammar_issues,
        "suggestions": suggestions
    }
