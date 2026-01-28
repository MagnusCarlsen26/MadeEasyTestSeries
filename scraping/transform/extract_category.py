import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from utils.config import SUBJECT_MAPPING

def extract_category(test_name):
    test_name_lower = test_name.lower()
    
    if "basic level test" in test_name_lower:
        return "Basic Level Tests"
    if "advance level test" in test_name_lower:
        return "Advance Level Tests"
    if "mock level test" in test_name_lower:
        return "Mock Level Tests"
    
    if "topicwise test" in test_name_lower or "subjectwise test" in test_name_lower:
        for key, value in SUBJECT_MAPPING.items():
            if key.lower() in test_name_lower:
                return value
    
    if "demo test" in test_name_lower:
        return "Demo Tests"
    
    return "Other Tests"
