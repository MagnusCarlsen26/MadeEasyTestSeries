import json
import os

# Mapping for MCQ answers based on observed patterns
MCQ_MAPPING = {
    "Dsdj/LJX8pBs6q+b96fwiQ==": "Option 1",
    "fhPK/WKkcuYMengj9uY6cg==": "Option 2",
    "9m/iwvJKC6coEJr5HJJczQ==": "Option 3",
    "Wkw/v0ACIC+JhZVbmq0HcA==": "Option 4"
}

# Fields to remove from each question object
GARBAGE_FIELDS = [
    "LABEL_1", "LABEL_2", "fldUnit", "IS_IMAGE_TYPE", "IS_COMPILER", 
    "IS_RECORDER", "TEST_CASE_TYPE", "fldTextAreaEnable", "ESSAY_SORT", 
    "SORTING_OPTIONS", "OPTION_LABEL", "FREE_SPACE", "ESSAY_TIME", 
    "MINIMUM_QUE_TIME", "isAnswerFileUpload", "MAX_OPT_LIMIT", "TIME", 
    "ESSAY_SORT_H", "SORTING_OPTIONS_H", "TEST_CASE_TYPE_H", "OPTION_LABEL_H",
    "DIFFCULTY_NAME", "ANSWER_TYPE"
]

# Fields to remove from the ENGLISH sub-dictionary
GARBAGE_ENGLISH_FIELDS = [
    "SOLUTION", "ESSAY_ID", "EASSY_DETAILS", "ESSAY_NAME"
]

def decode_answer(q):
    q_type = str(q.get("QUESTION_TYPE"))
    english = q.get("ENGLISH", {})
    ans_encrypted = english.get("CORRECT_ANSWER")
    
    # 1. NAT (Numerical Answer Type)
    if q_type == "2":
        # For NAT, OPT1 usually contains the numerical answer value
        return english.get("OPT1", "Unknown")
    
    # 2. MCQ (Multiple Choice Question)
    if q_type in ["7", "1"]:
        return MCQ_MAPPING.get(ans_encrypted, f"Encrypted MCQ ({ans_encrypted})")
    
    # 3. MSQ (Multiple Select Question)
    if q_type == "5":
        return f"Encrypted MSQ ({ans_encrypted})"
    
    return f"Unknown Type ({q_type})"

def clean_json_files(base_dir):
    for root, dirs, files in os.walk(base_dir):
        if "questions.json" in files:
            filepath = os.path.join(root, "questions.json")
            print(f"Processing: {filepath}")
            
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            if not isinstance(data, dict):
                continue

            modified = False
            for key, value in data.items():
                if key.startswith('qu') and isinstance(value, dict):
                    # Add readable answer
                    value['READABLE_ANSWER'] = decode_answer(value)
                    modified = True # we added readable answer
                    
                    # Remove garbage fields from question object
                    for field in GARBAGE_FIELDS:
                        if field in value:
                            del value[field]
                            modified = True
                    
                    # Remove garbage fields from ENGLISH object
                    english = value.get("ENGLISH")
                    if isinstance(english, dict):
                        for field in GARBAGE_ENGLISH_FIELDS:
                            if field in english:
                                del english[field]
                                modified = True
            
            if modified:
                with open(filepath, 'w') as f:
                    json.dump(data, f, indent=2)

if __name__ == "__main__":
    data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "data"))
    clean_json_files(data_dir)
