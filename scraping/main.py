import os
import sys

root_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(root_dir)

from scripts.downloadExamQuestions import run_exam_download
from scripts.process_data import transform_data
from scripts.download_images import run_image_download
from scripts.status import get_status
from utils.io_utils import ensure_dir

def main():
    scraped_data_dir = os.path.join(root_dir, "scraped_data")
    ensure_dir(scraped_data_dir)

    test_ids_path = os.path.join(scraped_data_dir, "test_ids.json")
    all_qs_path = os.path.join(scraped_data_dir, "all_tests_questions.json")
    images_dir = os.path.join(scraped_data_dir, "images")
    web_data_path = os.path.join(scraped_data_dir, "final_data.json")

    print("\n=== STAGE 1: Downloading Questions ===")
    run_exam_download(test_ids_path, scraped_data_dir)

    print("\n=== STAGE 2: Processing Data ===")
    transform_data(all_qs_path, web_data_path)

    print("\n=== STAGE 3: Downloading Images ===")
    run_image_download(all_qs_path, images_dir)

    print("\n=== STATUS ===")
    get_status()

if __name__ == "__main__":
    main()

