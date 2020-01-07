from cafa_do_format_checker import author_check, model_check, keywords_check


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
