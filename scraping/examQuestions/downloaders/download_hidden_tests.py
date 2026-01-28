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
    output_dir = os.path.normpath(os.path.join(current_dir, "../extractions"))
    os.makedirs(output_dir, exist_ok=True)
    
    # All downloadable hidden test IDs
    hidden_tests = [
        6464563, 6464564, 6464565, 6464566, 6464567,
        6464568, 6464569, 6464570, 6464571, 6464572,
        6464626, 6464627, 6464628, 6464629, 6464630,
        6464631, 6464632, 6464633, 6464634, 6464635,
        6464636, 6464637, 6464638, 6464639, 6464640
    ]
    
    print(f"Downloading {len(hidden_tests)} hidden tests...")
    print("=" * 60)
    
    all_questions = []
    success_count = 0
    
    for test_id in hidden_tests:
        print(f"\nDownloading test {test_id}...", end=" ")
        data = api.scrape_test(test_id)
        
        if data and isinstance(data, dict):
            questions = []
            for key in sorted(data.keys()):
                if key.startswith('qu'):
                    q = data[key]
                    clean_question(q)
                    questions.append(q)
            
            all_questions.extend(questions)
            success_count += 1
            print(f"✓ {len(questions)} questions")
        else:
            print("✗ Failed")
        
        time.sleep(1)  # Rate limiting
    
    # Save to file
    output_file = os.path.join(output_dir, "hidden_tests_questions.json")
    with open(output_file, 'w') as f:
        json.dump(all_questions, f, indent=2)
    
    print(f"\n{'=' * 60}")
    print(f"✓ Downloaded {len(all_questions)} total questions from {success_count}/{len(hidden_tests)} tests")
    print(f"✓ Saved to: {output_file}")

if __name__ == "__main__":
    main()

