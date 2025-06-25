# Issue 202: Fix Transliterator Transform IDs

## Problem
Some transliterator transform IDs are not working correctly with ICU:
- "Russian-Latin" should be "Cyrillic-Latin"
- Some transforms like "Han-Latin" may not be available in all ICU builds
- Need better error handling and documentation of available transforms

## Tasks
1. Create a function to list available transliterator IDs
2. Document commonly used transform IDs
3. Add fallback handling for missing transforms
4. Update examples to use only widely-available transforms
5. Add validation for transform IDs before creating transliterators

## Test Cases
- Test all example transforms work on common ICU installations
- Verify error messages are helpful when transforms are unavailable
- Ensure the list of available transforms is accessible to users