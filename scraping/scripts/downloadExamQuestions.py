import os
import time
import sys
import requests
import json
import base64

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)

from config import DEFAULT_HEADERS, INITIAL_TOKEN, BASE_URL, BASE_REQUEST_DATA
from transform import clean_question
from io_utils import read_json, write_json

def scrape_test_data(test_id, token=INITIAL_TOKEN):
    """
    Fetches question data for a given test_id.
    test_id can be a number or a base64 encoded string.
    """
    # If test_id is an integer or numeric string, encode it to base64
    if isinstance(test_id, int) or (isinstance(test_id, str) and test_id.isdigit()):
        test_id = base64.b64encode(str(test_id).encode('utf-8')).decode('utf-8')

    base_json = BASE_REQUEST_DATA.copy()
    base_json.update({
        "accessToken": token,
        "parameter": {"testId": test_id}
    })

    payload = {'data': json.dumps(base_json)}

    try:
        response = requests.post(
            BASE_URL, 
            headers=DEFAULT_HEADERS, 
            data=payload, 
            timeout=15
        )

        if response.status_code == 200:
            resp_json = response.json()
            if 'data' in resp_json:
                return json.loads(resp_json['data'])
        return None

    except Exception as e:
        print(f"API Error: {e}")
        return None

def run_exam_download(test_ids_path, output_path):
    """Downloads all exams defined in the test_ids file."""
    test_ids_data = read_json(test_ids_path)
    
    results = {}
    total = len(test_ids_data)
    
    print(f"[*] Starting download of {total} exams...")
    
    for i, entry in enumerate(test_ids_data, 1):
        test_id = entry['testId']
        test_name = entry['testName']
        
        print(f"[{i}/{total}] Downloading: {test_name} ({test_id})", end='\r')
        
        data = scrape_test_data(test_id)
        if data:
            # Add some metadata that might be useful
            data['TEST_NAME'] = test_name
            data['TEST_ID_ENCODED'] = test_id
            
            # Extract questions to match the expected format for process_data.py
            questions = []
            for k, v in data.items():
                if k.startswith('qu') and isinstance(v, dict):
                    v['TEST_NAME'] = test_name
                    v['TEST_ID_ENCODED'] = test_id
                    questions.append(v)
            
            results[test_id] = {
                "metadata": entry,
                "questions": questions
            }
        
        # Small delay to be nice to the server
        time.sleep(0.5)

    write_json(results, output_path)
    print(f"\n[+] Successfully downloaded {len(results)} exams to {output_path}")

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    scraped_data_dir = os.path.normpath(os.path.join(current_dir, "../scraped_data"))
    test_ids_path = os.path.normpath(os.path.join(current_dir, "../examId/test_ids.json"))
    output_path = os.path.join(scraped_data_dir, "all_tests_questions.json")
    
    run_exam_download(test_ids_path, output_path)
