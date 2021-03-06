import os
from collections import Counter
import pytest
from cafa4_format_checker import cafa4_file_validator as cafa_checker

'''
This file contains end-to-end tests that call the primary cafa submission file format validator
'''

@pytest.fixture(scope="module")
def test_data_path():
    ''' Provides a single, consistent absolute path to the test_data directory across environments '''
    root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return "{}/test/test_data/end_to_end_data/".format(root_path)


def test_team1234567890_zip_good(test_data_path, capfd):
    filepath = "{}valid/team1234567890.zip".format(test_data_path)
    is_valid = cafa_checker(filepath)
    output, error = capfd.readouterr()
    assert is_valid is True
    assert 'VALIDATION SUCCESSFUL' in output
    assert 'team1234567890.zip meets CAFA4 file naming specifications' in output

def test_team1234567890_zip_bad(test_data_path, capfd):
    filepath = "{}invalid/team1234567890.zip".format(test_data_path)
    is_valid = cafa_checker(filepath)
    output, error = capfd.readouterr()
    assert is_valid is False
    assert 'VALIDATION FAILED' in output
    assert "Only one team is allowed per zip file" in output

def test_basic_do_txt_file(test_data_path):
    filepath = "{}valid/ateam_1_9606_do.txt".format(test_data_path)
    is_valid = cafa_checker(filepath)
    assert is_valid is True


def test_basic_go_txt_file(test_data_path):
    filepath = "{}valid/ateam_1_9606_go.txt".format(test_data_path)
    is_valid = cafa_checker(filepath)
    assert is_valid is True


def test_mixed_predictions_zip_file(test_data_path, capfd):
    filepath = "{}invalid/Test1_9.zip".format(test_data_path)
    is_valid = cafa_checker(filepath)
    # Capture print statements to stdout
    output, error = capfd.readouterr()
    assert is_valid is False
    assert "VALIDATION FAILED" in output
    assert "Only one team is allowed per zip file" in output


def test_invalid_teamXYZ_zip_file(test_data_path, capfd):
    # this zip file contains a bind site prediction file that is not valid for CAFA 4:
    filepath = "{}invalid/teamXYZ.zip".format(test_data_path)
    is_valid = cafa_checker(filepath)
    # Capture print statements to stdout
    output, error = capfd.readouterr()

    assert is_valid is False
    assert error == ""
    assert 'VALIDATION FAILED' in output
    assert "With file teamXYZ_3_9606_binding.txt, binding is not a valid ontology for CAFA" in output


def test_go_and_do_zip_file(test_data_path, capfd):
    ''' Tests a simple valid zipfile '''
    filepath = "{}valid/ateam.zip".format(test_data_path)
    print("TESTING {}".format(filepath))
    is_valid = cafa_checker(filepath)
    # Capture print statements to stdout
    output, error = capfd.readouterr()
    assert is_valid is True
    assert error == ""
    #assert "Files correctly formatted" in output
    #assert "ateam_1_do.txt, passed the CAFA 4 DO prediction format checker" in output
    #assert "ateam_1_go.txt, passed the CAFA 4 GO prediction format checker" in output


def test_invalid_term_centric_zip(test_data_path, capfd):
    ''' This should fail due to multiple teams in a single zip '''
    filepath = "{}invalid/term_centric_test_predictions.zip".format(test_data_path)
    is_valid = cafa_checker(filepath)
    # Capture print statements to stdout
    output, error = capfd.readouterr()
    assert is_valid is False
    assert 'VALIDATION FAILED' in output
    #assert 'Only one team is allowed per zip file' in output
    assert 'Zip file names cannot include more than one underscore character' in output


def test_invalid_protein_centric_zip(test_data_path, capfd):
    #filepath = "{}invalid/protein_centric_test_predictions.zip".format(test_data_path)
    filepath = "{}invalid/TestTeam1_3.zip".format(test_data_path)
    is_valid = cafa_checker(filepath)
    # Capture print statements to stdout
    output, error = capfd.readouterr()
    assert is_valid is False
    assert 'VALIDATION FAILED' in output
    assert 'Only one team is allowed per zip file' in output


def test_invalid_binding_site_zip(test_data_path, capfd):
    filepath = "{}invalid/TestTeam1_1.zip".format(test_data_path)
    is_valid = cafa_checker(filepath)
    # Capture print statements to stdout
    output, error = capfd.readouterr()
    assert is_valid is False
    # TODO: Is this triggering the correct error?:
    assert 'VALIDATION FAILED' in output
    assert 'Only one team is allowed per zip file' in output

def test_invalid_mixed_ontology_data_in_txt_file(test_data_path, capfd):
    filepath = "{}invalid/bteam_1_9606_do.txt".format(test_data_path)
    is_valid = cafa_checker(filepath)
    # Capture print statements to stdout
    output, error = capfd.readouterr()
    assert is_valid is False
    assert 'VALIDATION FAILED' in output
    assert 'Author: Expected bteam, but found ateam' in output


def test_invalid_mixed_ontology_data_in_zip_file(test_data_path, capfd):
    filepath = "{}invalid/bTeam.zip".format(test_data_path)
    is_valid = cafa_checker(filepath)
    # Capture print statements to stdout
    output, error = capfd.readouterr()
    assert is_valid is False
    assert 'VALIDATION FAILED' in output
    #assert 'Error in bteam_1_9606_do.txt, line 0, Author: Expected bteam, but found ateam' in output
    assert 'Only one team is allowed' in output

def test_valid_tc_hpo_txt_file_with_implied_taxonomy(test_data_path):
    filepath = "{}valid/TC_ateam_3_hpo.txt".format(test_data_path)
    is_valid = cafa_checker(filepath)
    assert is_valid is True


