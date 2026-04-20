import sys
import json
import sqlite3

from app import extract_text_from_file
from ai_engine.structure_checker import check_all_rules

text = extract_text_from_file('uploads/Asset.docx')
conn = sqlite3.connect("aades_db.sqlite")
cursor = conn.cursor()
cursor.execute("SELECT rules_json FROM evaluation_rules WHERE doc_type = ?", ("project",))
rules_row = cursor.fetchone()
rules = json.loads(rules_row[0])
doc_metadata = {"page_count": 50}

print("Extracted text length:", len(text))
res = check_all_rules(text, rules, doc_metadata)
print("Missing sections:")
print(json.dumps(res['missing_sections'], indent=2))

import re
plain_text = re.sub(r'<[^>]+>', '', text)
plain_lower = plain_text.lower()
print("'candidates\\' declaration' in plain_lower?", "candidates' declaration" in plain_lower)
print("'chapter 1' in plain_lower?", "chapter 1" in plain_lower)
print("'appendices' in plain_lower?", "appendices" in plain_lower)

with open("uploads/asset_text.txt", "w") as f:
    f.write(plain_lower)
