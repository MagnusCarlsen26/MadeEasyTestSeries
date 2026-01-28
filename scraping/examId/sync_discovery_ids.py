import os
import json
import base64
import re
import sys

# Add root to path for imports
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)

from utils.io_utils import read_json, write_json

def parse_test_details(test_name):
    """
    Determines testType, level, subject, and branch from a test name.
    """
    details = {
        "testType": "Other",
        "branch": "Unknown"
    }
    
    # 1. Determine Branch
    if " CS" in test_name or "Computer Science" in test_name or "CS & IT" in test_name:
        details["branch"] = "CS"
    elif " CH" in test_name or "Chemical Engineering" in test_name:
        details["branch"] = "CH"
    
    # 2. Determine Test Type
    if "Topicwise" in test_name:
        details["testType"] = "Topicwise"
    elif "Subjectwise" in test_name:
        details["testType"] = "Subjectwise"
    elif "Full Syllabus" in test_name:
        details["testType"] = "Full Syllabus"
    elif "DEMO TEST" in test_name:
        details["testType"] = "Demo"
    
    # 3. Determine Level (for Full Syllabus)
    if details["testType"] == "Full Syllabus":
        if "Basic" in test_name:
            details["level"] = "Basic"
        elif "Mock" in test_name:
            details["level"] = "Mock"
        elif "Advance" in test_name:
            details["level"] = "Advance"
    
    # 4. Extract Subject (for Topicwise/Subjectwise)
    if details["testType"] in ["Topicwise", "Subjectwise"]:
        # Try to find subject after the branch code
        # Example: Subjectwise Test-1 Part Syllabus GATE 2025 CS Theory of Computation
        match = re.search(r'(CS|CH)\s+(.+)$', test_name)
        if match:
            subject = match.group(2).strip()
            # Clean up trailing numbers like -1, -2 for topicwise
            subject = re.sub(r'-\d+$', '', subject).strip()
            details["subject"] = subject

    return details

def sync_test_ids():
    discovery_path = "/home/khushal/Desktop/Projects/MadeEasyTestSeries/scraping/discovery/package_details.json"
    exam_ids_path = "/home/khushal/Desktop/Projects/MadeEasyTestSeries/scraping/examId/test_ids.json"
    
    # Load existing IDs
    existing_ids = read_json(exam_ids_path)
    if not isinstance(existing_ids, list):
        existing_ids = []
    
    # Map index by decoded ID for faster lookup/overwrite
    id_map = {}
    for entry in existing_ids:
        try:
            decoded = base64.b64decode(entry['testId']).decode('utf-8')
            id_map[decoded] = entry
        except:
            continue

    # Load from package_details.json
    try:
        discovery_data = read_json(discovery_path)
        packages = discovery_data.get('data', [])
        
        new_count = 0
        updated_count = 0
        
        for pkg in packages:
            test_ids = pkg.get('testId', '').split(',')
            test_names = pkg.get('testName', '').split('$#$')
            
            if len(test_ids) != len(test_names):
                print(f"Warning: ID/Name mismatch in package {pkg.get('packageName')}")
                continue
                
            for tid, tname in zip(test_ids, test_names):
                tid = tid.strip()
                tname = tname.strip()
                if not tid: continue
                
                b64_id = base64.b64encode(tid.encode('utf-8')).decode('utf-8')
                details = parse_test_details(tname)
                
                # Filter for CS branch only
                if details.get('branch') != 'CS':
                    continue
                
                entry = {
                    "testId": b64_id,
                    "testName": tname,
                    **details
                }
                # Remove None values
                entry = {k: v for k, v in entry.items() if v is not None}
                
                if tid in id_map:
                    id_map[tid].update(entry)
                    updated_count += 1
                else:
                    id_map[tid] = entry
                    new_count += 1
        
        # Sort and save
        final_list = sorted(id_map.values(), key=lambda x: x.get('testName', ''))
        write_json(final_list, exam_ids_path)
        
        print(f"Sync Complete: {new_count} new tests added, {updated_count} existing tests updated.")
        print(f"Total tests in {exam_ids_path}: {len(final_list)}")
        
    except Exception as e:
        print(f"Sync Error: {e}")

if __name__ == "__main__":
    sync_test_ids()
