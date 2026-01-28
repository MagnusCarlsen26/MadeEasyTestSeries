import os
import sys

# Add parent directory to path to allow importing core config
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from config import MCQ_MAPPING

def decode_answer(q):
    """Decodes the CORRECT_ANSWER field into a readable string."""
    q_type = str(q.get("QUESTION_TYPE") or q.get("QUESTION_TYPE_ID") or "")
    q_type_name = q.get("QUESTION_TYPE_NAME")
    
    english = q.get("ENGLISH", {})
    ans_encrypted = english.get("CORRECT_ANSWER") or q.get("CORRECT_ANSWER")
    
    if q_type == "2" or q_type_name == "NAT":
        return english.get("OPT1") or q.get("OPT1") or "Unknown"
    
    if q_type in ["7", "1"] or q_type_name == "MCQ":
        return MCQ_MAPPING.get(ans_encrypted, f"Encrypted MCQ ({ans_encrypted})")
    
    if q_type == "5" or q_type_name == "MSQ":
        return f"Encrypted MSQ ({ans_encrypted})"
    
    return f"Unknown Type ({q_type}/{q_type_name})"
