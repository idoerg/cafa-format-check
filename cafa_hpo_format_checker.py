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
import sys

pr_field = re.compile("^PR=[0,1]\.[0-9][0-9];$")
rc_field = re.compile("^RC=[0,1]\.[0-9][0-9]$")
hpo_field = re.compile("^HP:[0-9]{5,7}$")
target_field = re.compile("^T[0-9]{5,20}$")
confidence_field = re.compile("^[0,1]\.[0-9][0-9]$")
legal_states1 = ["author","model","keywords","accuracy","hpo_prediction","end"]
legal_states2 = ["author","model","keywords","hpo_prediction","end"]
legal_states3 = ["author","model","hpo_prediction","end"]

legal_keywords = [
"sequence alignment", "sequence-profile alignment", "profile-profile alignment", "phylogeny",
"sequence properties",
"physicochemical properties", "predicted properties", "protein interactions", "gene expression",
"mass spectrometry",
"genetic interactions", "protein structure", "literature", "genomic context", "synteny", 
"structure alignment",
"comparative model", "predicted protein structure", "de novo prediction", "machine learning", 
"genome environment", 
"operon", "ortholog", "paralog", "homolog", "hidden Markov model", "clinical data", "genetic data", 
"natural language processing", "other functional information"
]
    

def author_check(inrec):
    correct = True
    errmsg = None
    fields = [i.strip() for i in inrec.split()]
    if len(fields) != 2:
        correct = False
        errmsg = "AUTHOR: invalid number of fields. Should be 2"
    elif fields[0] != "AUTHOR":
        correct = False
        errmsg = "AUTHOR: First field should be AUTHOR"
    return correct, errmsg

def model_check(inrec):
    correct = True
    errmsg = None
    fields = [i.strip() for i in inrec.split()]
    if len(fields) != 2:
        correct = False
        errmsg = "MODEL: invalid number of fields. Should be 2"
    elif fields[0] != "MODEL":
        correct = False
        errmsg = "MODEL: First field should be MODEL"
    elif len(fields[1]) != 1 or not fields[1].isdigit():
        correct = False
        errmsg = "MODEL: second field should be single digit."
    return correct, errmsg

def keywords_check(inrec):
    correct = True
    errmsg = None
    if inrec[:8] != "KEYWORDS":
        correct = False
        errmsg = "KEYWORDS: first field should be KEYWORDS"
    else:
        keywords = [i.strip() for i in inrec[8:].split(",")]
        for keyword in keywords:
            # stupid full stop 
            if keyword[-1] == ".":
                keyword = keyword[:-1]
            if keyword not in legal_keywords:
                correct = False
                errmsg = "KEYWORDS: illegal keyword %s" % keyword
                break
    return correct, errmsg

def accuracy_check(inrec):
    correct = True
    errmsg = None
    fields = [i.strip() for i in inrec.split()]
    if len(fields) != 4:
        correct = False
        errmsg = "ACCURACY: error in number of fields. Should be 4"
    elif fields[0] != "ACCURACY":
        correct = False
        errmsg = "ACCURACY: first field should be 'ACCURACY'"
    elif not fields[1].isdigit() or len(fields[1]) != 1:
        correct = False
        errmsg = "ACCURACY: second field should be a single digit"
    elif not pr_field.match(fields[2]):
        correct = False
        errmsg = "ACCURACY: error in PR field"
    elif not rc_field.match(fields[3]):
        correct = False
        errmsg = "ACCURACY: error in RC field"
    return correct, errmsg


def hpo_prediction_check(inrec):
    correct = True
    errmsg = None
    fields = [i.strip() for i in inrec.split()]
    if len(fields) != 3:
        correct = False
        errmsg = "HPO prediction: wrong number of fields. Should be 3"
    elif not target_field.match(fields[0]):
        correct = False
        errmsg = "HPO prediction: error in first (Target ID) field"
    elif not hpo_field.match(fields[1]):
        correct = False
        errmsg = "HPO prediction: error in second (HP ID) field"
    elif not confidence_field.match(fields[2]):
        correct = False
        errmsg = "GO prediction: error in third (confidence) field"
    elif float(fields[2]) > 1.0:
        correct = False
        errmsg = "GO prediction: error in third (confidence) field"
    return correct, errmsg

def end_check(inrec):
    correct = True
    errmsg = None
    fields = [i.strip() for i in inrec.split()]
    if len(fields) != 1:
        correct = False
        errmsg = "END: wrong number of fields. Should be 1"
    elif fields[0] != "END":
        correct = False
        errmsg = "END: record should include the word END only"
    return correct, errmsg

def handle_error(correct, errmsg, inrec):
    if not correct:
        print inrec
        raise ValueError, errmsg

def cafa_checker(infile):
    visited_states = []
    s_token = 0
    n_accuracy = 0
    first_prediction = True
    first_accuracy = True
    first_keywords = True
    n_models = 0
    for inline in open(infile,'r'):
        inrec = [i.strip() for i in inline.split()]
        field1 = inrec[0]
        # Check which field type (state) we are in
        if field1 == "AUTHOR":
            state = "author"
        elif field1 == "MODEL":
            state = "model"
        elif field1 == "KEYWORDS":
            state = "keywords"
        elif field1 == "ACCURACY":
            state = "accuracy"
        elif field1 == "END":
            state = "end"
        else: #default to prediction state
            state = "hpo_prediction"
#        print "****"
#        print "FIELD1", field1
#        print inline, state
        # Check for errors according to state
        if state == "author":
            correct,errmsg = author_check(inline)
            handle_error(correct, errmsg,inline)
            visited_states.append(state)
        elif state == "model":
            n_models += 1
            n_accuracy = 0
            if n_models > 3:
                raise ValueError, "Too many models. Only up to 3 allowed"
            correct,errmsg = model_check(inline)
            handle_error(correct, errmsg,inline)
            if n_models == 1:
                visited_states.append(state)
        elif state == "keywords":
            if first_keywords:
                visited_states.append(state)
                first_keywords = False
            correct, errmsg = keywords_check(inline)
            handle_error(correct, errmsg,inline)
        elif state == "accuracy":
            if first_accuracy:
                visited_states.append(state)
                first_accuracy = False
            n_accuracy += 1
            if n_accuracy > 3:
                handle_error(False, "ACCURACY: too many ACCURACY records")
            else:
                correct, errmsg = accuracy_check(inline)
        elif state == "hpo_prediction":
            correct, errmsg = hpo_prediction_check(inline)
            handle_error(correct, errmsg,inline)
            if first_prediction:
                visited_states.append(state)
                first_prediction = False
        elif state == "end":
            correct, errmsg = end_check(inline)
            handle_error(correct, errmsg,inline)
            visited_states.append(state)
    # End file forloop
    if (visited_states != legal_states1 and
        visited_states != legal_states2 and
        visited_states != legal_states3):
        print visited_states
        print "file not formatted according to CAFA specs"
        print "Check whether all these record types are in your file in the correct order"
        print "AUTHOR, MODEL, KEYWORDS, ACCURACY (optional), predictions, END"
        raise ValueError
    else:
        print "Your input file passed the CAFA 2 format checker"
def usage():
    print "Usage: cafa_hpo_format_checker infile"
if __name__ == '__main__':
    try:
        cafa_checker(sys.argv[1])
    except IndexError:
        usage()

