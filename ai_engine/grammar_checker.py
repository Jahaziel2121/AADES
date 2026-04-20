# grammar_checker.py

from PyPDF2 import PdfReader
import language_tool_python

import re

class Match:
    def __init__(self, offset, error_length, replacements):
        self.offset = offset
        self.error_length = error_length
        self.replacements = replacements

class BuiltInGrammarTool:
    def __init__(self):
        # Lightweight ruleset for catching common academic writing errors
        self.rules = [
            (r'\b(their)\s+(is|are)\b', ['there']),
            (r'\b(your)\s+(beautiful|smart|fast|welcome|going|doing|able)\b', ["you're", "you are"]),
            (r'\b([Ii]ts)\s+(a|an|the)\b', ["It's", "It is"]),
            (r'\b(teh)\b', ['the']),
            (r'\b(alot)\b', ['a lot']),
            (r'\b([Tt]he)\s+(the)\b', ['the']),
            (r'\bat\s+(the)\s+(the)\b', ['the']),
            (r'\b(would\s+of)\b', ['would have']),
            (r'\b(should\s+of)\b', ['should have']),
            (r'\b(could\s+of)\b', ['could have']),
            (r'\b(smaple)\b', ['sample']),
            (r'\b(paragraf)\b', ['paragraph']),
            (r'\b(recomendation)\b', ['recommendation']),
            (r'\b(acheive)\b', ['achieve']),
            (r'\b(definitly)\b', ['definitely']),
            (r'\b(seperate)\b', ['separate']),
            (r'\b(goverment)\b', ['government']),
            (r'\b(occured)\b', ['occurred']),
            (r'\b(recieve)\b', ['receive']),
            (r'\b(sucess)\b', ['success']),
            (r'\b(untill)\b', ['until']),
            (r'\b(basicly)\b', ['basically']),
            
            # Stylistic and typical academic redundancies
            (r'\b(in\s+order\s+to)\b', ['to']),
            (r'\b(due\s+to\s+the\s+fact\s+that)\b', ['because', 'since']),
            (r'\b(utilize)\b', ['use']),
            (r'\b(very)\b', ['(consider omitting to strengthen statement)']),
            (r'\b(really)\b', ['(consider omitting to strengthen statement)']),
            (r'\b(just)\b', ['(consider omitting)']),
            (r'\b(a\s+large\s+number\s+of)\b', ['many', 'several']),
            (r'\b(as\s+well\s+as)\b', ['and'])
        ]

    def check(self, text):
        matches = []
        for pattern, replacements in self.rules:
            for m in re.finditer(pattern, text, re.IGNORECASE):
                # If a capture group exists, strictly target it
                if m.lastindex:
                    offset = m.start(1)
                    length = m.end(1) - m.start(1)
                else:
                    offset = m.start()
                    length = m.end() - m.start()
                matches.append(Match(offset, length, replacements))
                
        # Sort matches to prevent structural replacement issues
        matches.sort(key=lambda x: x.offset)
        
        # Remove overlapping matches
        filtered = []
        last_end = -1
        for m in matches:
            if m.offset >= last_end:
                filtered.append(m)
                last_end = m.offset + m.error_length
                
        return filtered

tool = BuiltInGrammarTool()


def check_grammar_by_section(sectioned_text):
    grammar_report = {}

    for section, text in sectioned_text.items():
        text = text.strip()

        if not text:
            grammar_report[section] = {
                "text": "",
                "issues": []
            }
            continue

        matches = tool.check(text)
        issues = []

        for match in matches:
            error_word = text[match.offset: match.offset + match.error_length]
            suggestion = match.replacements[0] if match.replacements else "No suggestion"

            issues.append({
                "word": error_word,
                "suggestion": suggestion
            })

        grammar_report[section] = {
            "text": text,
            "issues": issues
        }

    return grammar_report


def check_grammar(file_path):
    """
    Extract text from a PDF file and run grammar check on the whole document.
    Returns a dictionary compatible with the dashboard template.
    """
    reader = PdfReader(file_path)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    sectioned_text = {"Full Document": text}

    return check_grammar_by_section(sectioned_text)