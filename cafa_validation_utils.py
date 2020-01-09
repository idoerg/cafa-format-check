from zipfile import ZipFile
import re
'''
This file contains various utility functions for validating the format
of CAFA submissions
'''


def validate_ontology_id(id_str):
    VALID_ONTOLOGIES = ['do', 'go', 'hpo']
    return id_str in VALID_ONTOLOGIES


def validate_model_id(model_id):
    # method_id should be an int between 1 and 3 inclusive:
    try:
        model_id = int(method_id)
    except ValueError:
        pass

    return 1 <= model_id <= 3

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
    split_filename = filename.rstrip(".txt").split("_")
    meta_count = len(split_filename)

    if not filename.endswith(".txt"):
        is_valid = False
        message = "{} is not a txt file".format(filename)

    # Most cases should have 4 "fields":
    elif meta_count == 4:
        team_name, model_id, taxonomy_id, ontology = split_filename
        # What to do about team name:

        if not validate_model_id(model_id):
            is_valid = False
            message = 'Model ID must be between 1 and 3 inclusive, not {model_id}'.format(model_id=model_id)

        elif not validate_taxonomy(taxonomy_id):
            is_valid = False
            message = '{taxomony_id} is not a valid taxonomy for CAFA'.format(taxonomy_id=taxonomy_id)

        elif not validate_ontology_id(ontology):
            is_valid = False
            message = '{ontology} is not a valid ontology'.format(ontology=ontology)

        # Special case for human species (taxonomy 9606) and the HPO
        elif not validate_human_phenotype_ontology(taxonomy_id, ontology):
            is_valid = False
            message = 'HPO is only valid with taxonomy 9606, not {taxonomy}'.format(taxonomy=taxonomy_id)

    return is_valid, message


def validate_one_team_per_archive(archive_handle):
    """ Check the files names contained in the passed archive to ensure that one and only one consistent team name
    is in the filenames of the archived files
    """
    txt_contents = [fname.split("/")[-1] for fname in archive_handle.namelist() if '__MACOSX' not in fname and '.DS_Store' not in fname and fname.endswith(".txt")]
    team_names_list = [fname.split("_")[0] for fname in txt_contents]
    team_names_set = set(team_names_list)
    return len(team_names_set) == 1, len(team_names_set), list(team_names_set)


def validate_archive_name(filepath):
    """ Checks that a zipfile's name includes only the teamname
    Also, compares the teamname found in the zipfile name to the teamname(s)
    of the files found within the zip.
    """
    zip_team_name = filepath.rstrip(".zip").split("/")[-1].split("_")[0]

    if not re.match('^\w+$', zip_team_name):
        return False, None, None


    with ZipFile(filepath, "r") as zip_handle:
        is_valid, team_count, team_names = validate_one_team_per_archive(zip_handle)

        # TODO: the return signatures shouldn't be so different depending on the validation state:
        if is_valid is False:
            return is_valid, team_count, team_names
        else:
            return zip_team_name == team_names[0], zip_team_name, team_names[0]
