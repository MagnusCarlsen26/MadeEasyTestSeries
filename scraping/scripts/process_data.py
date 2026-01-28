import os
import sys

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)

from transform import extract_category, process_question, clean_question
from utils.io_utils import read_json, write_json

def transform_data(input_path, output_path):
    scraped_data = read_json(input_path)

    if isinstance(scraped_data, dict):
        all_qs = []
        for test_data in scraped_data.values():
            all_qs.extend(test_data.get('questions', []))
        scraped_data = all_qs

    transformed = {}

    for idx, q in enumerate(scraped_data):
        # Decode answers and clean question data
        q = clean_question(q)
        
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
        transformed_q = process_question(q, idx, test_obj)

        test_obj['sections'][0]['questions'].append(transformed_q)
        test_obj['total_qs'] = len(test_obj['sections'][0]['questions'])
        test_obj['total_marks'] += transformed_q['award']

    final_output = {sub: list(tests.values()) for sub, tests in transformed.items()}
    write_json(final_output, output_path)

    print(f"Successfully transformed data and saved to {output_path}")

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.normpath(os.path.join(current_dir, "../scraped_data/all_tests_questions.json"))
    output_file = os.path.normpath(os.path.join(current_dir, "../scraped_data/final_data.json"))
    
    transform_data(input_file, output_file)
