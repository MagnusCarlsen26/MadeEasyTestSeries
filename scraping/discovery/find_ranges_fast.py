import json
import os
import time
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.downloadExamQuestions import scrape_test_data
from io_utils import write_json

def probe_test_id(test_id):
    """Test if a test ID exists"""
    data = scrape_test_data(test_id)
    if data and isinstance(data, dict):
        q_keys = [k for k in data.keys() if k.startswith('qu')]
        if q_keys:
            first_q = data[q_keys[0]]
            return {
                'exists': True,
                'question_count': len(q_keys),
                'subject': first_q.get('SUBJECT_NAME', 'Unknown'),
                'topic': first_q.get('TOPIC_NAME', 'Unknown'),
            }
    return {'exists': False}

def find_range_boundaries(start, end, step=10):
    """Find where tests start and end in a range"""
    print(f"\n🔍 Scanning {start} to {end} (step={step})...")
    
    valid_ids = []
    for test_id in range(start, end + 1, step):
        result = probe_test_id(test_id)
        if result['exists']:
            valid_ids.append(test_id)
            print(f"  ✓ {test_id} ({result['question_count']}Q - {result['topic']})")
    
    return valid_ids

def find_exact_boundaries(valid_ids, search_radius=30):
    """Find exact start/end of ranges around discovered IDs"""
    ranges = []
    processed = set()
    
    for vid in valid_ids:
        if vid in processed:
            continue
            
        # Search backward
        start = vid
        for test_id in range(vid - 1, max(vid - search_radius - 1, 0), -1):
            result = probe_test_id(test_id)
            if result['exists']:
                start = test_id
                processed.add(test_id)
            else:
                break
        
        # Search forward
        end = vid
        for test_id in range(vid + 1, vid + search_radius + 1):
            result = probe_test_id(test_id)
            if result['exists']:
                end = test_id
                processed.add(test_id)
            else:
                break
        
        processed.add(vid)
        ranges.append((start, end))
        print(f"  📍 Range: {start} - {end} (span: {end - start + 1})")
    
    return ranges

def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.normpath(os.path.join(current_dir, "../../scraped_data"))
    
    print("=" * 80)
    print("FAST RANGE FINDER")
    print("=" * 80)
    
    try:
        start_range = int(input("Enter start ID (default 6464000): ") or "6464000")
        end_range = int(input("Enter end ID (default 6466000): ") or "6466000")
        sample_step = int(input("Enter sampling step (default 10): ") or "10")
    except ValueError:
        print("Invalid input, using defaults.")
        start_range, end_range, sample_step = 6464000, 6466000, 10

    all_valid_ids = find_range_boundaries(start_range, end_range, step=sample_step)
    
    print(f"\n✓ Found {len(all_valid_ids)} valid IDs in sampling")
    
    if all_valid_ids:
        # Find exact boundaries
        ranges = find_exact_boundaries(all_valid_ids, search_radius=30)
        
        # Save results
        output_file = os.path.join(output_dir, 'test_id_ranges.json')
        write_json({'ranges': ranges}, output_file)
        
        print(f"\n✓ Ranges saved to: {output_file}")
    else:
        print("\nNo valid IDs found in the specified range.")

if __name__ == "__main__":
    main()

