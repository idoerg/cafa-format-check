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
        '/home/user/path/something/teamX_1_3702_hpo.txt',  # hpo has to be paired with 9606
    )

    invalid_filenames = (
        ('TC_team1_go.txt', 'TC_team1_go.txt does not match the required naming schemes'),  # Too few fields
        ('team1_1_1_1_9606_hpo.txt', 'team1_1_1_1_9606_hpo.txt does not match the required naming schemes'),  # Too many fields
        ('team.1_1_hpo.txt', 'With file team.1_1_hpo.txt, team.1 is not a valid team name'),  # punctuation in team name
        ('team-1_1_hpo.txt', 'With file team-1_1_hpo.txt, team-1 is not a valid team name'),  # punctuation in team name
        ('team1_0_3702_do.txt', 'With file team1_0_3702_do.txt, model ID must be between 1 and 3 inclusive, not 0'),  # invalid model ID
        ('team1_4_9606_go.txt',  'With file team1_4_9606_go.txt, model ID must be between 1 and 3 inclusive, not 4'),  # invalid model ID
        ('TC_team1_3_9606_zo.txt',  'With file TC_team1_3_9606_zo.txt, zo is not a valid ontology for CAFA'),  # invalid ontology
        ('team10000_1_9999_go.txt',  'With file team10000_1_9999_go.txt, 9999 is not a valid taxonomy for CAFA'),  # invalid taxonomy
        ('../team1_2_7955_do.doc',  'team1_2_7955_do.doc is not a txt file'),  # invalid file extension
        ('/home/user/path/something/teamX_1_3702_hpo.txt', 'With file teamX_1_3702_hpo.txt, HPO is only valid with taxonomy 9606, not 3702'),  # hpo has to be paired with 9606
    )

    for filename, error_str in invalid_filenames:
        parsed = validate_filename(filename)
        assert parsed.is_valid is False
        assert error_str in parsed.message
        assert 'ok' not in parsed.message

'''
TC_1_9606_hpo.txt
TC_1_hpo.txt
'''