# Scraping Workspace Organization

## Directory Structure
- `/scraping/examId/`: Focused on fetching the high-level list of available exams and parsing their IDs/Metadata from `data.json`.
- `/scraping/examQuestions/`: Focused on deep-scraping the individual question data for each test ID.

## Processing Pipeline
1. **Extraction**: `extract_test_ids.py` parses `data.json` to generate `test_ids.json`.
2. **Scraping**: `main.py` uses the generated list to fetch detailed nested JSON for each test.
3. **Cleaning**: `clean_data.py` performs post-processing to strip out `HINDI` localization data and inject `READABLE_ANSWER` fields for easier frontend integration.
