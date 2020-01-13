#!/usr/bin/env python


#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import zipfile
import sys
import os
from cafa_hpo_format_checker import cafa_checker as hpo
from cafa_go_format_checker import cafa_checker as go
from cafa_do_format_checker import cafa_checker as do_checker
from cafa_validation_utils import validate_filename, validate_archive_name

CAFA_VERSION = 4



def ontology_validator(ontology, read_handle, filepath):
    """ A helper wrapper around the individual ontology checkers for go, do, hpo """
    VALIDATORS = {
        'do': do_checker,
        'go': go,
        'hpo': hpo
    }

    validator = VALIDATORS.get(ontology)

    if validator is None:
        return False, "Could not process ontology {}".format(ontology)

    is_valid, message = validator(read_handle, filepath)
    return is_valid, message


def cafa4_file_validator(filepath):
    """ Validates the filenaming of CAFA submissions """
    is_valid = True
    filepath_short = filepath.split("/")[-1]
    message = "VALIDATION SUCCESSFUL\n{filepath} meets CAFA4 file naming specifications".format(filepath=filepath_short)
    error_preamble = "\nVALIDATION FAILED"

    if filepath.endswith(".txt"):
        parsed = validate_filename(filepath)

        if not parsed.is_valid:
            message = parsed.message
            is_valid = False
        else:
            with open(filepath, "r") as read_handle:
                is_valid, message = ontology_validator(parsed.ontology, read_handle, filepath)

    elif zipfile.is_zipfile(filepath):
        # Check that the zipfile contains the team name and that team name is
        # consistent with the individual files within the zip:
        validation_result = validate_archive_name(filepath)
        if validation_result.is_valid is False:
            message = validation_result.message
            is_valid = False

        else:
            # we need to validate the contained txt files:

            for child_file in validation_result.files:
                zip_reader = zipfile.ZipFile(filepath)
                file_contents = zip_reader.open(child_file.filepath, 'r')
                child_file_is_valid, child_file_message = ontology_validator(child_file.ontology, file_contents, child_file.filename)

                if not child_file_is_valid:
                    is_valid = False
                    message = child_file_message
                    break

    else:
        is_valid = False
        message = "Could not parse {filepath}".format(filepath=filepath_short)

    if not is_valid:
        print(error_preamble)

    print(message)
    return is_valid


def usage():
    print("Usage: cafa4_format_check.py <path to input file or zipped archive>")


if __name__ == "__main__":
    try:
        cafa4_file_validator(sys.argv[1])
    except IndexError:
        usage()
