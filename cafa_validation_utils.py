from zipfile import ZipFile
import re
from collections import namedtuple
'''
This file contains various utility functions for validating the format
of CAFA submissions
'''

parsed_filename = namedtuple(
    "parsed_filename",
    ("is_valid", "message", "filename", "filepath", "team_name", "model_id", "taxonomy_id", "ontology")
)

parsed_zip_file = namedtuple(
    "parsed_zip_file",
    ("is_valid", "message", "team_name", "files")
)

def validate_ontology_id(id_str):
    VALID_ONTOLOGIES = ['do', 'go', 'hpo']
    return id_str in VALID_ONTOLOGIES


def validate_model_id(model_id):
    # method_id should be an int between 1 and 3 inclusive:
    try:
        model_id = int(model_id)
    except ValueError:
        pass

    return 1 <= model_id <= 3


def validate_author_line(author_line_str, expected_author=None):
    is_valid = True
    message = "ok"
    line_split = [i.strip() for i in author_line_str.split()]

    try:
        key, value = line_split
    except ValueError:
        # not two strings
        is_valid = False
        message = "AUTHOR: invalid number of fields. Should be 2, not {}".format(len(line_split))

    if is_valid:
        try:
            assert key == "AUTHOR"
        except AssertionError:
            is_valid = False
            message = 'AUTHOR: First field should be "AUTHOR", not "{}"'.format(key)

    if is_valid and expected_author is not None:
        try:
            assert value == expected_author
        except AssertionError:
            is_valid = False
            message = "Author: Expected {expected}, but found {actual}".format(expected=expected_author, actual=value)

    return is_valid, message


def validate_taxonomy(taxonomy_id_str):

    VALID_TAXONOMIES = (
        9606,   # "Homo sapiens"
        10090,  # "Mus musculus[All Names]"
        10116,  # "Rattus norvegicus"
        3702,   # "Arabidopsis thaliana[All Names]"
        83333,   # "Escherichia coli K-12[all names]" P
        7227,   # "Drosophila melanogaster[All Names]"
        287,    # "Pseudomonas aeruginosa[All Names]" P
        559292, # "Saccharomyces cerevisiae ATCC 204508"
        284812, # "Schizosaccharomyces pombe ATCC 24843"
        7955,   # "Danio rerio[All Names]"
        44689,  # "Dictyostelium discoideum[All Names]"
        243273, # "Mycoplasma genitalium ATCC 33530" P
        6239,   # "Caenorhabditis elegans[All Names]"
        226900, # "Bacillus cereus ATCC 14579" P
        4577,   # "Zea Mays [All names]"
        9823,   # "Sus scrofa"
        99287,  # Salmonella typhymurium ATCC 700720
    )

    try:
        taxonomy_id = int(taxonomy_id_str)
        return taxonomy_id in VALID_TAXONOMIES
    except ValueError:
        # taxonomy_id_str can't be converted to an int:
        return False


def validate_human_phenotype_ontology(taxonomy_id, ontology_id):
    if ontology_id == 'hpo' and str(taxonomy_id) != '9606':
        return False
    else:
        return True


def validate_filename(filename):
    ''' Validates that a CAFA submission txt file is properly named '''

    is_valid = True
    message = 'ok'
    team_name = model_id = taxonomy_id = ontology = None

    long_path = filename
    # If this is a path, we don't want to evaluate anything but the filename itself:
    filename = filename.split("/")[-1]
    split_filename = filename[:-4].split("_")
    #split_filename = filename.rstrip(".txt").split("_")
    meta_count = len(split_filename)

    if not filename.endswith(".txt"):
        is_valid = False
        message = "{filename} is not a txt file".format(filename=filename)
    elif meta_count == 5 and split_filename[0] == "TC":
        # This should be a term-centric file with this filename pattern:
        # TC_TEAMNAME_1_9606_GO.txt
        team_name, model_id, taxonomy_id, ontology = split_filename[1:]
    elif meta_count == 4 and split_filename[0] == "TC":
        # this is a term-centric hpo file with implied taxonomy of 9606:
        taxonomy_id = 9606
        team_name, model_id, ontology = split_filename[1:]

    elif meta_count == 3 and split_filename[-1] == "hpo":
        # This is an HPO file where the taxonomy is implicitly 9606:
        taxonomy_id = 9606
        team_name, model_id, ontology = split_filename
    elif meta_count == 4:
        # Most cases should have 4 "fields":
        team_name, model_id, taxonomy_id, ontology = split_filename
    else:
        is_valid = False
        message = "{filename} does not match the required naming schemes".format(filename=filename)

    # @ this point we should have team_name, model_id, taxonomy_id and ontology metadata extracted
    # from the various valid filename schemes
    # We can now move forward with validating each piece of metadata:
    if is_valid is True:
        # What to do about team name:
        if not re.match(r'^\w+$', team_name):
            is_valid = False
            message = "With file {filename}, {team_name} is not a valid team name".format(filename=filename, team_name=team_name)

        if not validate_model_id(model_id):
            is_valid = False
            message = 'With file {filename}, model ID must be between 1 and 3 inclusive, not {model_id}'.format(filename=filename, model_id=model_id)

        elif not validate_taxonomy(taxonomy_id):
            is_valid = False
            message = 'With file {filename}, {taxonomy_id} is not a valid taxonomy for CAFA'.format(filename=filename, taxonomy_id=taxonomy_id)

        elif not validate_ontology_id(ontology):
            is_valid = False
            message = 'With file {filename}, {ontology} is not a valid ontology for CAFA'.format(filename=filename, ontology=ontology)

        # Special case for human species (taxonomy 9606) and the HPO
        elif not validate_human_phenotype_ontology(taxonomy_id, ontology):
            is_valid = False
            message = 'With file {filename}, HPO is only valid with taxonomy 9606, not {taxonomy}'.format(filename=filename, taxonomy=taxonomy_id)

    return parsed_filename(is_valid, message, filename, long_path, team_name, model_id, taxonomy_id, ontology)

def validate_one_team_per_archive(archive_handle):
    """ Check the files names contained in the passed archive to ensure that one and only one consistent team name
    is in the filenames of the archived files
    """
    txt_contents = [fname.split("/")[-1] for fname in archive_handle.namelist() if '__MACOSX' not in fname and '.DS_Store' not in fname and fname.endswith(".txt")]
    # The following doesn't account for the TC_ (term-centric) filename prefix, so it's been replaced with
    # somethign more verbose:
    #team_names_list = [fname.split("_")[0] for fname in txt_contents]
    team_names_list = []
    for fname in txt_contents:
        fname_split = fname.split("_")

        if fname_split[0].upper() != 'TC':
            team_names_list.append(fname_split[0])
        else:
            team_names_list.append(fname_split[1])

    team_names_set = set(team_names_list)
    return len(team_names_set) == 1, len(team_names_set), list(team_names_set)


def validate_archive_name(filepath):
    """ Checks that a zipfile's name includes only the teamname
    Also, compares the teamname found in the zipfile name to the teamname(s)
    of the files found within the zip.
    """
    is_valid = True
    message = 'ok'

    if filepath[-4:] != ".zip":
        return parsed_zip_file(
            is_valid=False,
            message='Archive files must be zip archives',
            team_name=None,
            files=[]
        )

    split_filename = filepath[:-4].split("/")[-1].strip().split("_")
    #split_filename = filepath.rstrip(".zip").split("/")[-1].strip().split("_")
    zip_team_name = split_filename[0]
    print("********************")
    print("TESTING {}".format(filepath))

    if len(split_filename) > 2:
        return parsed_zip_file(
            is_valid=False,
            message='Zip file names cannot include more than one underscore character',
            team_name=zip_team_name,
            files=[]
        )

    if len(split_filename) == 2:
        try:
            ordinal = int(split_filename[-1])
        except ValueError:
            # the portion of the filename following the underscore which should represent an int, is invalid
            return parsed_zip_file(
                is_valid=False,
                message='The portion of the zip file name following the underscore should be an integer',
                team_name=zip_team_name,
                files=[]
            )



    parsed_files = None

    if not re.match(r'^\w+$', zip_team_name):
        return parsed_zip_file(
            is_valid=False,
            message='Team names in files can only include alphanumeric characters',
            team_name=zip_team_name,
            files=[]
        )

    with ZipFile(filepath, "r") as zip_handle:
        is_valid, team_count, team_names = validate_one_team_per_archive(zip_handle)

        if not is_valid:
            message = "Only one team is allowed per zip file"
        else:

            if team_names[0] != zip_team_name:
                is_valid = False
                message = 'Only one team is allowed per zipfile. "{}" and "{}" do not match.'.format(zip_team_name, team_names[0])

            parsed_files = []

            for filename in zip_handle.namelist():

                if 'DS_Store' in filename or '__MACOSX' in filename:
                    continue
                if filename.endswith("/"):
                    continue

                parsed = validate_filename(filename)
                parsed_files.append(parsed)

                if not parsed.is_valid:
                    is_valid = False
                    message = parsed.message

    #("is_valid", "message", "team_name", "files")
    return parsed_zip_file(
        is_valid=is_valid,
        message=message,
        team_name=zip_team_name,
        files=parsed_files
    )