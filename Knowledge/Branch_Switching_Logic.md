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
Recent probing for a "Master Key" or branch bypass confirmed a strict **Hard Session Lock**.

### 1. Hard Session Lock Logic
The `authorization` and `custom-header` strings act as a mandatory context filter.
- **Failed Bypass**: Sending a specific `packageId` for Branch A (e.g., CS) while using an `authorization` token for Branch B (e.g., Chemical) results in the API returning the full list of Branch B packages, ignoring the specific ID.
- **Ignored Overrides**: Injecting `testcategory` or `categoryId` into the request body while on a mismatched session is completely ignored.
- **No Public Access**: The discovery endpoints require valid, branch-specific authorization headers. No public or generic data retrieval is possible.

### 2. Implementation & Context Swapping
Switching branches programmatically is achieved by **Context Swapping**: using an authorization token captured during a session on the specific branch portal. The API automatically pivots all its responses—including generic "package list" requests—to that branch's ecosystem.

## Discovered Scope
Through consolidated discovery using known tokens:
- **Chemical Engineering**: 4 Packages identified (Mock, Practice, Full Syllabus, Combo).
- **Computer Science**: 5 Packages identified (Mock, Practice, Full Syllabus, 2025/2026 Combos).

Full details including `testId` lists for these packages are stored in `scraping/discovery/all_branches_data.json`.

## Summary for Scaling
To scale discovery to remaining branches (ME, CE, EE, etc.):
1. **Header Capture is Mandatory**: Capture a legitimate request from the portal for each target branch.
2. **One Token per Branch**: A single captured session unlocks the entire `getPackageDetail` scope for that branch.
3. **testId Extraction**: Once the package details are fetched, the `testId` field provides a comma-separated list of all valid test IDs for that package.
