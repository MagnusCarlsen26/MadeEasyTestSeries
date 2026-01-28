import os
import sys
from .decode_answer import decode_answer

# Add parent directory to path to allow importing core config
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from config import GARBAGE_FIELDS, GARBAGE_ENGLISH_FIELDS

def clean_question(q):
    """Removes garbage fields and adds a READABLE_ANSWER."""
    q['READABLE_ANSWER'] = decode_answer(q)
    
    if 'HINDI' in q:
        del q['HINDI']
    
    for field in GARBAGE_FIELDS:
        if field in q:
            del q[field]
            
    english = q.get("ENGLISH")
    if isinstance(english, dict):
        for field in GARBAGE_ENGLISH_FIELDS:
            if field in english:
                del english[field]
    
    return q
