import json
import re

def parse_test_name(test_name):
    details = {
        "testType": "Other"
    }
    
    # 1. Determine Test Type
    if "Topicwise" in test_name:
        details["testType"] = "Topicwise"
    elif "Subjectwise" in test_name:
        details["testType"] = "Subjectwise"
    elif "Full Syllabus" in test_name:
        details["testType"] = "Full Syllabus"
    
    # 2. Determine Level (for Full Syllabus)
    if details["testType"] == "Full Syllabus":
        if "Basic" in test_name:
            details["level"] = "Basic"
        elif "Mock" in test_name:
            details["level"] = "Mock"
        elif "Advance" in test_name:
            details["level"] = "Advance"
    
    # 3. Extract Subject Name (for Topicwise/Subjectwise)
    if details["testType"] in ["Topicwise", "Subjectwise"]:
        # Standard pattern seems to be: ... GATE 2025 CS [Subject Name]
        match = re.search(r'CS\s+(.+)$', test_name)
        if match:
            subject = match.group(1).strip()
            # Clean up trailing numbers like -1, -2 for topicwise
            subject = re.sub(r'-\d+$', '', subject).strip()
            details["subject"] = subject

    return details

def extract_test_info(input_file, output_file):
    try:
        with open(input_file, 'r') as f:
            data = json.load(f)
        
        test_list = data.get('data', [])
        extracted_info = []
        
        for test in test_list:
            test_id = test.get('testId')
            test_name = test.get('testName')
            if test_id and test_name:
                details = parse_test_name(test_name)
                entry = {
                    "testId": test_id,
                    "testName": test_name,
                    **details
                }
                # Remove keys with None values
                entry = {k: v for k, v in entry.items() if v is not None}
                extracted_info.append(entry)
        
        with open(output_file, 'w') as f:
            json.dump(extracted_info, f, indent=2)
            
        print(f"Successfully extracted {len(extracted_info)} tests with refined details (no nulls) to {output_file}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # data.json is in the parent of scraping folder
    import os
    current_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(current_dir, "../../data.json")
    output_path = os.path.join(current_dir, "test_ids.json")
    extract_test_info(input_path, output_path)
