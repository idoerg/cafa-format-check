import os
import pytest
from cafa_validation_utils import validate_archive_name, validate_one_team_per_archive

@pytest.fixture(scope="module")
def test_data_path():
    ''' Provides a single, consistent absolute path to the test_data directory across environments '''
    root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return "{}/test/test_data/end_to_end_data/".format(root_path)


def test_zip_file_with_underscore(test_data_path):

   path = "{path}valid/TeamMultipleZipFiles_1.zip".format(path=test_data_path)
   validator = validate_archive_name(path)
   assert validator.is_valid is True


def test_too_many_underscores_in_zip_file_name():
    bad_filename = "ateam_1_2.zip"
    validator = validate_archive_name(bad_filename)
    assert validator.is_valid is False
    assert 'Zip file names cannot include more than one underscore character' in validator.message


def test_zip_ordinal_field_is_not_int():
    bad_filename = "ateam_two.zip"
    validator = validate_archive_name(bad_filename)
    assert validator.is_valid is False
    assert 'The portion of the zip file name following the underscore should be an integer' in validator.message
