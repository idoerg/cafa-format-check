#!/usr/bin/perl -w
use strict;
############################
# Code to check whether prediction files comply with CAFA format.
# For details on CAFA format, see the CAFA Rules:
# http://biofunctionprediction.org/node/8
# Changes
# 2-JAN-2014 Iddo Friedberg: changed keyword list to conform with CAFA
# 2014 keywords
#
##############################


#check arguments, if none, print error
##################################
##################################

if ($#ARGV ==-1){
	print "\nERROR\n\n";
	print "Please provide the name of a file to check\n";
	print "\nERROR\n\n";
	exit;
}


#if more than one argument print error
##################################
##################################

if ($#ARGV != 0){
	print "\nERROR\n\n";
	print "Please provide only one argument\n";
	print "\nERROR\n\n";	
	exit;
}
	

#read file
##################################
##################################

my $file = shift;

open(FILE, "$file") or die "\nERROR\n\ncouldn't open file $file\n\nERROR\n\n";
my @data = <FILE>;
close FILE;

chomp(@data);


#make hash of keywords
##################################
##################################


#my @keytemp = ("sequence alignments", "profile-profile alignments", "sequence-profile alignments", "phylogeny", "phylogenomics", "derived/predicted", "sequence properties", "protein interactions", "gene expression", "mass spectrometry", "genetic interactions", "protein structure", "literature", "genomic context", "structure alignment", "comparative model", "predicted protein structure", "de novo prediction", "machine learning based method", "genome environment", "operon", "ortholog", "paralog", "protein interaction", "other functional information");

# Iddo: Added new keywords for CAFA 2014. 2-JAN-2014
my @keytemp = ( "sequence alignment", "sequence-profile alignment",
"profile-profile alignment", "phylogeny", "sequence properties",
"physicochemical properties", "predicted properties", "protein
interactions", "gene expression", "mass spectrometry", "genetic
interactions", "protein structure", "literature", "genomic context",
"synteny", "structure alignment", "comparative model", 
"predicted protein structure", "de novo prediction", 
"machine learning", "genome environment", "operon", 
"ortholog", "paralog", "homolog", "hidden Markov model", 
"clinical data", "genetic data", "natural language processing",
"other functional information");
my %valid_keywords;
map $valid_keywords{$_} = 1, @keytemp;

#print map "$_\n", keys(%keywords);

my $ERROR_NUMBER = 1;

#first check first line
##################################
##################################
if ($data[0] !~ m/^AUTHOR\s{1}/){
	print "\nERROR $ERROR_NUMBER\n\n";
	$ERROR_NUMBER++;
	print "First line should contain AUTHOR field\n\n";
	
	print "this is what should be your AUTHOR line\n$data[0]\n\n";
	print "\nEND ERROR\n\n";
	exit;
}


#check to make sure AUTHOR is specified only once
##################################
##################################
my @author_lines = grep $data[$_] =~ /^AUTHOR\s{1}/, 0..$#data;

if ($#author_lines > 0){
	print "\nERROR $ERROR_NUMBER\n\n";
	$ERROR_NUMBER++;

	print "It seems more than one AUTHOR was specified.\n";
	
	print "Only one AUTHOR line per file is permitted.\n\n";
	
	print "\nEND ERROR\n\n";
	exit;


}



#next check last line
##################################
##################################
if ($data[$#data] !~ m/^END$/){

	print "\nERROR $ERROR_NUMBER\n\n";
	$ERROR_NUMBER++;

	print "File should end with END\n\n";
	
	print "this is your last line:\n$data[$#data]\n\n";
	print "\nEND ERROR\n\n";
	exit;
}
	


#check to make sure END is specified only once
##################################
##################################
my @end_lines = grep $data[$_] =~ /^END$/, 0..$#data;

if ($#end_lines > 0){
	print "\nERROR $ERROR_NUMBER\n\n";
	$ERROR_NUMBER++;

	print "It seems more than one END was specified.\n";
	
	print "Only one END line per file is permitted.\n\n";
	
	print "\nEND ERROR\n\n";
	exit;


}




#lets determine the author name
##################################
##################################

my $author_line = $data[0];

my @author_fields = split /[\s|\t]/, $author_line;

#print map "Hello $_\n", @author_fields;
shift(@author_fields);


my $author_name = join ' ', @author_fields;
chomp($author_name);

if (length($author_name) == 0){
	print "\nERROR $ERROR_NUMBER\n\n";
	$ERROR_NUMBER++;

	print "It seems no Team Name was provided.\n";
	
	print "First line should contain AUTHOR field.\n\n";
	
	print "this is what should be your AUTHOR line.\n$data[0]\n\n";
	print "\nEND ERROR\n\n";
#	exit
}
	

#print "Author Name is $author_name\n";




#lets see how many models there are
##################################
##################################


my @model_lines = grep $data[$_] =~ /^MODEL/, 0..$#data;


#print map "$_\n", @model_lines;

if ($#model_lines == -1){
	print "\nERROR $ERROR_NUMBER\n\n";
	$ERROR_NUMBER++;

	print "It seems no MODEL line was specified.\n";
	
	print "Please specify a MODEL.\n\n";
	
	print "\nEND ERROR\n\n";
	exit;


}


if ($model_lines[0] != 1){
	print "\nERROR $ERROR_NUMBER\n\n";
	$ERROR_NUMBER++;

	print "Invalid File Format.\n";
	
	print "Please ensure the MODEL line is always the second line in the file.\n\n";
	
	print "\nEND ERROR\n\n";
	exit;


}



if ($#model_lines > 0){
	print "\nERROR $ERROR_NUMBER\n\n";
	$ERROR_NUMBER++;

	print "It seems more than 1 MODEL line was specified.\n";
	
	print "Please ensure that only one model is represented in each file.\n\n";
	
	print "\nEND ERROR\n\n";
	exit;


}


#make sure MODEL lines are of proper format
##################################
##################################



my $mln = $model_lines[0];
my @model_fields = split /[\s|\t]/, $data[$mln];
chomp(@model_fields);
my $line_number = $mln+1;

#check to make sure there is only one number in the model line
if ($#model_fields != 1){

	print "\nERROR $ERROR_NUMBER\n\n";
	$ERROR_NUMBER++;

	print "It seems you've specified a model of illegal format.\n";

	print "Models should be labeled 1 through 3.\n\n";

	print "this is your invalid MODEL line, from line number $line_number.\n$data[$mln]\n\n";
	print "\nEND ERROR\n\n";
#	exit
	
}


my $MODEL_NUMBER = $model_fields[1];

#make sure model numbers are valid
if ($model_fields[1] > 3 || $model_fields[1] < 1){
	print "\nERROR $ERROR_NUMBER\n\n";
	$ERROR_NUMBER++;

	print "Unexpected MODEL number. Model numbers should be 1 through 3.\n";

	print "this is your invalid MODEL line, from line number $line_number.\n$data[$mln]\n\n";
	print "\nEND ERROR\n\n";
	#exit
}
		
	







#now lets get into our models
##################################
##################################

#pop off end line
pop(@data);
#shift off top two lines
shift(@data);
shift(@data);


#next line should be the keyword line
my @keyword_lines = grep $data[$_] =~ /^KEYWORDS\s{1}/, 0..$#data;
	
if ($#keyword_lines > 0){
	print "\nERROR $ERROR_NUMBER\n\n";
	$ERROR_NUMBER++;

	print "It your file has more than one KEYWORDS line.\n";
	print "Please ensure that each model has exactly 1 KEYWORDS line.\n";
	print "\nEND ERROR\n\n";
	exit;
}


if ($#keyword_lines == -1){
	print "\nERROR $ERROR_NUMBER\n\n";
	$ERROR_NUMBER++;

	print "It seems your file has no KEYWORDS line.\n";
	print "Please ensure that each model has a KEYWORDS line.\n";
	print "\nEND ERROR\n\n";
	exit;
}


if ($keyword_lines[0] != 0){
	print "\nERROR $ERROR_NUMBER\n\n";
	$ERROR_NUMBER++;

	print "It seems your file is of invalid format.\n";
	print "Please ensure that the third line is the KEYWORDS line.\n";
	print "\nEND ERROR\n\n";
	exit;
}


my $kwl = shift(@data);
$kwl =~ s/KEYWORDS\s{1}//;

my @keywords = split ',', $kwl;
chomp(@keywords);

#


#why perl doesn't have a function to remove leading white space, like chomp
#I'll never know
foreach my $j (0..$#keywords){
	$keywords[$j] =~ s/^\s+//;
}

#my $temp = $keywords[$#keywords];
$keywords[$#keywords] =~ s/\.//;	

#print map"keyword START$_ STOP\n", @keywords;	
#print "\n\n";

my @nanners = grep !exists($valid_keywords{$_}), @keywords;


if ($#nanners != -1){
	print "\nERROR $ERROR_NUMBER\n\n";
	$ERROR_NUMBER++;

	print "It seems you have one or more invalid keywords.\n";
	print "Invalid Keywords: ";
	print map "$_\t", @nanners;
	print "\n";
	print "\nEND ERROR\n\n";
#	exit

}

################################		
#lets check for ACCURACY line  #
################################



if ($data[0] =~ /^ACCURACY\s{1}/){

	my $acl = shift(@data);
	my $raw_accuracy_line = $acl;
	
	$acl =~ s/^ACCURACY\s{1}//;
	my @accuracy_fields = split ' ', $acl;

	chomp(@accuracy_fields);
	foreach my $j (0..$#accuracy_fields){
		$accuracy_fields[$j] =~ s/^\s+//;
	}
	
	
	if ($#accuracy_fields != 1){
		print "\nERROR $ERROR_NUMBER\n\n";
		$ERROR_NUMBER++;

		print "Unexpected ACCURACY line format.\n";
		print "this is your invalid ACCURACY line.\n$raw_accuracy_line\n\n";
		print "\nERROR\n\n";
#		exit
	}
		
	if ($accuracy_fields[1] !~ /^PR=\d{1}\.{1}\d{2}$/){
		print "\nERROR $ERROR_NUMBER\n\n";
		$ERROR_NUMBER++;

		print "Unexpected ACCURACY line format.\n";
		print "this is your invalid ACCURACY line.\n$raw_accuracy_line\n\n";
		print "\nEND ERROR\n\n";
#			exit
	}

	if ($accuracy_fields[2] !~ /^RC=\d{1}\.{1}\d{2}$/){
		print "\nERROR $ERROR_NUMBER\n\n";
		$ERROR_NUMBER++;

		print "Unexpected ACCURACY line format.\n";
		print "this is your invalid ACCURACY line.\n$raw_accuracy_line\n\n";
		print "\nEND ERROR\n\n";
#			exit
	}


		
		
}



my %target_counts;
my %term_counts;
my @scores;
my %term_target;
my @excluded;
	
################################			
# now, all thats left are target, go id, score lines
################################


#space is assumed to be only valid delimiter, was told this was to be changed
foreach my $line (@data){
	
	my @fields = split 	/\s{1}/, $line;
	
	if ($#fields != 2){
		print "\nERROR $ERROR_NUMBER\n\n";
		$ERROR_NUMBER++;

		print "It seems you have an invalid prediction line.\n";

		print "this is your invalid prediction line.\n$line\n\n";

		print "\nEND ERROR\n\n";
#			exit

	}
		
#	if ($fields[0] !~ /^T\d{5}$/){
	if ($fields[0] !~ /^T\d{13}$/){
		print "\nERROR $ERROR_NUMBER\n\n";
		$ERROR_NUMBER++;

		print "It seems you have an invalid prediction line, invalid target id.\n";

		print "this is your invalid prediction line.\n$line\n\n";

		print "\nEND ERROR\n\n";
#			exit

	
	}
	else{
		if ($fields[2] ne "0"){
			$target_counts{$fields[0]}++;
		}
	}
	
		
	if ($fields[1] !~ /^GO\:\d{7}$/){
		print "\nERROR $ERROR_NUMBER\n\n";
		$ERROR_NUMBER++;

		print "It seems you have an invalid prediction line, invalid GO id.\n";

		print "this is your invalid prediction line.\n$line\n\n";

		print "\nEND ERROR\n\n";
#			exit

	
	}
	else{
		if ($fields[2] ne "0"){
			$term_counts{$fields[1]}++;
		}
	
	
	}
	
	#this part changed to allow 0's
	if ($fields[2] > 1 || $fields[2] < 0 ){
		print "\nERROR $ERROR_NUMBER\n\n";
		$ERROR_NUMBER++;

		print "It seems you have an invalid prediction line, invalid score.\n";

		print "this is your invalid prediction line.\n$line\n\n";

		print "\nEND ERROR\n\n";
#			exit

	
	}elsif ($fields[2] !~ /^\d?\.{1}\d{2}$/){
	
	    #allow the new zero score
		if ($fields[2] ne "0"){
			print "\nERROR $ERROR_NUMBER\n\n";
			$ERROR_NUMBER++;
	
			print "It seems you have an invalid prediction line, invalid score.\n";
	
			print "this is your invalid prediction line.\n$line\n\n";
	
			print "\nEND ERROR\n\n";
	    }else{
	    
    		push @excluded, $fields[0];
		}
	
	
	}else{

    	
		push @scores, $fields[2];

	}
	
	if ( !exists( $term_target{$fields[0]}{$fields[1]} ) ){
		$term_target{$fields[0]}{$fields[1]} = 1;
	}
	else{
		print "\nERROR $ERROR_NUMBER\n\n";
		$ERROR_NUMBER++;

		print "It seems you have an invalid prediction line: Duplicate Predictions.\n";
		print "Please only submit at most one score for one term/target pair\n";
		print "this is your invalid prediction line.\n$line\n\n";

		print "\nEND ERROR\n\n";
	
	
	}



}



my @too_many = grep {$target_counts{$_} > 1000} keys %target_counts;


if ($#too_many > -1){
	print "\nERROR $ERROR_NUMBER\n\n";
	$ERROR_NUMBER++;

	print "It seems some targets have too many predictions.\n";

	print "these are the targets:\n";
	print map "\t$_\n", @too_many;
	print "\n\n";
	print "\nEND ERROR\n\n";
#			exit


}


if ($ERROR_NUMBER == 1){

	my @targets = keys(%target_counts);
	my $num_targets = $#targets + 1;
	my @terms = keys(%term_counts);
	my $num_terms = $#terms + 1;
	my $num_excluded = $#excluded + 1;
	my @counts = values(%target_counts);
	@counts = sort {$a <=> $b} @counts;
	
	my $sum;
	
	map{$sum += $_} @counts;
	my $avg = $sum / ($#counts +1);
	$avg = sprintf("%.2f", $avg);
	print "\n\n\t\tCONGRATULATIONS!  No Errors Found\n\n";
	print"\t\tTeam Name: $author_name,\tModel Number: $MODEL_NUMBER\n";
	print "\t\tNumber of Targets with Predictions: $num_targets\n";
	print "\t\tNumber of GO Terms utilized: $num_terms\n";
	print "\t\tMaximum Number of Terms per Target: $counts[$#counts]\n";
	print "\t\tMinimum Number of Terms per Target: $counts[0]\n";
	print "\t\tAverage Number of Terms per Target: $avg\n";
	print "\t\tTotal Number of Excluded Annotations: $num_excluded\n";
	print "\n\n\t\tGood luck! The AFP team.\n\n";
}
else{
	print "\nFor the rules regarding valid file formats please refer to:\n\n";
	
	print "http://biofunctionprediction.org/node/262\n\n";
	

}


