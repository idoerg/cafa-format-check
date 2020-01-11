from cafa_do_format_checker import do_prediction_check


def test_valid_DO_lines():
    ''' Tests that a valid DO line passes validation '''
    data = (
        "T96060020120   DO:0003700  0.80",
        # multiple tabs:
        "T96060020120       DO:0003700      0.80",
        # Same as above with single spaces instead of tabs:
        "T96060020120 DO:0003700 0.70",
    )
    for line in data:
        is_valid, error_message = do_prediction_check(line)
        assert is_valid is True
        assert error_message is None


def test_invalid_DO_term_ids():
    ''' Tests that a variety of bad lines of prediction data fail validation '''

    # Combining multiple test cases for the sake of brevity
    # Each entry is a tuple of (1) bad prediction entry and (2) a substring of the expected error message
    bad_data = (
        # Wrong Ontology:
        ("T96060020120    GO:0003700  0.80", "error in second"),
        # Another wrong Ontology:
        ("T96060020120    FOO   0.80", "error in second"),
    )

    for line, expected_error_str in bad_data:
        is_valid, error_message = do_prediction_check(line)
        assert is_valid is False
        assert expected_error_str in error_message


def test_invalid_confidence_data():
    ''' Tests the a variety of invalid confidence data fail validation '''
    # Combining multiple test cases for the sake of brevity
    # Each entry is a tuple of (1) bad prediction entry and (2) a substring of the expected error message
    bad_data = (
        # Bad confidence:
        ("T96060020120    DO:0003700  None", "error in third (confidence) field"),
        # Too few digits in confidence:
        ("T96060020120 DO:0003700 0.9", "error in third (confidence) field"),
        # Too many digits in confidence:
        ("T96060020120    DO:0003700  0.765", "error in third (confidence) field"),
    )

    for line, expected_error_str in bad_data:
        is_valid, error_message = do_prediction_check(line)
        assert is_valid is False
        assert expected_error_str in error_message


def test_wrong_number_of_fields():
    ''' Tests that field count (3) is enforced during validation '''

    # Combining multiple test cases for the sake of brevity
    # Each entry is a tuple of (1) bad prediction entry and (2) a substring of the expected error message
    bad_data = (
        # Too few fields:
        ("DO:0003700  0.80", "wrong number of fields"),
        # Too many fields:
        ("DO:0003700 DO:0003700 1 0.80", "wrong number of fields"),
    )
    for line, expected_error_str in bad_data:
        is_valid, error_message = do_prediction_check(line)
        assert is_valid is False
        assert expected_error_str in error_message

