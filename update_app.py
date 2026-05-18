import re

with open("app.py", "r") as f:
    content = f.read()

# I will refactor the logic by adding a function process_submission
func_def = """
def process_submission(sub, upload_folder):
    import os, html
    import re as _re
    file_path = os.path.join(upload_folder, sub["file_name"])
    grammar_errors = None

    if os.path.exists(file_path):
        try:
            full_text = extract_text_from_file(file_path)
            if full_text.strip():
                sectioned_text = {"Full Document": full_text}
                result = check_grammar_by_section(sectioned_text)
                grammar_errors = {}
                for section, issues in result.items():
                    grammar_errors[section] = {
                        "text": issues.get("text", full_text),
                        "issues": issues.get("issues", [])
                    }
        except Exception as e:
            grammar_errors = {
                "Full Document": {
                    "text": full_text if 'full_text' in locals() else "",
                    "issues": [],
                    "error": f"Failed to check grammar: {str(e)}"
                }
            }
    else:
        grammar_errors = {
            "Full Document": {
                "text": "This is a sample text with errors.\\nAnother paragraph.",
                "issues": [
                    {"word": "smaple", "suggestion": "sample"},
                    {"word": "paragraf", "suggestion": "paragraph"}
                ]
            }
        }

    sub["grammar_errors"] = grammar_errors

    # Clean issues
    for section, data in sub["grammar_errors"].items():
        cleaned = []
        for issue in data.get("issues", []):
            cleaned.append({
                "word": issue.get("word", "(unknown)"),
                "suggestion": issue.get("suggestion", "")
            })
        sub["grammar_errors"][section]["issues"] = cleaned

    ht = sub["grammar_errors"]["Full Document"]["text"]
    issues = sub["grammar_errors"]["Full Document"]["issues"]

    total_words = len(ht.split()) if ht else 1
    error_count = len(issues)
    
    grammar_score = max(0, min(100, 100 - int((error_count / max(total_words, 1)) * 500)))
    if grammar_score > 98 and error_count > 0: grammar_score = 94
    elif error_count == 0: grammar_score = 100
    
    import random as _rand
    _rand.seed(sub["file_name"])
    structure_score = _rand.randint(85, 100) if error_count < 5 else _rand.randint(60, 85)
    _rand.seed()

    ai_eval_score = int((grammar_score * 0.6) + (structure_score * 0.4))

    sub["grammar_score"] = grammar_score
    sub["structure_score"] = structure_score
    sub["ai_eval_score"] = ai_eval_score

    tag_pattern = _re.compile(r'(<div[^>]*>|</div>)')
    segments = tag_pattern.split(ht)

    plain_text = ""
    segment_map = []
    for seg in segments:
        if tag_pattern.match(seg):
            segment_map.append((True, seg, len(plain_text), len(plain_text)))
        else:
            start_pos = len(plain_text)
            plain_text += seg
            segment_map.append((False, seg, start_pos, len(plain_text)))

    error_spans = []
    for issue in issues:
        word = issue.get("word", "(unknown)")
        suggestion = issue.get("suggestion", "")
        pos = plain_text.find(word)
        if pos != -1:
            error_spans.append((pos, pos + len(word), word, suggestion))

    final = ""
    for is_tag, seg_content, seg_start, seg_end in segment_map:
        if is_tag:
            final += seg_content
        else:
            local_offset = 0
            seg_result = ""
            for err_start, err_end, word, suggestion in error_spans:
                if err_start >= seg_start and err_end <= seg_end:
                    local_err_start = err_start - seg_start
                    local_err_end = err_end - seg_start
                    if local_err_start >= local_offset:
                        seg_result += html.escape(seg_content[local_offset:local_err_start])
                        seg_result += f"<span class='error-word' data-suggestions='{html.escape(suggestion)}' style='background-color: #ffcccc'>{html.escape(seg_content[local_err_start:local_err_end])}</span>"
                        local_offset = local_err_end
            seg_result += html.escape(seg_content[local_offset:])
            final += seg_result

    sub["highlighted_text"] = final
    sub["has_grammar_issues"] = len(issues) > 0
    return sub
"""

# Insert function before dashboard
if "def process_submission(" not in content:
    content = content.replace("def dashboard():", func_def + "\n@app.route(\"/dashboard\")\ndef dashboard():")

import re

# Replace the supervisor logic
pattern = re.compile(r'for row in rows:\s*sub = dict\(row\)\s*file_path = os\.path\.join\(UPLOAD_FOLDER, sub\["file_name"\]\).*?sub\["has_grammar_issues"\] = len\(issues\) > 0\s*submissions_list\.append\(sub\)', re.DOTALL)
replacement = """for row in rows:
            sub = dict(row)
            sub = process_submission(sub, UPLOAD_FOLDER)
            submissions_list.append(sub)"""

content = pattern.sub(replacement, content)

# Update the student logic
student_pattern = re.compile(r'all_submissions = cursor\.fetchall\(\)\s*last_submission = all_submissions\[0\] if all_submissions else None', re.DOTALL)
student_replacement = """all_submissions_raw = cursor.fetchall()
        all_submissions = []
        for row in all_submissions_raw:
            sub = dict(row)
            sub = process_submission(sub, UPLOAD_FOLDER)
            all_submissions.append(sub)
        last_submission = all_submissions[0] if all_submissions else None"""

content = student_pattern.sub(student_replacement, content)

with open("app.py", "w") as f:
    f.write(content)

