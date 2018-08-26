#!/bin/sh

manual(){
   echo "REMOVE NOISE SCRIPT ($0):

This script has been written to remove files whose names matches any of the regex given in the input paramter file, given in -f,
The goal is to remove bad data file captured from the feeders.
"
}

usage() {
   echo "Usage:
	 $0 [-f <pattern file>] [-p <path>] [-t]
Where:
	-f: The file containing patterns to be matched against the file names to be removed.
	-t: Indicates the test mode. When runing in test mode files will be listed but not removed.
	-p: The path where the articl files are stored. If not provided defaults to the working dir.";
}

path="."
pfile=0
tflag=0

while getopts ":f:p:ht" o; do
    case "${o}" in
        f)
            pfile=${OPTARG}
            if [ ! -f $pfile ]; then 
                echo "*ERROR - Could not find the file \"$pfile\"."
                exit 1
            fi
            ;;
        t)
            echo "*INFO - Runing in test mode."
            tflag=1
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

echo "*INFO - Using path \"$path\"."
echo "*INFO - Using regex file \"$pfile\"."

ncharspath=`echo $path | wc -m`

if [ $tflag -eq 1 ]; then
    for file in `find $path | egrep -f $pfile`; do
        echo "*INFO - The file \"$file\" is marked to be removed."
    done
else
    for file in `find $path | egrep -f $pfile`; do
        ncharsfile=`echo $file | wc -m`

        if [ $ncharsfile -lt $((ncharspath + 14)) ]; then
            echo "*WARN - File name \"$file\" is too short, not removing for safety."
        else
            echo "*INFO - Removing file \"$file\"."
            rm $file
        fi
    done
fi

exit 0
