from zipfile import ZipFile
'''
This file contains various utility functions for validating the format
of CAFA submissions
'''

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
    zip_team_name = filepath.split("/")[-1].split("_")[0]

    with ZipFile(filepath, "r") as zip_handle:
        is_valid, team_count, team_names = validate_one_team_per_archive(zip_handle)

        # TODO: the return signatures shouldn't be so different depending on the validation state:
        if is_valid is False:
            return is_valid, team_count, team_names
        else:
            return zip_team_name == team_names[0], zip_team_name, team_names[0]


def main():
    import sys

    try:
        zip_path = sys.argv[1]

        with ZipFile(zip_path, "r") as zip_handle:
            result = validate_one_team_per_archive(zip_handle)
            print(result)

    except IndexError:
        print("Please pass a zip filename")

if __name__ == "__main__":
    main()


