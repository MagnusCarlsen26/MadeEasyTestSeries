import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from io_utils import read_json

def analyze_data_json(file_path):
    data = read_json(file_path)
    
    test_list = data.get('data', [])
    categories = {}
    subcategories = {}
    
    for test in test_list:
        cat = test.get('testcategory')
        subcat = test.get('selectedSubCategory')
        
        categories[cat] = categories.get(cat, 0) + 1
        subcategories[subcat] = subcategories.get(subcat, 0) + 1
        
    print("Categories found:")
    for cat, count in categories.items():
        print(f"  {cat}: {count} tests")
        
    print("\nSubcategories found:")
    for subcat, count in subcategories.items():
        print(f"  {subcat}: {count} tests")

if __name__ == "__main__":
    analyze_data_json('/home/khushal/Desktop/Projects/MadeEasyTestSeries/scraping/examId/data.json')
