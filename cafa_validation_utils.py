'''
This file contains various utility functions for validating the format
of CAFA submissions
'''

def validate_one_team_per_archive(archive_handle):
    ''' Check the files names contained in the passed archive to ensure that one and only one consistent team name
    is in the filenames of the archived files
    '''
    txt_contents = [fname.split("/")[-1] for fname in archive_handle.namelist() if '__MACOSX' not in fname and '.DS_Store' not in fname and fname.endswith(".txt")]
    team_names_list = [fname.split("_")[0] for fname in txt_contents]
    team_names_set = set(team_names_list)
    return len(team_names_set) == 1, len(team_names_set), team_names_set

def main():
    import sys
    from zipfile import ZipFile

    try:
        zip_path = sys.argv[1]

        with ZipFile(zip_path, "r") as zip_handle:
            result = validate_one_team_per_archive(zip_handle)
            print(result)

    except IndexError:
        print("Please pass a zip filename")

if __name__ == "__main__":
    main()


