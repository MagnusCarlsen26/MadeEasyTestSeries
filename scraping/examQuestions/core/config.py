# Standard headers for ThinkExam API
DEFAULT_HEADERS = {
    "accept": "application/json, text/javascript, */*; q=0.01",
    "accept-language": "en-US,en;q=0.5",
    "cache-control": "no-cache",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "pragma": "no-cache",
    "priority": "u=0, i",
    "sec-ch-ua": '"Brave";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Linux"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "sec-gpc": "1",
    "Referer": "https://ots2026.onlinetestseriesmadeeasy.in/"
}

# Initial token from a fresh login
INITIAL_TOKEN = "W0n4i4pj+w40sULY6j5o2qQqIyG2HoGZHk+oi+08V1pjyvLzubRRih87yQzCBWVi5GIVgi+on8mC*k85ogE9k89W4*XHeTbNaMenpsTQFk4vnz0FyPY3v6m9HLRNd+I1KNUKg3NOeC*CwnqTWY3RryY2UQN82wEV43euEQ5j4bDOt7owYiKUu28X6Xju9dP8lNwFQWR63lRenPr89Z6IdpYF6F*ATwy6vceI*Tcj9AaGprAjjIFU9bYY*TsS7SMZJi4Xa1aEOBfT50RVMamtxhQ8miQhofTy5prsixmhgYwhtCfy6jB98*so5YlmQ6KpdqvNTIZuB88Y0n3Ytu0NbIREqu44*fHG1p7QPyAyIkCDJazOlcz0mKff3Y4mfj+ejoC8L32jJEZROf8Pe1R7TWrhCqZcRUigETOaHR99QwQEh2jeJQHXjzePZG939+tR3CX83ILUwAu+1HIqdwEqiEMdy4OEp9AfCzQP0NahVEXnk3xHIF0sGWLRTfG*QyPYLmp3Zc1pn0ic5BnIXPnSXA=="

# Mapping for encrypted MCQ answers
MCQ_MAPPING = {
    "Dsdj/LJX8pBs6q+b96fwiQ==": "Option 1",
    "fhPK/WKkcuYMengj9uY6cg==": "Option 2",
    "9m/iwvJKC6coEJr5HJJczQ==": "Option 3",
    "Wkw/v0ACIC+JhZVbmq0HcA==": "Option 4",
    # Alternative format observed in some scripts
    'RKlBTlNXRVI=': 'Option 1',
    'QktBTlNXRVI=': 'Option 2', 
    'Q0tBTlNXRVI=': 'Option 3',
    'REtBTlNXRVI=': 'Option 4'
}

# Fields to remove to keep JSON files slim
GARBAGE_FIELDS = [
    "LABEL_1", "LABEL_2", "fldUnit", "IS_IMAGE_TYPE", "IS_COMPILER", 
    "IS_RECORDER", "TEST_CASE_TYPE", "fldTextAreaEnable", "ESSAY_SORT", 
    "SORTING_OPTIONS", "OPTION_LABEL", "FREE_SPACE", "ESSAY_TIME", 
    "MINIMUM_QUE_TIME", "isAnswerFileUpload", "MAX_OPT_LIMIT", "TIME", 
    "ESSAY_SORT_H", "SORTING_OPTIONS_H", "TEST_CASE_TYPE_H", "OPTION_LABEL_H",
    "DIFFCULTY_NAME", "ANSWER_TYPE"
]

GARBAGE_ENGLISH_FIELDS = [
    "SOLUTION", "ESSAY_ID", "EASSY_DETAILS", "ESSAY_NAME"
]

# Subject mapping for data transformation
SUBJECT_MAPPING = {
    "Theory of Computation": "Theory of Computation",
    "Algorithms": "Algorithms",
    "Computer Organization and Architecture": "Computer Organization and Architecture",
    "Operating System": "Operating Systems",
    "Engineering Mathematics": "Engineering Mathematics",
    "General Aptitude": "General Aptitude",
    "Database": "Databases & DBMS",
    "DBMS": "Databases & DBMS",
    "Programming and Data Structures": "Programming & DS",
    "Computer Networks": "Computer Networks",
    "Digital Logic": "Digital Logic",
    "Discrete Mathematics": "Discrete Mathematics",
    "Compiler Design": "Compiler Design",
}
