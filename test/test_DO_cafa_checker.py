import os
import pytest
from cafa_do_format_checker import cafa_checker

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
    return "{}/test/test_data/".format(root_path)



def test_basic_happy_path_file(test_data_path):
    filepath = "{}disorder_ontology/ZZZ_basic_valid_DO_example.txt".format(test_data_path)

    with open(filepath, "r") as read_handle:
        is_valid, message = cafa_checker(read_handle)
        assert is_valid is True
        assert "passed the CAFA 4 DO prediction format checker" in message


def test_invalid_keyword_file(test_data_path):
    ''' Tests that an illegal keyword is caught during validation '''

    filepath = "{}disorder_ontology/ZZZ_bad_keyword_DO_example.txt".format(test_data_path)

    with open(filepath, "r") as read_handle:
        is_valid, message = cafa_checker(read_handle)
        assert is_valid is False
        assert 'KEYWORDS: illegal keyword' in message


def test_missing_method_line_file(test_data_path):
    ''' Tests that a file with no method data is caught during validation '''
    filepath = "{}disorder_ontology/ZZZ_missing_model_DO_example.txt".format(test_data_path)

    with open(filepath, "r") as read_handle:
        is_valid, message = cafa_checker(read_handle)
        assert is_valid is False

        message_split = message.split("\n")
        # The second line of the message should be something like this:
        # Sections found in the file: [author, keywords, do_prediction, end]
        # So, we will verify that "model" is missing, as expected:

        print("#####################################")
        print(message_split)
        #assert True
        assert "model" not in message_split[1]


def test_missing_author_line_file(test_data_path):
    ''' Tests that a file with no author data is caught during validation '''
    filepath = "{}disorder_ontology/missing_author_DO_example.txt".format(test_data_path)

    with open(filepath, "r") as read_handle:
        is_valid, message = cafa_checker(read_handle)
        assert is_valid is False

        # See test_missing_method_line() function for explanation of this:
        message_split = message.split("\n")
        assert "author" not in message_split[1]


def test_missing_end_line_file(test_data_path):
    ''' Tests that a file with no END delimiter is caught during validation '''
    filepath = "{}disorder_ontology/ZZZ_missing_end_DO_example.txt".format(test_data_path)

    with open(filepath, "r") as read_handle:
        is_valid, message = cafa_checker(read_handle)
        assert is_valid is False

        # See test_missing_method_line() function for explanation of this:
        message_split = message.split("\n")
        assert "end" not in message_split[1]


def test_invalid_confidence_data_file(test_data_path):
    ''' Tests that a variety of bad confidence entries are caught during validation '''
    # Combining multiple test cases for brevity

    bad_confidence_filepaths = (
        # contains a zero confidence:
        "disorder_ontology/bad_confidence_DO_example_1.txt",
        # contains a positive integer confidence:
        "disorder_ontology/bad_confidence_DO_example_2.txt",
        # contains a string confidence:
        "disorder_ontology/bad_confidence_DO_example_3.txt",
    )
    print("")
    for path in bad_confidence_filepaths:
        full_path = test_data_path + path
        print("TESTING {}".format(full_path))

        with open(full_path, "r") as read_handle:
            is_valid, message = cafa_checker(read_handle)
            assert is_valid is False
            assert "DO prediction: error in third (confidence) field" in message

