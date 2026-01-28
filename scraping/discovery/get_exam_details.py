import os
import sys
import json

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)

from scripts.downloadExamQuestions import scrape_test_data


def save(exam_id, details):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Convert to string and create a safe filename
    safe_exam_id = str(exam_id).replace('/', '_').replace('+', '-').replace('=', '')
    output_file = os.path.join(script_dir, f"exam_{safe_exam_id}.json")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(details, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Exam details saved to: {output_file}")
    if isinstance(details, list):
        print(f"✓ Found {len(details)} questions")
    elif isinstance(details, dict):
        print(f"✓ Found {len([k for k in details.keys() if k.startswith('qu')])} questions")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    discovery_file = os.path.join(script_dir, "discovery.json")
    
    discovery = {}
    if os.path.exists(discovery_file):
        with open(discovery_file, 'r') as f:
            discovery = json.load(f)
    
    start_id = 64_34_900
    end_id = 64_35_900
    step = 100
    total_steps = (end_id - start_id) // step
    
    # Counter for progress
    current_step = 0
    
    for id in range(start_id, end_id, step):
        current_step += 1
        progress = (current_step / total_steps) * 100
        print(f"Progress: {progress:.1f}% ({current_step}/{total_steps}) - Checking ID: {id}")

        if str(id) not in discovery:
            details = scrape_test_data(id)
            
            if details is not None:
                test_name = "Unknown Test Name"
                
                # Try to extract name from first question
                if isinstance(details, dict):
                    for k, v in details.items():
                        if k.startswith('qu') and isinstance(v, dict):
                            topic = v.get('TOPIC_NAME', '')
                            subject = v.get('SUBJECT_NAME', '')
                            if topic:
                                test_name = topic
                                if subject and subject != topic:
                                    test_name += f" ({subject})"
                            break
                
                discovery[str(id)] = test_name
                save(id, details)
            else:
                discovery[str(id)] = False
                
            with open(discovery_file, 'w') as f:
                json.dump(discovery, f, indent=2)


