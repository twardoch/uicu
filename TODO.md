# TODO - uicu v1.0 MVP

## 🎯 Focus: Fast, Reliable, Essential Unicode Operations

### ✅ Already Completed
- [x] Delete src/uicu/uicu.py (placeholder file removed)
- [x] Core Unicode functionality implemented (char, collate, segment, translit)
- [x] Locale management with BCP 47 support
- [x] Comprehensive demo script created
- [x] Clean up obsolete issue tracking (removed 5 deferred issues)

### 🔥 Phase 1: Critical Fixes (Week 1)

- [x] Fix or remove DateTimeFormatter.parse() method (Issue #102 - method never implemented, no action needed)
- [x] Fix transliterator transform IDs (Issue #202 - demo already uses correct IDs, added find_transforms() helper)
- [x] Fix Char class to handle multi-codepoint strings (documented limitation, improved error messages)
- [x] Remove all TODO stub comments from format.py (none found)

### ✅ Phase 2: Code Cleanup (Week 2) - COMPLETE

- [x] Simplify exception handling - removed excessive try-except wrapping
- [x] Let ICU exceptions bubble up with original context
- [x] Clean up verbose docstrings (removed parameter type repetition)
- [x] Optimize imports - conditional imports all well-justified, kept as-is
- [x] Make demo script non-interactive (already was non-interactive)
- [x] Remove hardcoded category mappings from demo

### 🎯 Phase 3: MVP Completion (Week 1-2: Critical Formatters)

- [ ] Implement NumberFormatter class in format.py
- [ ] Add decimal number formatting with locale-specific separators
- [ ] Add currency formatting with ISO 4217 currency codes
- [ ] Add percentage formatting with proper symbols
- [ ] Add scientific notation formatting
- [ ] Add compact notation (1.2K, 3.4M) formatting
- [ ] Add precision control (min/max digits)
- [ ] Add rounding mode support
- [ ] Add grouping separator control
- [ ] Add NumberFormatter tests for all locales and styles
- [ ] Implement ListFormatter class in format.py
- [ ] Add list type support (and, or, units)
- [ ] Add list style support (standard, short, narrow)
- [ ] Add proper 2-item vs 3+ item handling
- [ ] Add locale-specific conjunction handling
- [ ] Add ListFormatter tests for all locales and types
- [ ] Implement DateTimeFormatter.parse() method
- [ ] Add timezone parsing and conversion
- [ ] Add lenient vs strict parsing modes
- [ ] Add round-trip parsing tests

### 🎯 Phase 3: MVP Completion (Week 3: Documentation)

- [ ] Set up Sphinx documentation infrastructure
- [ ] Configure modern theme (Furo or sphinx-rtd-theme)
- [ ] Create API reference documentation
- [ ] Write quickstart guide
- [ ] Write Unicode basics guide
- [ ] Write locale usage guide
- [ ] Write performance guide
- [ ] Create migration guide from PyICU
- [ ] Create cookbook with real-world examples
- [ ] Set up automatic deployment to GitHub Pages
- [ ] Add documentation badges to README

### 🎯 Phase 3: MVP Completion (Week 4: Performance & Quality)

- [ ] Create performance benchmark infrastructure
- [ ] Add character operation benchmarks
- [ ] Add collation performance benchmarks
- [ ] Add segmentation speed benchmarks
- [ ] Add formatting operation benchmarks
- [ ] Add memory usage profiling
- [ ] Set up continuous benchmarking in CI
- [ ] Improve test coverage to >90%
- [ ] Add tests for NumberFormatter edge cases
- [ ] Add tests for ListFormatter edge cases
- [ ] Add tests for DateTimeFormatter parsing
- [ ] Add property-based testing with hypothesis
- [ ] Add long-running operation tests
- [ ] Add cross-platform compatibility tests

### 🎯 Phase 3: MVP Completion (Week 5-6: Polish & Release)

- [ ] Enhance Char class for multi-codepoint support
- [ ] Add grapheme cluster handling
- [ ] Add support for flag emojis and combining characters
- [ ] Review API consistency across modules
- [ ] Standardize naming conventions
- [ ] Standardize return type patterns
- [ ] Standardize parameter validation
- [ ] Improve error messages with helpful suggestions
- [ ] Add input validation before ICU calls
- [ ] Add graceful degradation for missing ICU features
- [ ] Set up proper version management with tags
- [ ] Complete package metadata in pyproject.toml
- [ ] Test distribution from TestPyPI
- [ ] Create release documentation
- [ ] Conduct security review of dependencies
- [ ] Prepare migration guides and breaking change docs

### 📏 Success Criteria for v1.0

- [ ] All core formatters implemented (Number, List, DateTime with parsing)
- [ ] >90% test coverage across all modules
- [ ] Zero critical bugs (no broken functionality)
- [ ] Professional documentation site with examples
- [ ] Performance benchmarks established (<5% PyICU overhead)
- [ ] <100ms import time
- [ ] <200KB package size
- [ ] Cross-platform compatibility verified
- [ ] Comprehensive examples and migration guides
- [ ] Clear error messages with suggestions

### 📏 Success Criteria for v1.0

- [ ] All shipped features work 100% correctly
- [ ] <5% performance overhead vs raw PyICU
- [ ] <2000 lines of core code
- [ ] <100ms import time
- [ ] >95% test coverage
- [ ] <100KB package size

## 🚫 Deferred to v2.0

**Not implementing in v1.0:**
- NumberFormatter (removed Issue #103)
- ListFormatter (removed Issue #104)
- MessageFormatter (removed Issue #105)
- Sphinx documentation (removed Issue #106)
- Performance benchmarks infrastructure (removed Issue #107)
- Property-based testing
- CI/CD pipeline
- Unicode regex support
- Advanced calendar systems

## ✨ v1.0 Feature Set

**Core Features (100% Working):**
1. **Character Properties** - Unicode character analysis
2. **Collation** - Locale-aware string comparison and sorting
3. **Segmentation** - Grapheme, word, sentence, line breaking
4. **Transliteration** - Script conversion and normalization
5. **Date Formatting** - Locale-aware date/time display (no parsing)
6. **Locale Management** - BCP 47 locale handling

**Quality Targets:**
- Zero broken features
- Minimal API surface
- Fast imports (<100ms)
- Clear error messages
- Small package (<100KB)

---

**Philosophy**: Ship a small, fast, reliable v1.0 that excels at core Unicode operations.