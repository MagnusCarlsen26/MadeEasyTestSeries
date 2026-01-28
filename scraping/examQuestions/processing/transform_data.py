import json
import os
import hashlib
import sys

# Add parent directory to path to allow importing core
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core import SUBJECT_MAPPING, localize_html

def transform_data(input_path, output_path):
    if not os.path.exists(input_path):
        print(f"Input file not found: {input_path}")
        return

    with open(input_path, 'r') as f:
        scraped_data = json.load(f)

    transformed = {}

    def get_qid(q, idx):
        text_hash = hashlib.md5(q['ENGLISH']['QUESTION_TEXT'].encode()).hexdigest()[:10]
        return f"q_{q['TEST_ID']}_{idx}_{text_hash}"

    def extract_category(test_name):
        test_name_lower = test_name.lower()
        
        if "basic level test" in test_name_lower:
            return "Basic Level Tests"
        if "advance level test" in test_name_lower:
            return "Advance Level Tests"
        if "mock level test" in test_name_lower:
            return "Mock Level Tests"
        
        if "topicwise test" in test_name_lower or "subjectwise test" in test_name_lower:
            for key, value in SUBJECT_MAPPING.items():
                if key.lower() in test_name_lower:
                    return value
        
        if "demo test" in test_name_lower:
            return "Demo Tests"
        
        return "Other Tests"

    for idx, q in enumerate(scraped_data):
        test_name = q.get('TEST_NAME', 'Unnamed Test')
        subject = extract_category(test_name)
        test_id = q.get('TEST_ID', 'test_id_unknown')

        if subject not in transformed:
            transformed[subject] = {}

        if test_name not in transformed[subject]:
            transformed[subject][test_name] = {
                "id": test_id,
                "display_name": test_name,
                "total_qs": 0,
                "total_marks": 0.0,
                "syllabus": f"Complete {subject} Syllabus",
                "test_link": "#",
                "sections": [{"name": "Technical", "questions": []}]
            }

        test_obj = transformed[subject][test_name]
        q_english = q['ENGLISH']
        
        # Build question text with localized image paths
        q_text = localize_html(q_english['QUESTION_TEXT'])
        
        # Add options to text
        options_html = ""
        has_options = False
        for i in range(1, 11):
            opt_key = f'OPT{i}'
            if opt_key in q_english and q_english[opt_key]:
                has_options = True
                opt_text = localize_html(q_english[opt_key])
                options_html += f'<li>{opt_text}</li>'
        
        if has_options:
            q_text += f'<ol style="list-style-type:upper-alpha">{options_html}</ol>'

        transformed_q = {
            "global_idx": idx + 1,
            "local_idx": len(test_obj['sections'][0]['questions']) + 1,
            "post_id": get_qid(q, idx),
            "text": q_text,
            "answer": q.get('READABLE_ANSWER', 'Not Answered'),
            "award": float(q.get('RIGHT_MARKS', 0)),
            "penalty": q.get('WRONG_MARKS', "0")
        }

        test_obj['sections'][0]['questions'].append(transformed_q)
        test_obj['total_qs'] = len(test_obj['sections'][0]['questions'])
        test_obj['total_marks'] += transformed_q['award']

    final_output = {sub: list(tests.values()) for sub, tests in transformed.items()}

    with open(output_path, 'w') as f:
        json.dump(final_output, f, indent=2)

    print(f"Successfully transformed data and saved to {output_path}")

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.normpath(os.path.join(current_dir, "../extractions/all_tests_questions.json"))
    output_file = os.path.normpath(os.path.join(current_dir, "../../../web/data.json"))
    
    transform_data(input_file, output_file)

