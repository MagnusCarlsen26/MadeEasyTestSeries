# Exam Name Parsing Rules

The naming convention of tests is parsed to categorize data for the Practice Portal.

## Test Types
- **Topicwise**: Identified by the keyword `Topicwise Test`. Logic strips trailing suffixes like `-1`, `-2` to group them by the actual subject name.
- **Subjectwise**: Identified by `Subjectwise Test`.
- **Full Syllabus**: Identified by `Full Syllabus`.

## Level Classification
For Full Syllabus tests, the difficulty levels are explicitly parsed:
- `Basic Level`
- `Mock Level`
- `Advance Level`

## Subject Extraction
Subject names are extracted by capturing the text following the `CS` (Computer Science) identifier in the string. Any numeric suffix (e.g., `Theory of Computation-1`) is normalized to the base subject.
