import os
from zipfile import ZipFile
import pytest
from cafa_do_format_checker import author_check, model_check, keywords_check
from cafa_validation_utils import validate_one_team_per_archive, validate_archive_name
from cafa_validation_utils import validate_author_line, validate_filename

@pytest.fixture(scope="module")
def test_data_path():
    ''' Provides a single, consistent absolute path to the test_data directory across environments '''
    root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return "{}/test/test_data/end_to_end_data/".format(root_path)

def test_validate_author_line_good():
    good_values = (
        "AUTHOR Shakespeare",
        "AUTHOR testauthor ",
        "AUTHOR      Plato",
    )

    for line in good_values:
        is_valid, message = validate_author_line(line)
        assert is_valid is True
        assert message == "ok"

def test_validate_author_line_bad():
    good_values = (
        "AUTHOR William Shakespeare",
        "AUTHOR: testauthor ",
        "AUTHORS     Plato",
    )

    for line in good_values:
        is_valid, message = validate_author_line(line)
        assert is_valid is False
        assert message != "ok"
        print(message)

def test_validate_archive_name_happy_path(test_data_path):
    ''' Test the validate_archive_name() function from cafa_validation_utils '''
    zip_path = "{}valid/ateam.zip".format(test_data_path)
    validation_result = validate_archive_name(zip_path)
    assert validation_result.is_valid is True
    assert validation_result.team_name == 'ateam' # == validation_result[2]

def test_validate_archive_name_with_bad_chars():
    ''' Test that a poorly named zip file would fail validation '''
    bad_str = "foo bar_.zip"
    validate_result = validate_archive_name(bad_str)
    assert validate_result[0] is False



def test_one_team_per_archive_happy_path(test_data_path):
    ''' Test that an archive containing files with a consistent single team name in the filenames passes
     the one team per archive validation
     '''
    zip_path = "{}valid/ateam.zip".format(test_data_path)

    with ZipFile(zip_path, "r") as zip_handle:
        is_valid, team_name_count, team_names = validate_one_team_per_archive(zip_handle)
        assert is_valid is True
        assert team_name_count == 1

def test_one_team_per_archive_invalid_input(test_data_path):
    ''' Test that an archive containing files with multiple team names in the filenames
    fails the one team per archive validation
     '''
    zip_path = "{}invalid/Test1_9.zip".format(test_data_path)

    with ZipFile(zip_path, "r") as zip_handle:
        is_valid, team_name_count, team_names = validate_one_team_per_archive(zip_handle)
        assert is_valid is False
        assert team_name_count == 5



def test_valid_author_str():
    ''' Tests that a valid author string passes validation '''
    test_str = "AUTHOR  testauthor"
    is_valid, message = author_check(test_str)
    assert is_valid is True
    assert message is None


def test_bad_author_str():
    ''' Tests that whitespace in the author name fails validation '''
    test_str = "AUTHOR  test author"
    is_valid, message = author_check(test_str)
    assert is_valid is False
    assert "invalid number of fields. Should be 2" in message


def test_good_model_str():
    ''' Tests that the expected model string format passes validation '''
    test_str = "MODEL 4"
    is_valid, message = model_check(test_str)
    assert is_valid is True
    assert message is None


def test_bad_model_str():
    ''' Tests that an empty string fails the model string validation '''
    test_str = ""
    is_valid, message = model_check(test_str)
    assert is_valid is False
    assert message is not None


def test_good_keywords_str():
    ''' Tests that a good keyword string passes validation as expected '''
    test_str = "KEYWORDS homolog, paralog, comparative model, predicted protein structure, de novo prediction, machine learning."
    is_valid, message = keywords_check(test_str)
    assert is_valid is True
    assert message is None


def test_bad_keywords_str():
    ''' Tests that a variety of bad keyword strings fail validation as expected '''

    # Combining multiple test cases for the sake of brevity:
    bad_keyword_strs = (
        # A colon after KEYWORDS identifier:
        "KEYWORDS homolog, parlog.",
        # No terminating period:
        "KEYWORDS homolog, parlog",
        # Invalid lowercase:
        "keywords machine learning.",
        # Unknown keyword:
        "KEYWORDS invalid-keyword.",
        # Tabs instead of commas:
        "KEYWORDS homolog    paralog.",
    )

    for test_str in bad_keyword_strs:
        is_valid, message = keywords_check(test_str)
        assert is_valid is False
        assert message is not None
