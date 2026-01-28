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
    
    probe_results_file = os.path.join(output_dir, 'wide_probe_results.json')
    
    if not os.path.exists(probe_results_file):
        print(f"Error: Probe results not found at {probe_results_file}")
        return

    with open(probe_results_file, 'r') as f:
        all_tests = json.load(f)
    
    # Filter CS tests
    cs_tests = [t for t in all_tests if 'COMPUTER SCIENCE' in t.get('topic', '')]
    
    print(f"\nFound {len(cs_tests)} CS tests to download")
    print("=" * 80)
    
    all_cs_questions = {}
    total_questions = 0
    
    for i, test in enumerate(cs_tests, 1):
        test_id = test['id']
        print(f"\n[{i}/{len(cs_tests)}] Downloading test {test_id} ({test['question_count']}Q - {test['topic']})...")
        
        data = api.scrape_test(test_id)
        
        if data and isinstance(data, dict):
            questions = []
            for key in sorted(data.keys()):
                if key.startswith('qu'):
                    q = data[key]
                    clean_question(q)
                    questions.append(q)
            
            all_cs_questions[test_id] = {
                'test_id': test_id,
                'question_count': len(questions),
                'subject': test.get('subject', ''),
                'topic': test.get('topic', ''),
                'difficulty': test.get('difficulty', ''),
                'questions': questions
            }
            total_questions += len(questions)
            print(f"  ✓ Downloaded {len(questions)} questions")
        else:
            print(f"  ❌ Failed to download")
        
        time.sleep(0.1)
    
    # Save to file
    output_file = os.path.join(output_dir, 'cs_tests_questions.json')
    with open(output_file, 'w') as f:
        json.dump(all_cs_questions, f, indent=2)
    
    print("\n" + "=" * 80)
    print("DOWNLOAD COMPLETE!")
    print(f"✓ Saved to: {output_file}")

if __name__ == "__main__":
    main()

