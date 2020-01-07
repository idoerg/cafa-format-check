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
import re
from cafa_go_format_checker import (
    target_field,
    confidence_field,
    author_check,
    model_check,
    keywords_check,
    accuracy_check,
    end_check,
    handle_error,
)

CAFA_VERSION = 4


def do_prediction_check(input_record):
    do_field_pattern = re.compile("^DO:[0-9]{5,7}$")
    is_correct = True
    error_msg = None
    error_msg_prefix = "DO prediction: "
    # fields = [i.strip() for i in input_record.split()

    try:
        target_value, do_value, confidence_value = [
            i.strip() for i in input_record.split()
        ]
    except ValueError:
        # Wrong number of values in the list
        is_correct = False
        error_msg = "{} wrong number of fields. Should be 3, not {}".format(error_msg_prefix, len(input_record.split()))
        return is_correct, error_msg

    # if len(fields) != 3:
    #    is_correct = False
    #    error_msg = "DO prediction: wrong number of fields. Should be 3"
    if not target_field.match(target_value):
        is_correct = False
        error_msg = "error in first (Target ID) field"
    elif not do_field_pattern.match(do_value):
        is_correct = False
        error_msg = "error in second (DO ID) field"
    elif not confidence_field.match(confidence_value):
        is_correct = False
        error_msg = "error in third (confidence) field"
    elif float(confidence_value) > 1.0:
        is_correct = False
        error_msg = "error in third (confidence) field. Cannot be > 1.0"

    if not is_correct:
        error_msg = error_msg_prefix + error_msg

    return is_correct, error_msg


def cafa_checker(input_file_handle, filename=None):
    """
    Main program that: 1. identifies fields; 2. Calls the proper checker function; 3. calls the
    error handler "handle_error" which builds the error report.  If correct is False, the function returns correct, errmsg
    to the file_name_check function in cafa3_format_checker.
    """

    # TODO: For the longterm, the filename param should be dropped.
    #  For the short-term, I'm keeping it so the function
    #  signature remains similar to the other checker functions, but making the filename param optional
    if filename is None:
        filename = input_file_handle.name

    visited_states = []
    accuracy_count = 0
    model_count = 0

    for line_index, input_line in enumerate(input_file_handle):
        line_split = [i.strip() for i in input_line.split()]
        input_state = line_split[0]

        states = ("AUTHOR", "MODEL", "KEYWORDS", "ACCURACY", "END")

        if input_state in states:
            state = input_state.lower()
        else:  # default to prediction state
            state = "do_prediction"

        # Check for errors according to state
        if state == "author":
            is_correct, error_msg = author_check(input_line)
            is_correct, error_msg = handle_error(
                is_correct, error_msg, input_line, line_index, filename
            )
            if not is_correct:
                return is_correct, error_msg
            visited_states.append(state)
        elif state == "model":
            model_count += 1
            accuracy_count = 0
            if model_count > 3:
                return False, "Too many models. Only up to 3 allowed"
            is_correct, error_msg = model_check(input_line)
            is_correct, error_msg = handle_error(
                is_correct, error_msg, input_line, line_index, filename
            )
            if not is_correct:
                return is_correct, error_msg
            if model_count == 1:
                visited_states.append(state)
        elif state == "keywords":

            if state not in visited_states:
                visited_states.append(state)

            is_correct, error_msg = keywords_check(input_line)
            is_correct, error_msg = handle_error(
                is_correct, error_msg, input_line, line_index, filename
            )
            if not is_correct:
                return is_correct, error_msg
        elif state == "accuracy":
            if state not in visited_states:
                visited_states.append(state)

            accuracy_count += 1
            if accuracy_count > 3:
                is_correct, error_msg = handle_error(
                    False, "ACCURACY: too many ACCURACY records", line_index, filename
                )
                return is_correct, error_msg
            else:
                is_correct, error_msg = accuracy_check(input_line)
                if not is_correct:
                    return is_correct, error_msg
        elif state == "do_prediction":
            is_correct, error_msg = do_prediction_check(input_line)
            if not is_correct:
                return handle_error(
                    is_correct, error_msg, input_line, line_index, filename
                )

            if state not in visited_states:
                visited_states.append(state)

        elif state == "end":
            is_correct, error_msg = end_check(input_line)
            is_correct, error_msg = handle_error(
                is_correct, error_msg, input_line, line_index, filename
            )
            if not is_correct:
                return is_correct, error_msg
            visited_states.append(state)

    # End file forloop

    # At this point the various states have been individually validated,
    # finally, check that the required states are all accounted for:
    if (
        visited_states[0] != "author"
        or visited_states[1] != "model"
        or visited_states[-2] != "do_prediction"
        or visited_states[-1] != "end"
    ):

        error_msg = "Error in {} filename \n".format(filename)
        error_msg += "Sections found in the file: [{}]\n".format(", ".join(visited_states))
        error_msg += "file not formatted according to CAFA {cafa_version} specs\n".format(
            cafa_version=CAFA_VERSION
        )
        error_msg += "Check if all these record types are in your file in the correct order\n"
        error_msg += (
            "AUTHOR, MODEL, KEYWORDS (optional), ACCURACY (optional), predictions, END"
        )
        return False, error_msg
    else:
        return (
            True,
            "{filename}, passed the CAFA {cafa_version} DO prediction format checker".format(
                filename=filename, cafa_version=CAFA_VERSION
            ),
        )


def main():
    import sys

    try:
        filepath = sys.argv[1]

        with open(filepath, "r") as do_handle:
            is_valid, error_msg = cafa_checker(do_handle)
            print("Is Valid: {}".format(is_valid))
            print("Message: {}".format(error_msg))
    except IndexError:
        print("No file specified")


if __name__ == "__main__":
    main()