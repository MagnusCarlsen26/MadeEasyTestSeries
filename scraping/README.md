# MadeEasy Test Series Scraper

## Overview

This scraping pipeline downloads exam questions and associated images from the MadeEasy online test series platform. The system is designed with ethical scraping principles, using sequential processing and rate limiting to minimize server load.

## Architecture

### Pipeline Stages

The scraping process consists of three sequential stages orchestrated by `main.py`:

1. **Question Download** - Fetches exam question data from the API
2. **Data Processing** - Transforms and cleans the raw question data
3. **Image Download** - Downloads all images referenced in questions

After completion, a status report is generated showing progress and data locations.

## Stage Details

### Stage 1: Question Download

**Script**: `scripts/downloadExamQuestions.py`

**Process**:
1. Reads test IDs from `scraped_data/test_ids.json`
2. For each test, makes API call to fetch question data
3. Saves individual test data to `scraped_data/raw/{test_id}.json`
4. Merges all tests into `scraped_data/all_tests_questions.json`
- Authentication: Token-based (configured in `utils/config.py`)

### Stage 2: Data Processing

**Script**: `scripts/process_data.py`

**Process**:
1. Reads `scraped_data/all_tests_questions.json`
2. Extracts and cleans each question
3. Decodes encrypted answers
4. Categorizes by subject
5. Removes garbage fields
6. Saves to `scraped_data/final_data.json`

**Transformations**:
- **Answer Decryption**: Converts encrypted answer hashes to readable format (e.g., "Option 1")
- **Subject Mapping**: Standardizes subject names using `SUBJECT_MAPPING`
- **Field Cleanup**: Removes Hindi content and unnecessary metadata
- **Structure Normalization**: Flattens nested structures for easier consumption

**Output Format**: Array of cleaned question objects ready for web application use

### Stage 3: Image Download

**Script**: `scripts/download_images.py`

**Process**:
1. Scans `all_tests_questions.json` for image URLs in questions and solutions
2. Extracts unique image links to `extracted_image_links.txt`
3. Downloads each image sequentially to `scraped_data/images/`
4. Uses URL-based or hash-based filenames

**Image Sources**: Questions, options, solutions, and explanations

## Usage

### Running the Full Pipeline

```bash
python main.py
```

This executes all three stages sequentially and generates a status report.

### Running Individual Stages

Each stage can be run independently:

```bash
python scripts/downloadExamQuestions.py
python scripts/process_data.py
python scripts/download_images.py
python scripts/status.py
```

### Input Requirements

**Required**: `scraped_data/test_ids.json`

This file must contain an array of test objects with:
- `testId`: Base64-encoded test identifier
- `testName`: Human-readable test name
- `testType`: Category (e.g., "Topicwise", "Full Length")
- `subject`: Subject name (optional)

## Configuration

### Core Settings (`utils/config.py`)

**API Configuration**:
- `INITIAL_TOKEN`: Authentication token

**Data Cleaning**:
- `GARBAGE_FIELDS`: Fields to remove from questions
- `GARBAGE_ENGLISH_FIELDS`: Additional English-specific fields to remove
- `MCQ_MAPPING`: Encrypted answer to readable option mapping
- `SUBJECT_MAPPING`: Subject name standardization
- `RATE_LIMIT_DELAY`: Delay between requests (default: 0.5 seconds)

## Status Reporting

The status reporter (`scripts/status.py`) provides:

## Error Handling

### Resumability

All stages support resumability:
- **Questions**: Checks if `raw/{test_id}.json` exists before downloading
- **Images**: Checks if image file exists before downloading
- **Processing**: Can be re-run without side effects (overwrites output)

### Failure Modes

- **API errors**: Logged and counted as FAILED, pipeline continues
- **Network timeouts**: 30-second timeout for questions, 10-second for images
- **Missing files**: `io_utils.py` raises `FileNotFoundError` for explicit error handling

## Data Flow

```
test_ids.json
    ↓
[API Calls] → raw/{test_id}.json (per test)
    ↓
[Merge] → all_tests_questions.json
    ↓
[Transform] → final_data.json
    ↓
[Extract URLs] → extracted_image_links.txt
    ↓
[Download] → images/*.png
```

### Common Issues

**"API Error for {test_id}"**
- Check token validity in `utils/config.py`

**"Images not downloading"**
- Ensure Stage 1 completed successfully
- Check `extracted_image_links.txt` for valid URLs

**"Slow download speeds"**
- Expected with rate limiting (500ms delay)
- Adjust `RATE_LIMIT_DELAY` if appropriate