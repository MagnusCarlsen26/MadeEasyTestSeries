# Test ID Pattern Analysis

## Overview
The MadeEasy test series uses sequential numeric IDs (Base64 encoded). Analysis reveals clear patterns in how tests were created and organized across different engineering branches.

## Computer Science (CS) Test ID Ranges

### Early Phase Batch (April 2025)
**Range**: `6433115` - `6435005`
- **6433115**: GATE 2026 DEMO TEST CS (oldest test)
- **6434994-6435005**: Topicwise Tests 1-10
  - Small gaps exist (6434995, 6435001) suggesting deleted/reserved tests
  - These were created months before the main batch

### Main Batch (Bulk Release)
**Range**: `6464583` - `6464620` (38 tests, perfectly sequential)

This massive batch was released in a single automated deployment:

| Sub-Range | Test Type | Count |
|-----------|-----------|-------|
| `6464583-6464596` | Topicwise 11-24 | 14 |
| `6464597-6464608` | Subjectwise 1-12 | 12 |
| `6464609-6464612` | Basic Level Full Syllabus | 4 |
| `6464613-6464616` | Advance Level Full Syllabus | 4 |
| `6464617-6464620` | Mock Level Full Syllabus | 4 |

**Key Insight**: Zero gaps in this range indicates a single bulk creation event.

## Multi-Branch Pattern Discovery

### Hidden Tests Discovery
While probing for missing CS tests, **25 additional test IDs** were discovered that are NOT listed in the original `test_ids.json`:

#### Before CS Block: Instrumentation Engineering (IN)
**IDs**: `6464563` - `6464572` (10 tests)
- **Question Count**: 65 questions per test (full-length format)
- **Subject**: General Aptitude
- **Topic**: INSTRUMENTATION ENGINEERING
- **Status**: Not visible in CS student dashboard but accessible via API

**Complete List**:
```
6464563, 6464564, 6464565, 6464566, 6464567,
6464568, 6464569, 6464570, 6464571, 6464572
```

#### After CS Block: Electrical Engineering (EE)
**IDs**: `6464621` - `6464640` (15 tests)
- **Question Count**: 17 questions per test (topicwise format)
- **Subject**: Technical
- **Topic**: ELECTRICAL ENGINEERING
- **Status**: Not visible in CS student dashboard but accessible via API

**Complete List**:
```
6464621, 6464622, 6464623, 6464624, 6464625,
6464626, 6464627, 6464628, 6464629, 6464630,
6464631, 6464632, 6464633, 6464634, 6464635,
6464636, 6464637, 6464638, 6464639, 6464640
```

### The Complete ID Sequence
The full sequential pattern across all branches:

```
6464563-6464572  → Instrumentation Engineering (IN) - 10 full-length tests
6464573-6464582  → [Unknown branch - not yet probed]
6464583-6464620  → Computer Science (CS) - 38 tests (YOUR TESTS)
6464621-6464640  → Electrical Engineering (EE) - 15 topicwise tests
6464641+         → [Unknown - not yet probed]
```

### Subject Identification Method
Tests can be identified by examining their question metadata, which includes subject and topic information that clearly indicates the engineering branch.

### Why These Tests Are Hidden
- **Dashboard Filtering**: The student dashboard only shows tests matching your enrolled branch (CS)
- **API Access**: The raw API returns question data for ANY valid test ID regardless of branch
- **Implication**: There are likely hundreds of additional tests for ME, CE, EC, CH, etc. in the database

## The 29,000 ID Gap

**Gap**: Between `6435005` (Topicwise 10) and `6464583` (Topicwise 11)
- **Size**: 29,578 IDs
- **Hypothesis**: This gap likely contains tests for other engineering branches (ME, CE, EC, etc.) created during the interim period
- **Implication**: CS tests 1-10 were created in early phase, while tests 11+ were part of a later multi-branch rollout

## Chronological Development Timeline

1. **Phase 1 (Early 2025)**: Demo test created (`6433115`)
2. **Phase 2 (April 2025)**: First 10 Topicwise CS tests (`6434994-6435005`)
3. **Phase 3 (Later)**: Massive multi-branch deployment
   - All remaining CS tests (Topicwise 11-24, Subjectwise, Full-Length)
   - IN, EE, and likely other branch tests
   - All created in tight sequential blocks

## Practical Implications

### For Scraping
- The current `test_ids.json` contains only CS tests
- Additional CS tests are unlikely to exist outside known ranges
- The 29k gap primarily contains other engineering branches

### For ID Prediction
- Within a test category, IDs are perfectly sequential
- Missing IDs in early batches (6434995, 6435001) are likely permanently deleted
- New CS tests would likely be added after `6464620`

## Data Files
- **test_ids.json**: All 49 CS tests (sorted by decoded ID)
- **decoded_test_ids.txt**: Human-readable list of IDs and names
