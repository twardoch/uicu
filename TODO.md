
## Objective

PyICU does not have a very pythonic API. I’d like us to make `uicu`, a very extensive, but mainly a natural, pythonic yet performant API (wrapper around PyICU), supplemented by fontTools.unicodedata if needed. The uciu API should expose rich, well-documented objects that naturally integrate with Python’s native Unicode but also expose rich additional functionality.

## Task 1

Research and meticulously document the various APIs supported by these packages

- https://fonttools.readthedocs.io/en/latest/unicodedata/index.html which includes info about writing systems but otherwise is based on https://github.com/fonttools/unicodedata2 which is like https://docs.python.org/3/library/unicodedata.html but uptodate
- https://pypi.org/project/pyicu/

Think, consult widely, and then make a very detailed, considerate plan for this new `uicu` package. Write a detailed spec that will guide a junior developer by hand allowing her to develop `uric`
