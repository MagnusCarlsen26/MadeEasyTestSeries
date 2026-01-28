import os
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.join(script_dir, "..")
sys.path.append(root_dir)

from utils.io_utils import read_json, ensure_dir

def get_status():
    scraped_data_dir = os.path.join(root_dir, "scraped_data")
    test_ids_path = os.path.join(scraped_data_dir, "test_ids.json")
    raw_dir = os.path.join(scraped_data_dir, "raw")
    images_dir = os.path.join(scraped_data_dir, "images")
    report_path = os.path.join(scraped_data_dir, "status.txt")
    
    # Transformed data is in the scraped_data directory now
    web_data_path = os.path.join(scraped_data_dir, "final_data.json")

    if not os.path.exists(test_ids_path):
        print(f"Error: {test_ids_path} not found.")
        return

    # 1. Analyze Tests
    test_ids_data = read_json(test_ids_path)
    total_tests = len(test_ids_data)
    downloaded_tests = 0
    missing_tests = []

    if os.path.exists(raw_dir):
        for entry in test_ids_data:
            test_id = entry['testId']
            # Reproduce the filename logic from downloadExamQuestions.py
            safe_test_id = test_id.replace('/', '_').replace('+', '-')
            expected_file = os.path.join(raw_dir, f"{safe_test_id}.json")
            
            if os.path.exists(expected_file):
                downloaded_tests += 1
            else:
                missing_tests.append(entry['testName'])
    
    test_progress = (downloaded_tests / total_tests * 100) if total_tests > 0 else 0

    # 2. Analyze Images
    total_images = 0
    if os.path.exists(images_dir):
        total_images = len([f for f in os.listdir(images_dir) if os.path.isfile(os.path.join(images_dir, f))])

    # 3. Check Transformed Data
    transformed_status = "Missing"
    if os.path.exists(web_data_path):
        size_kb = os.path.getsize(web_data_path) / 1024
        transformed_status = f"Present ({size_kb:.2f} KB)"

    # 4. Generate Report
    lines = [
        "========================================",
        "          SCRAPING STATUS REPORT        ",
        "========================================",
        f"Total Tests (Goal)    : {total_tests}",
        f"Tests Cached (Done)   : {downloaded_tests}",
        f"Tests Pending         : {total_tests - downloaded_tests}",
        f"Progress              : {test_progress:.2f}%",
        "----------------------------------------",
        f"Total Images Cached   : {total_images}",
        "========================================",
        "          DATA LOCATIONS                ",
        "========================================",
        f"Transformed Output    : {web_data_path}",
        f"   -> Status          : {transformed_status}",
        "----------------------------------------",
        f"Raw Cache Directory   : {raw_dir}",
        f"Images Directory      : {images_dir}",
        "========================================"
    ]

    report_content = "\n".join(lines)
    print(report_content)
    
    ensure_dir(report_path)
    with open(report_path, "w") as f:
        f.write(report_content)
    print(f"\n[+] Status report updated at {report_path}")

if __name__ == "__main__":
    get_status()
