import os
from collections import Counter
import pytest
from cafa4_format_checker import cafa_checker

'''
The tests are intended to be run with pytest (pip install pytest)

From the project root directory (parent directory of the test directory), run pytest with python's module syntax:
python -m pytest

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

def test_mixed_predictions_zip_file(test_data_path, capfd):
    filepath = "{}invalid/mixed_predictions.zip".format(test_data_path)
    is_valid = cafa_checker(filepath)
    # Capture print statements to stdout
    output, error = capfd.readouterr()

    assert is_valid is False
    #assert "Files correctly formatted" in output
    assert "VALIDATION FAILED" in output
    assert "Only one team is allowed per zipfile" in output

    # The zip file contains 7 files, so the word "passed"
    # should appear 7 times in stdout:
    #counter = Counter(output.split())
    #assert counter['passed'] == 7
    #assert error == ""


def test_go_and_do_zip_file(test_data_path, capfd):
    filepath = "{}valid/go_and_do.zip".format(test_data_path)
    is_valid = cafa_checker(filepath)
    # Capture print statements to stdout
    output, error = capfd.readouterr()
    assert is_valid is True
    assert error == ""
    assert "Files correctly formatted" in output
    assert "ateam_1_do.txt, passed the CAFA 4 DO prediction format checker" in output
    assert "ateam_1_go.txt, passed the CAFA 4 GO prediction format checker" in output


def test_invalid_term_centric_zip(test_data_path, capfd):
    filepath = "{}invalid/term_centric_test_predictions.zip".format(test_data_path)
    is_valid = cafa_checker(filepath)
    # Capture print statements to stdout
    output, error = capfd.readouterr()
    assert is_valid is False


def test_invalid_protein_centric_zip(test_data_path, capfd):
    filepath = "{}invalid/protein_centric_test_predictions.zip".format(test_data_path)
    is_valid = cafa_checker(filepath)
    # Capture print statements to stdout
    output, error = capfd.readouterr()
    assert is_valid is False


def test_invalid_binding_site_zip(test_data_path, capfd):
    filepath = "{}invalid/binding_site_test_predictions.zip".format(test_data_path)
    is_valid = cafa_checker(filepath)
    # Capture print statements to stdout
    output, error = capfd.readouterr()
    assert is_valid is False


