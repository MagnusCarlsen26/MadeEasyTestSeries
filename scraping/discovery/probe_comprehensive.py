import json
import os
from io_utils import write_json
import time
import sys
from collections import defaultdict

# Add parent directory to path to allow importing core
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.downloadExamQuestions import scrape_test_data

def probe_range(start, end, step=1, delay=0.2, name="Range"):
    """Probe a range of IDs"""
    results = []
    total = (end - start) // step + 1
    
    print(f"\n🔍 {name}: {start} to {end} (step={step}, total={total} IDs)")
    print("=" * 80)
    
    found_count = 0
    for i, test_id in enumerate(range(start, end + 1, step), 1):
        data = scrape_test_data(test_id)
        
        if data and isinstance(data, dict):
            q_keys = [k for k in data.keys() if k.startswith('qu')]
            if q_keys:
                found_count += 1
                first_q = data[q_keys[0]]
                result = {
                    'id': test_id,
                    'exists': True,
                    'question_count': len(q_keys),
                    'subject': first_q.get('SUBJECT_NAME', 'Unknown'),
                    'topic': first_q.get('TOPIC_NAME', 'Unknown'),
                    'difficulty': first_q.get('DIFFCULTY_NAME', ''),
                }
                results.append(result)
                print(f"[{i}/{total}] ✓ {test_id}: {result['question_count']}Q - {result['subject']} / {result['topic']}")
            else:
                if i % 10 == 0 or i == total:
                    print(f"[{i}/{total}] Probing (empty)...", end='\r')
        else:
            if i % 10 == 0 or i == total:
                print(f"[{i}/{total}] Probing...", end='\r')
        
        time.sleep(delay)
    
    print(f"\n{'=' * 80}")
    print(f"Found {found_count} valid tests out of {total} probed IDs ({found_count/total*100:.1f}% hit rate)")
    return results

def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.normpath(os.path.join(current_dir, "../../scraped_data"))

    print("\n" + "=" * 80)
    print("COMPREHENSIVE EXAM ID PROBE")
    print("=" * 80)
    
    try:
        start_range = int(input("Enter start ID: "))
        end_range = int(input("Enter end ID: "))
        sample_step = int(input("Enter step (default 1): ") or "1")
    except ValueError:
        print("Invalid input.")
        return

    all_results = probe_range(start_range, end_range, step=sample_step, name="User Range")

    if all_results:
        # Save results
        output_file = os.path.join(output_dir, "comprehensive_probe_results.json")
        write_json(all_results, output_file)
        
        print(f"✓ Results saved to: {output_file}")
    else:
        print("No valid tests found.")

if __name__ == "__main__":
    main()

