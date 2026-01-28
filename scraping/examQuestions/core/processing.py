import os
import re
import hashlib
from urllib.parse import urlparse
from .config import MCQ_MAPPING, GARBAGE_FIELDS, GARBAGE_ENGLISH_FIELDS

def decode_answer(q):
    """
    Decodes the CORRECT_ANSWER field into a readable string.
    Works for NAT, MCQ, and MSQ types.
    """
    q_type = str(q.get("QUESTION_TYPE") or q.get("QUESTION_TYPE_ID") or "")
    # Check alternate field name used in some versions
    q_type_name = q.get("QUESTION_TYPE_NAME")
    
    english = q.get("ENGLISH", {})
    ans_encrypted = english.get("CORRECT_ANSWER") or q.get("CORRECT_ANSWER")
    
    # NAT (Numerical Answer Type)
    if q_type == "2" or q_type_name == "NAT":
        return english.get("OPT1") or q.get("OPT1") or "Unknown"
    
    # MCQ (Multiple Choice Question)
    if q_type in ["7", "1"] or q_type_name == "MCQ":
        return MCQ_MAPPING.get(ans_encrypted, f"Encrypted MCQ ({ans_encrypted})")
    
    # MSQ (Multiple Select Question)
    if q_type == "5" or q_type_name == "MSQ":
        return f"Encrypted MSQ ({ans_encrypted})"
    
    return f"Unknown Type ({q_type}/{q_type_name})"

def clean_question(q):
    """
    Removes garbage fields and adds a READABLE_ANSWER.
    Modifies the question object in-place.
    """
    # Add readable answer
    q['READABLE_ANSWER'] = decode_answer(q)
    
    # Clean HINDI content if any (we focus on English)
    if 'HINDI' in q:
        del q['HINDI']
    
    # Remove top-level garbage fields
    for field in GARBAGE_FIELDS:
        if field in q:
            del q[field]
            
    # Remove garbage fields from ENGLISH sub-dict
    english = q.get("ENGLISH")
    if isinstance(english, dict):
        for field in GARBAGE_ENGLISH_FIELDS:
            if field in english:
                del english[field]
    
    return q

def localize_html(html, images_path="images/"):
    """
    Replaces absolute image URLs with local paths.
    """
    if not html:
        return html

    def replace_src(match):
        url = match.group(1)
        parsed = urlparse(url)
        basename = os.path.basename(parsed.path)
        if not basename or len(basename) < 5:
            basename = hashlib.md5(url.encode()).hexdigest() + ".png"
        return f'src="{images_path}{basename}"'

    return re.sub(r'src="([^"]+)"', replace_src, html)
