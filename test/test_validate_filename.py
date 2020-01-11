from cafa_validation_utils import validate_filename


def test_valid_filenames():
    ''' Test a variety of valid filenames '''
    valid_filenames = (
        'team1_1_3702_go.txt',
        'team1_1_9606_hpo.txt',
        'team1_1_hpo.txt',
        'team1_2_3702_do.txt',
        'team1_3_9606_go.txt',
        'TC_team1_3_9606_go.txt',
        'team10000_1_3702_go.txt',
        '../team1_2_7955_do.txt',
        '/home/user/path/something/teamX_1_3702_go.txt',
    )
    for filename in valid_filenames:
        parsed = validate_filename(filename)
        assert parsed.is_valid is True
        assert parsed.message == "ok"


def test_invalid_filenames():
    ''' Test a variety of INvalid filenames '''
    invalid_filenames = (
        'TC_team1_go.txt',  # Too few fields
        'team1_1_1_1_9606_hpo.txt',  # Too many fields
        'team.1_1_hpo.txt',  # punctuation in team name
        'team-1_1_hpo.txt',  # punctuation in team name
        'team1_0_3702_do.txt',  # invalid model ID
        'team1_4_9606_go.txt',  # invalid model ID
        'TC_team1_3_9606_zo.txt',  # invalid ontology
        'team10000_1_9999_go.txt',  # invalid taxonomy
        '../team1_2_7955_do.doc',  # invalid file extension
        '/home/user/path/something/teamX_1_3702_hpo.txt',  # hpo has to be paired with 9606?
    )

    for filename in invalid_filenames:
        parsed = validate_filename(filename)
        assert parsed.is_valid is False
        print(parsed.message)
        assert parsed.message != "ok"

'''
TC_1_9606_hpo.txt
TC_1_hpo.txt
'''