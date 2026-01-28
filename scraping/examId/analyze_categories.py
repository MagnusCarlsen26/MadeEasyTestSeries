import json

def analyze_data_json(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    
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
