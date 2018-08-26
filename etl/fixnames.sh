#!/bin/sh

manual(){
   echo "FIX NAMES SCRIPT ($0):

This script has been written to remove special characters from file names,
"
}

usage() {
   echo "Usage:
	 $0 [-p <path>] [-t] [-k]
Where:
	-k: Keep suspects flag. If this flag is enabled and the new file name is too short, the file will be kept as is. This is used to capture files writen in different alphabets, which should be removed and not renamed.
	-t: Indicates the test mode. When runing in test mode files will be listed but not removed.
	-p: The path where the articl files are stored. If not provided defaults to the working dir.";
}

path="."
pfile=0
tflag=0
keepsuspectsflag=0

while getopts ":p:htk" o; do
    case "${o}" in
        k)
            keepsuspectsflag=1
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

if [ $tflag -eq 1 ]; then
    for file in `find $path | egrep -f ./filtrocharspecial.txt`; do
        filedir=`dirname $file`
        filename=`basename $file`
        newfilename=`echo $filename | sed -r 's/[^a-zA-Z0-9]+//g' | sed 's/txt$/.txt/'`

        nchars=`echo $newfilename | wc -m`
        if [ $nchars -lt 25 ]; then 
            # If most of the characters were replaced...
            echo "*WARN - \"$filename\" will be renamed to \"$newfilename\". This seems to be a foreign alphabet content and should be removed!"
        else
            echo "*INFO - \"$filename\" will be renamed to \"$newfilename\"."
        fi

    done
else
    for file in `find $path | egrep -f ./filtrocharspecial.txt`; do
        filedir=`dirname $file`
        filename=`basename $file`
        newfilename=`echo $filename | sed -r 's/[^a-zA-Z0-9]+//g' | sed 's/txt$/.txt/'`

	sourcepath=$file
        targetpath=$filedir"/"$newfilename

        nchars=`echo $newfilename | wc -m`
        if [ $nchars -lt 25 ]; then 
            # If most of the characters were replaced...

            if [ ! $keepsuspectsflag ]; then
                mv "$sourcepath" "$targetpath"
                echo "*INFO - \"$filename\" renamed to \"$targetpath\"."
            else
                echo "*WARN - \"$filename\" not renamed to \"$newfilename\". This seems to be a foreign alphabet content and should be removed!"
            fi
        else
            mv "$sourcepath" "$targetpath"
            echo "*INFO - \"$filename\" renamed to \"$targetpath\"."
        fi

    done
fi

exit 0
