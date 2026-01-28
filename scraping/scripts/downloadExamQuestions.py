import os
import time
import sys
import requests
import json
import base64
from concurrent.futures import ThreadPoolExecutor, as_completed

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)

from utils.config import DEFAULT_HEADERS, INITIAL_TOKEN, BASE_URL, BASE_REQUEST_DATA
from utils.io_utils import read_json, write_json, ensure_dir

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
            timeout=30 # Increased timeout for stability
        )

        if response.status_code == 200:
            resp_json = response.json()
            if 'data' in resp_json:
                return json.loads(resp_json['data'])
        return None

    except Exception as e:
        print(f"API Error for {test_id}: {e}")
        return None

def process_single_test(entry, raw_output_dir):
    """
    Downloads and saves a single test. Returns result dict if successful, None if skipped/failed.
    """
    test_id = entry['testId']
    test_name = entry['testName']
    
    # Clean filename for individual storage
    safe_test_id = test_id.replace('/', '_').replace('+', '-')
    file_path = os.path.join(raw_output_dir, f"{safe_test_id}.json")
    
    # Resumability check
    if os.path.exists(file_path):
        return ("SKIPPED", test_name)

    data = scrape_test_data(test_id)
    if data:
        # Add metadata
        data['TEST_NAME'] = test_name
        data['TEST_ID_ENCODED'] = test_id
        # Adding TEST_ID as well since downstream process_data.py/get_qid expects it
        data['TEST_ID'] = test_id
        
        # Save individual file immediately
        write_json(data, file_path)
        return ("DOWNLOADED", test_name)
    else:
        return ("FAILED", test_name)

def run_exam_download(test_ids_path, output_dir, max_workers=5):
    """
    Downloads all exams using threading and saves them individually.
    Finally merges them into one big file for backward compatibility.
    """
    test_ids_data = read_json(test_ids_path)
    
    raw_output_dir = os.path.join(output_dir, "raw")
    ensure_dir(raw_output_dir)
    
    total = len(test_ids_data)
    print(f"[*] Starting download of {total} exams with {max_workers} threads...")
    
    stats = {"SKIPPED": 0, "DOWNLOADED": 0, "FAILED": 0}
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_test = {
            executor.submit(process_single_test, entry, raw_output_dir): entry 
            for entry in test_ids_data
        }
        
        for i, future in enumerate(as_completed(future_to_test), 1):
            result = future.result()
            if result:
                status, name = result
                stats[status] += 1
                sys.stdout.write(f"\r[{i}/{total}] {status}: {name[:30]}...")
                sys.stdout.flush()
    
    print(f"\n[+] Download Complete. Stats: {stats}")
    
    # Merge step
    print("[*] Merging individual files into all_tests_questions.json...")
    merge_results(raw_output_dir, os.path.join(output_dir, "all_tests_questions.json"))

def merge_results(raw_dir, output_file):
    """
    Reads all JSON files from raw_dir and helps construct the final structure.
    Note: The original structure was Dict[test_id, Dict].
    """
    merged = {}
    files = [f for f in os.listdir(raw_dir) if f.endswith('.json')]
    
    for f in files:
        path = os.path.join(raw_dir, f)
        data = read_json(path)
        test_id = data.get('TEST_ID_ENCODED')
        test_name = data.get('TEST_NAME')
        
        if not test_id: 
            continue

        # Extract questions
        questions = []
        for k, v in data.items():
            if k.startswith('qu') and isinstance(v, dict):
                v['TEST_NAME'] = test_name
                v['TEST_ID_ENCODED'] = test_id
                v['TEST_ID'] = test_id
                questions.append(v)
        
        # Reconstruct the entry expected by process_data.py
        # We need the original metadata, but it's not fully inside 'data' except what we added.
        # Ideally we'd map back to test_ids.json, but for now we reconstruct basic meta.
        merged[test_id] = {
            "metadata": {"testId": test_id, "testName": test_name},
            "questions": questions
        }

    write_json(merged, output_file)
    print(f"[+] Merged {len(merged)} tests to {output_file}")

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # IMPORTANT: Switching to SCRAPED_DATA directory as the source of truth
    scraped_data_dir = os.path.normpath(os.path.join(current_dir, "../scraped_data"))
    
    # Input file from scraped_data
    test_ids_path = os.path.join(scraped_data_dir, "test_ids.json")
    
    if not os.path.exists(test_ids_path):
        print(f"Error: {test_ids_path} not found.")
        sys.exit(1)

    # Output to scraped_data
    run_exam_download(test_ids_path, scraped_data_dir, max_workers=10)
