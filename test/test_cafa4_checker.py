import os
import pytest
from cafa4_format_checker import cafa_checker

'''
The tests are intended to be run with pytest (pip install pytest)

From the project root directory (parent directory of the test directory), run pytest with python's module syntax:
python -m pytest
or to run a single test (where test_valid_DO_lines is the example test):
python -m pytest test/test_DO.py::test_valid_DO_lines -v

'''

@pytest.fixture(scope="module")
def test_data_path():
    ''' Provides a single, consistent absolute path to the test_data directory across environments '''
    root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return "{}/test/test_data/end_to_end_data/".format(root_path)


def test_basic_do_txt_file(test_data_path, capfd):
    filepath = "{}valid/ateam_1_do.txt".format(test_data_path)
    is_valid = cafa_checker(filepath)
    # Capture print statements to stdout
    output, error = capfd.readouterr()
    assert is_valid is True
    assert "Files correctly formatted" in output
    assert "passed the CAFA 4 DO prediction format checker" in output


def test_basic_go_txt_file(test_data_path, capfd):
    filepath = "{}valid/ateam_1_go.txt".format(test_data_path)
    is_valid = cafa_checker(filepath)
    # Capture print statements to stdout
    output, error = capfd.readouterr()
    assert is_valid is True
    assert "Files correctly formatted" in output


