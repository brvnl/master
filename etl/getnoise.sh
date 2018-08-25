#!/bin/sh

manual(){
   echo "GET NOISE SCRIPT ($0):

This script has been written to retrieve the name of files with most ocurrences, which may represent noise in the data,
The goal is to use the script for analysis, and then later to use the information for data cleaning.
"
}

usage() {
   echo "Usage:
	 $0 [-n <rank>] [-p <path>]
Where:
	-n: The script will print the first n file names with more ocurrence. If not provided defaults to 15.
	-p: The path where the articl files are stored. If not provided defaults to the working dir.";
}

rank=15
path="."
while getopts ":n:p:h" o; do
    case "${o}" in
        n)
            rank=${OPTARG}
            ;;
        p)
            path=${OPTARG}
            ;;
        h)
            manual
            usage
            exit 0
            ;;
        *)
            usage
            exit 1
            ;;
    esac
done

echo "Count	Title" 
find $path | awk -F"/" '{ print substr($NF,16) }' | sort | uniq -c | sort -nr | head -n $rank

# Where:
#    1. The find command retrieves a list of files with their absolute path
#    2. The awk command will get only the filename with $NF, then remove the timestamp from the name;
#       Notice that 16 is hard coded, since it is specting a file name in the form yyyyMMddHHMMSS.thename.txt           
#    3. The next 3 commands will sort the filenames, then count the duplicates and sort again by the number of duplicates.
#    4. The head command is used to show the file names repeating the most, which can be interpreted as noise. 
