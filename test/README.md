
## Instructions for running tests

1. pytest is required: `pip install pytest`

2. from the project's base directory (ie parent of the test directory), 
run pytest using Python's module calling syntax: `python -m pytest`
3. Alternatively, verbose output is available via the verbose flag: 
`python -m pytest -v`
4. Individual test files can be run as well: 
`python -m pytest -v test/test_DO_prediction_checker.py`
5. And a single test function can be targeted as well:
`python -m pytest -v test/test_DO_metadata_checks.py::test_valid_author_str`
