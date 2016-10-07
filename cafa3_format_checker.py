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
import csv
import sys
import re

import cafa_hpo_format_checker as hpo
hpo = hpo.cafa_checker

import cafa_go_format_checker as go
go = go.cafa_checker

import cafa_binding_site_format_checker as bind
bind = bind.cafa_checker

"""
Files are sent here from the main function if there are three fields seperated by '_' in the input filename.
function purpose:
    1. check that the third field is an integer and is between 1 and 3.
    2. check the second field for a taxonId or "hpo" to decide whether to branch into the GO format checker or HPO format checker
    3. test to see whether the file is zipped
        a. if zipped, opens, unzips, and reads the zipped file into cafa_{go/hpo}_format_checker.cafa_checker
        b. if not zipped, opens file and reads into cafa_{go/hpo}_format_checker.cafa_checker

"""
def go_hpo_predictions(path, fileName):
    features = (fileName.split(".")[0]).split("_")
    try:
        modelNum = int(features[1][-1:])
    except:
        return False, "Model number in filename must be integer"
    taxon = features[2].lower()
    if (modelNum < 1 or modelNum > 3):
        return False, "Model number in file name incorrect, you may only submit one to three models\n\nFormat should be teamId_model#_taxonId/hpo.txt"
    if taxon == "hpo":
        if zipfile.is_zipfile(path):
            files = zipfile.ZipFile(path, "r")
            names = files.namelist()
            names = [name for name in names if "__MACOSX" not in name]
            if len(names) > 1:
                return False, "Each zipped archive can only contain one file.  Please re-submit using single zipped files."
            else:
                file = names[0]
                file = files.read(file).strip().split("\n")
                hpo(file)
        else:
            infile = open(path, 'r')
            hpo(infile)
        return True, "HPO prediction file has been validated!"
    else:
        if zipfile.is_zipfile(path):
            files = zipfile.ZipFile(path, "r")
            names = files.namelist()
            names = [name for name in names if "__MACOSX" not in name]
            if len(names) > 1:
                return False, "Each zipped archive can only contain one file.  Please re-submit using single zipped files."
            else:
                file = names[0]
                file = files.read(file).strip().split("\n")
                go(file)
        else:
            infile = open(path, 'r')
            go(infile)
        return True, "GO prediction file has been validated!"


"""
Files are sent here from the main function if there are four fields seperated by '_' in the input filename.
function purpose:
    1. check that the fourth field is 'binding'.
    2. check that the third field is an integer and is between 1 and 3.
    3. check that the second field is not 'hpo'
    4. test to see whether the file is zipped
        a. if zipped, opens, unzips, and reads the zipped file into cafa_binding_site_format_checker.cafa_checker
        b. if not zipped, opens file and reads into cafa_binding_site_format_checker.cafa_checker
"""
def binding_sites(path, fileName):
    features = (fileName.split(".")[0]).split("_")
    try:
        modelNum = int(features[1][-1:])
    except:
        return False, "Model number in filename must be integer"
    taxon = features[2].lower()
    bind_field = features[3].lower()
    if bind_field != "binding":
        return False, "Binding specification in filename is incorrect.  Binding site prediction filename must be formatted teamId_model#_taxonId_binding.{txt/zip}\nField four is incorrect, must be 'binding'."
    elif (modelNum < 1 or modelNum > 3):
        return False, "Model number in file name incorrect, you may only submit one to three models\n\nFormat should be teamId_model#_taxonId/hpo_binding.{txt/zip}"
    elif taxon == "hpo":
        return False, "Binding site prediction filename cannot have 'hpo' as third field, must be taxon Id."
    else:
        if zipfile.is_zipfile(path):
            files = zipfile.ZipFile(path, "r")
            names = files.namelist()
            names = [name for name in names if "__MACOSX" not in name]
            if len(names) > 1:
                return False, "Each zipped archive can only contain one file.  Please re-submit using single zipped files."
            else:
                file = names[0]
                file = files.read(file).strip().split("\n")
                bind(file)
        else:
            infile = open(path, "r")
            bind(infile)
        return True, "Binding site prediction file has been validated!"


"""
HPO and GO predictions are supposed to be team_model#_taxonID/HPO
Binding site predictions are supposed to be team_model#_taxonID/HPO
Checks how many fields seperated by '_' counted, and sent to the proper checker function

function purpose:
    1. Checks the filename and format
    2. Calls the proper checker function
"""
def cafa_checker(infile):

    fileName = infile.split("/")[-1]
    features = fileName.split(".")[0].split("_")

    if len(features) == 3:
        return go_hpo_predictions(infile, fileName)

    elif len(features) == 4:
        return binding_sites(infile, fileName)
    
    elif len(features) < 3:
        print "There are not enough fields seperated by '_' to the left of .{txt/zip} in the filename\n\nFor HPO and GO predictions, the filename should be three fields, team_model#_{taxonID / hpo}\n\nFor binding site predictions, filename should be four fields, team_model#_{taxonID / hpo}_binding"
        
    else:
        print "There are too many fields seperated by '_' to the left of .{txt/zip} in the filename\n\nFor HPO and GO predictions, the filename should only be three fields, team_model#_{taxonID / hpo}\n\nFor binding site predictions, filename should only be four fields, team_model#_{taxonID / hpo}_binding"

def usage():
    print "Usage: cafa3_format_check.py <infile path>"

if __name__ == '__main__':
    try:
        cafa_checker(sys.argv[1])
    except IndexError:
        usage()

