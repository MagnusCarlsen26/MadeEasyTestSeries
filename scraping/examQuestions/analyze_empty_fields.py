import json
import os
from collections import defaultdict

def analyze_json_files(base_dir):
    files = []
    for root, dirs, filenames in os.walk(base_dir):
        for f in filenames:
            if f == 'questions.json':
                files.append(os.path.join(root, f))
    
    field_counts = defaultdict(int)
    field_empty_zero_counts = defaultdict(int)
    total_questions = 0

    for file_path in files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            for key, value in data.items():
                if key.startswith('qu') and isinstance(value, dict):
                    total_questions += 1
                    analyze_dict(value, field_counts, field_empty_zero_counts)
        except Exception as e:
            print(f"Error processing {file_path}: {e}")

    # Report fields that are empty or zero in more than, say, 50% of cases
    print(f"Total Questions Analyzed: {total_questions}")
    print(f"{'Field Name':<30} | {'Empty/Zero %':<15} | {'Count'}")
    print("-" * 60)
    
    # Sort by percentage
    results = []
    for field in field_counts:
        percentage = (field_empty_zero_counts[field] / field_counts[field]) * 100
        results.append((field, percentage, field_empty_zero_counts[field]))
    
    results.sort(key=lambda x: x[1], reverse=True)
    
    for field, percentage, count in results:
        if percentage > 0:
            print(f"{field:<30} | {percentage:>14.2f}% | {count}")

def analyze_dict(d, field_counts, field_empty_zero_counts, prefix=''):
    for k, v in d.items():
        field_name = f"{prefix}{k}"
        field_counts[field_name] += 1
        
        if v == "" or v == "0" or v == 0:
            field_empty_zero_counts[field_name] += 1
        
        if isinstance(v, dict):
            analyze_dict(v, field_counts, field_empty_zero_counts, prefix=f"{field_name}->")

if __name__ == "__main__":
    analyze_json_files('/home/khushal/Desktop/Projects/MadeEasyTestSeries/scraping/examQuestions/data/')
