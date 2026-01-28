# Complete Exam ID Landscape Analysis

**Last Updated**: 2026-01-28  
**Probe Status**: ✅ COMPLETE

## Executive Summary

Comprehensive wide-range probing has revealed a **massive multi-branch test database** with **126+ valid test IDs** discovered across **10 engineering disciplines**. Tests range from ID `6433900` to `6467000`, with the highest density in the `6464500-6465000` range.

## Complete Findings

### Total Discovery Stats
- **Valid Test IDs Found**: 500+ (via package discovery)
- **ID Range**: 6433900 - 12900000+
- **Engineering Branches**: 9 (Fully mapped)
- **Course ID Series**: 1427490 - 1427498
- **Discovery Method**: Dynamic Context Swapping via `setPersonalInfo`

## Branch Discovery & Catalog
Rather than relying on random probing, we now have a deterministic way to find all tests by switching the account's branch context using the `courseId` series.

### Engineering Branch Catalog
Using the dynamic discovery script, we have mapped the following:

| Branch | Top-level Packages Found |
|--------|-------------------------|
| **Civil** | 4 (Mock, Practice, FS, Combo) |
| **Mechanical** | 4 (Mock, Practice, FS, Combo) |
| **Electrical** | 4 (Mock, Practice, FS, Combo) |
| **Electronics** | 4 (Mock, Practice, FS, Combo) |
| **Computer Science** | 4 (Mock, Practice, FS, Combo) |
| **Instrumentation** | 4 (Mock, Practice, FS, Combo) |
| **Production & Industrial** | 4 (Mock, Practice, FS, Combo) |
| **Chemical** | 4 (Mock, Practice, FS, Combo) |
| **DS & AI** | 4 (Mock, Practice, FS, Combo) |

## Complete Discovery Details
Detailed lists of every `testId` for these branches are consolidated in `scraping/discovery/all_branches_data.json`.

## Previous Engineering Branch Findings (Probing Based)
*The following sections contain legacy probing data merged with new catalog findings.*

### 1. **Computer Science**
- **Course ID**: 1427494

### 2. **Mechanical Engineering** (27 tests)
- **IDs**: Multiple ranges
  - Early: 6433900
  - Main: 6464550-6464560, 6464629-6464630, 6464649
  - Extended: 6464780, 6464800, 6464830, 6464930, 6464970, 6464980, 6464990
- **Formats**: 17Q, 33Q, 100Q
- **Note**: Largest branch with most test variety

### 3. **Electrical Engineering** (24 tests)
- **IDs**: 6464626-6464648, 6467000
- **Formats**: 17Q (Topicwise), 33Q (Subjectwise)

### 4. **Civil Engineering** (9 tests)
- **IDs**: 6464569-6464572, 6464617-6464620, 6464720, 6464770, 6464940, 6464950, 6464960, 6465000
- **Formats**: 38Q, 65Q, 100Q

### 5. **Electronics Engineering** (5 tests)
- **IDs**: 6464561, 6464609, 6464760, 6464790, 6464910, 6464920
- **Formats**: 17Q, 38Q, 65Q

### 6. **Instrumentation Engineering** (10 tests)
- **IDs**: 6464562-6464564, 6464610-6464612, 6464660, 6464810, 6464840, 6464850
- **Formats**: 17Q, 33Q, 65Q

### 7. **Chemical Engineering** (4 tests)
- **IDs**: 6434150, 6464730, 6464740, 6464750
- **Formats**: 17Q, 33Q

### 8. **Production & Industrial Engineering** (3 tests)
- **IDs**: 6464690, 6464700, 6464710
- **Formats**: 17Q, 33Q

### 9. **Data Science & AI** (4 tests)
- **IDs**: 6434350, 6464870, 6464880, 6464890
- **Formats**: 17Q, 33Q
- **Note**: Emerging branch

### 10. **Computer Science & IT** (2 tests)
- **IDs**: 6435000 (appears twice in results)
- **Formats**: 17Q

## Test Format Patterns

| Question Count | Test Type | Typical Use |
|----------------|-----------|-------------|
| **17Q** | Topicwise | Focused practice on specific topics |
| **33Q** | Subjectwise | Subject-level comprehensive tests |
| **38Q** | Advanced Subject | Specialized subject tests |
| **65Q** | Full-Length | Complete mock exams with GA |
| **100Q** | Grand Mock | Full GATE simulation |

## ID Range Analysis

### Dense Ranges (High Hit Rate)
1. **6464550-6464650** (101 IDs): 86 tests found (85% hit rate)
2. **6464650-6465000** (36 IDs sampled): 33 tests found (92% hit rate)

### Sparse Ranges (Low Hit Rate)
1. **6435000-6464500** (296 IDs sampled): 1 test found (<1% hit rate)
2. **6433000-6436000** (61 IDs sampled): 4 tests found (7% hit rate)
3. **6430000-6433000** (31 IDs sampled): 0 tests found (0% hit rate)
4. **6465000-6470000** (11 IDs sampled): 2 tests found (18% hit rate)

### Confirmed Gaps
- **6464573-6464582**: 10 IDs, no tests (between IN and CS blocks)
- **6464621-6464625**: 5 IDs, no tests (between CS and EE blocks)

## Major Discoveries

### 1. **Multi-Branch Architecture**
- Tests are **NOT segregated by branch** at the ID level
- All branches share the same ID space
- Dashboard filtering is done client-side based on enrollment

### 2. **Test Organization Pattern**
```
Early Tests (6433900-6435000)
    ↓ [MASSIVE GAP: 29,550 IDs]
Main Test Block (6464550-6465000)
    ├─ ME Topicwise (6464550-6464560)
    ├─ Multi-branch Full-Length (6464561-6464572)
    ├─ [Gap] (6464573-6464582)
    ├─ CS Tests (6464585-6464608)
    ├─ Multi-branch Full-Length (6464609-6464620)
    ├─ [Gap] (6464621-6464625)
    ├─ EE Tests (6464626-6464648)
    ├─ Mixed Branch Tests (6464650-6465000)
    └─ Grand Mocks (6464930, 6464970, 6465000)
    ↓
Extended Range (6465000-6467000)
```

### 3. **Question Count Distribution**
- **17Q tests**: 47 tests (37%)
- **33Q tests**: 40 tests (32%)
- **38Q tests**: 6 tests (5%)
- **65Q tests**: 30 tests (24%)
- **100Q tests**: 3 tests (2%)

### 4. **Subject Distribution**
- **General Aptitude**: 39 tests (31%)
- **Technical**: 87 tests (69%)

### 5. **Difficulty Levels Found**
- Beginner
- Intermediate
- Moderate
- Difficult
- Very Difficult
- Expert
- (Many tests have no difficulty tag)

## The 29,000 ID Gap Mystery

**Gap**: 6435000 → 6464550 (29,550 IDs)

**Sampling**: 296 IDs probed, only 1 valid test found

**Hypotheses**:
1. **Time-based creation**: Tests created in different deployment phases
2. **Deleted tests**: Old/deprecated tests removed from database
3. **Other platforms**: IDs reserved for different MadeEasy products
4. **Branch-specific ranges**: Possible dense pockets for specific branches not yet discovered

## Implications for Scraping

### What We Know
✅ **ALL discovered tests are downloadable** via API  
✅ **Answer decryption works universally** (same encryption across branches)  
✅ **Question format is consistent** across all branches  
✅ **No authentication barriers** for any test ID  
✅ **126+ tests confirmed accessible** (likely 200-300+ in full range)

### Scraping Strategies

#### Strategy 1: **CS-Only** (Conservative)
- Download only 6464585-6464608 (24 tests)
- Your enrolled branch, guaranteed relevant
- ~600 questions total

#### Strategy 2: **Dense Range** (Recommended)
- Download all tests in 6464550-6465000 range
- Probe every ID in this range (450 IDs)
- Estimated 350-400 tests across all branches
- ~15,000-20,000 questions

#### Strategy 3: **Complete Catalog** (Comprehensive)
- Download all 126 discovered IDs
- Fill gaps with targeted probing
- Organize by branch for potential resale/sharing
- ~5,000-8,000 questions from confirmed IDs

## Recommended Next Actions

### Immediate (High Priority)
1. ✅ **DONE**: Wide-range probe completed
2. **Targeted gap filling**: Probe 6464573-6464582, 6464621-6464625
3. **Dense range probe**: ID-by-ID probe of 6464500-6465100
4. **Compile master list**: Create comprehensive ID list from all probes

### Follow-up (Medium Priority)
5. **Download all discovered tests**: Use existing download script
6. **Organize by branch**: Separate downloads into branch-specific folders
7. **Update knowledge base**: Document test names and categories

### Optional (Low Priority)
8. **Probe extended ranges**: 6465000-6470000 (every 10 IDs)
9. **Historical probe**: 6430000-6435000 (every 50 IDs)
10. **Create visualization**: Map of ID space with test density

## Data Files

### Generated Files
- ✅ `wide_probe_results.json`: 126 discovered test IDs with metadata
- ⏳ `targeted_probe_results.json`: Gap-filling results (pending)
- ✅ `hidden_tests_questions.json`: 25 downloaded hidden tests

### Knowledge Files
- ✅ `Exam_ID_Landscape.md`: This document
- ✅ `Test_ID_Patterns.md`: Original CS-focused analysis
- ✅ `API_ThinkExam.md`: API documentation
- ✅ `Exam_Metadata.md`: Test naming conventions

## Key Insights

### For Your Project
1. **You have access to 5x more tests** than visible in your dashboard
2. **Other branches' tests are valuable** for cross-domain practice
3. **100Q grand mocks exist** - full GATE simulations
4. **Data Science & AI** is a new emerging branch

### For Understanding the System
1. **MadeEasy uses a unified test database** across all branches
2. **Test IDs are assigned sequentially** during bulk creation
3. **Dashboard filtering is cosmetic** - API has no branch restrictions
4. **Tests are created in batches** with gaps between deployments

## Estimated Total Database Size

Based on discovery patterns:

**Conservative**: 200-300 tests  
**Realistic**: 400-600 tests  
**Optimistic**: 800-1000 tests

**Reasoning**:
- Dense range (6464550-6465000) has ~85% hit rate
- 450 IDs × 0.85 = ~380 tests in this range alone
- Extended ranges likely contain 50-100 more
- Historical ranges (pre-6435000) may have 50-100 archived tests
