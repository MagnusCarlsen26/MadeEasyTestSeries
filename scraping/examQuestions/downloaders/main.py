import json
import os
import time
import sys

# Add parent directory to path to allow importing core
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core import MadeEasyAPI, clean_question

def main():
    api = MadeEasyAPI()
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Adjust path to test_ids.json relative to new script location
    test_ids_file = os.path.normpath(os.path.join(current_dir, "../../examId/test_ids.json"))
    
    # Keep extractions in the base examQuestions directory for consistency
    output_dir = os.path.normpath(os.path.join(current_dir, "../extractions"))
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "all_tests_questions.json")
    
    if not os.path.exists(test_ids_file):
        print(f"Error: test_ids.json not found at {test_ids_file}")
        return

    with open(test_ids_file, 'r') as f:
        tests = json.load(f)

    all_questions = []
    
    # Process all tests
    for test in tests:
        test_id = test['testId']
        test_name = test['testName']
        
        print(f"Scraping: {test_name}...")
        data_field = api.scrape_test(test_id)
        
        if data_field and isinstance(data_field, dict):
            questions = []
            # Sort keys to maintain order if possible
            sorted_keys = sorted([k for k in data_field.keys() if k.startswith('qu')], key=lambda x: int(x[2:]))
            for key in sorted_keys:
                value = data_field[key]
                if isinstance(value, dict):
                    # Clean and add metadata
                    clean_question(value)
                    value['TEST_NAME'] = test_name
                    value['TEST_ID'] = test_id
                    questions.append(value)
            
            all_questions.extend(questions)
            print(f"  Fetched {len(questions)} questions.")
        else:
            print(f"  No data found for {test_name}.")
        
        # Save incrementally to avoid losing data
        with open(output_file, 'w') as f:
            json.dump(all_questions, f, indent=2)
        
        time.sleep(1) # Be a bit nice to the server

if __name__ == "__main__":
    main()