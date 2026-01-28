import json
import os
import time
import sys
from collections import defaultdict

# Add parent directory to path to allow importing core
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core import MadeEasyAPI

def probe_range(api, start, end, step=1, delay=0.2, name="Range"):
    """Probe a range of IDs"""
    results = []
    total = (end - start) // step + 1
    
    print(f"\n🔍 {name}: {start} to {end} (step={step}, total={total} IDs)")
    print("=" * 80)
    
    found_count = 0
    for i, test_id in enumerate(range(start, end + 1, step), 1):
        data = api.scrape_test(test_id)
        
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
    api = MadeEasyAPI()
    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.normpath(os.path.join(current_dir, "../extractions"))
    os.makedirs(output_dir, exist_ok=True)

    all_results = []
    
    print("\n" + "=" * 80)
    print("COMPREHENSIVE EXAM ID PROBE (REFACTORED)")
    print("=" * 80)
    
    # PHASE 1: Fill known gaps
    all_results.extend(probe_range(api, 6464573, 6464582, step=1, delay=0.2, name="Gap 1 (IN-CS)"))
    all_results.extend(probe_range(api, 6464621, 6464625, step=1, delay=0.2, name="Gap 2 (CS-EE)"))
    
    # ... (other phases simplified for brevity in this example, or kept as is)
    all_results.extend(probe_range(api, 6464500, 6464549, step=1, delay=0.2, name="ME Block Area"))

    # Save results
    output_file = os.path.join(output_dir, "comprehensive_probe_results.json")
    with open(output_file, 'w') as f:
        json.dump(all_results, f, indent=2)
    
    print(f"✓ Results saved to: {output_file}")

if __name__ == "__main__":
    main()

