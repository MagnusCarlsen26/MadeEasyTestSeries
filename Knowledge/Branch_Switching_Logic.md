# Branch Discovery and Switching Logic

## Overview
The MadeEasy/ThinkExam API does not use explicit branch identifiers (like `branch=CS` or `branch=CH`) in the request parameters or body for common discovery endpoints such as `getPackageDetail`. Instead, the branch context is entirely determined by the session state.

## Available Engineering Branches
The MadeEasy Online Test Series (GATE 2026) covers the following branches:
- **CE**: Civil Engineering
- **ME**: Mechanical Engineering
- **EE**: Electrical Engineering
- **EC**: Electronics & Communication Engineering
- **CS & IT**: Computer Science & IT
- **IN**: Instrumentation Engineering
- **PI**: Production & Industrial Engineering
- **CH**: Chemical Engineering
- **DA**: Data Science and Artificial Intelligence

## Discovery Probing Results
Previously, a "Hard Session Lock" was suspected, implying that branch switching required capturing separate authorization tokens for each branch. However, deeper analysis revealed that the branch context is actually controlled by the `courseId` field in the user's personal profile.

### 1. Dynamic Branch Switching
The branch context can be programmatically pivoted for a single session without capturing new tokens.
- **Mechanism**: Sending a `POST` request to `setPersonalInfo` with a target `courseId` updates the account's branch context on the server side.
- **Persistence**: Once updated, all subsequent calls to `getPackageDetail` (using the same authorization headers) return tests for that specific branch.
- **Zero-Token Captures**: This allows for complete discovery of all disciplines using only a single valid session.

### 2. Discovered Course IDs
The following `courseId` values have been mapped to their respective engineering disciplines:

| Branch Name | Course ID |
|-------------|------------|
| Civil Engineering | 1427490 |
| Mechanical Engineering | 1427491 |
| Electrical Engineering | 1427492 |
| Electronics Engineering | 1427493 |
| Computer Science Engineering | 1427494 |
| Instrumentation Engineering | 1427495 |
| Production & Industrial Engineering | 1427496 |
| Chemical Engineering | 1427497 |
| DS & AI | 1427498 |

## Discovered Scope
Using the dynamic switching script (`discovery/stream_discovery.py`), the following catalog has been extracted for the GATE 2026/2025 series:

- **All 9 Branches Discovered**: Every branch listed above has exactly 4 major packages identified (Mock, Practice, Full Syllabus, and Combo).
- **Consolidated Data**: Full details, including `packageId` and individual `testId` arrays, are stored in `scraping/discovery/all_branches_data.json`.
- **Total Catalog Size**: Discovery confirms a massive database across all disciplines, now fully mapped.

## Summary for Scaling
To scale discovery or scraping to any branch:
1. **Dynamic Shift**: Run the discovery script to pivot the `courseId`.
2. **Catalog Fetch**: Call `getPackageDetail` to get the latest list of `packageId` and `testId`.
3. **Download**: Use the extracted `testId` list to batch-download questions using the core scraping engine.
