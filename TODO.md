# TODO - uicu v1.0 MVP

## 🎯 Focus: Fast, Reliable, Essential Unicode Operations

## ✅ Already Completed

### Phase 1: Critical Fixes
- [x] Fix or remove DateTimeFormatter.parse() method (never implemented, no action needed)
- [x] Fix transliterator transform IDs (added find_transforms() helper)
- [x] Fix Char class to handle multi-codepoint strings (documented limitation, improved error messages)
- [x] Remove all TODO stub comments from format.py (none found)

### Phase 2: Code Cleanup
- [x] Simplify exception handling - removed excessive try-except wrapping
- [x] Let ICU exceptions bubble up with original context
- [x] Clean up verbose docstrings (removed parameter type repetition)
- [x] Optimize imports - conditional imports all well-justified
- [x] Make demo script non-interactive (already was non-interactive)
- [x] Remove hardcoded category mappings from demo

## 🎯 Current Tasks

### Phase 3: API Simplification ✅ COMPLETE
- [x] Consolidate duplicate validation code
- [x] Reduce custom exceptions usage (removed unnecessary wrapping)
- [x] Remove field position tracking stubs
- [ ] Move constants inline where appropriate
- [ ] Make internal classes private (_prefixed)

### Phase 4: Documentation & Testing
- [ ] Set up Sphinx with modern theme (Furo)
- [ ] Auto-generate API documentation from docstrings
- [ ] Write user guides for common use cases
- [ ] Create cookbook with real-world examples
- [ ] Set up automatic deployment to GitHub Pages
- [ ] Update tests for streamlined API
- [ ] Remove tests for deleted features
- [ ] Update README for v1.0 features
- [ ] Create migration guide from v0.2 to v1.0
- [ ] Final performance testing

## 📏 Success Criteria for v1.0

### Metrics
- [ ] Test coverage: >95%
- [ ] Import time: <100ms
- [ ] Package size: <100KB
- [ ] Core code lines: <2000
- [ ] PyICU overhead: <5%
- [ ] Working features: 100%

### Code Quality
- [ ] Exception classes reduced to 3
- [ ] Import complexity reduced
- [ ] Docstring verbosity reduced by 40%
- [ ] Validation duplication eliminated
- [ ] Dead code eliminated

## 🚫 Deferred to v2.0

**Not implementing in v1.0:**
- NumberFormatter
- ListFormatter
- MessageFormatter
- Field position tracking
- Relative time formatting
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

**Philosophy**: Ship a small, fast, reliable v1.0 that excels at core Unicode operations.