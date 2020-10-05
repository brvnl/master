#!/bin/sh

manual(){
   echo "REMOVE URLS SCRIPT ($0):

This script has been written to remove the first line (URLs) from article files.
After execution the script will generate a lock file in the data path, to avoid runing it twice over the same files and removing data besides the url.
"
}

usage() {
   echo "Usage:
	 $0 [-p <path>]
Where:
	-p: The path where the articl files are stored. If not provided defaults to the working dir.";
}

path="."
pfile=0

while getopts ":p:h" o; do
    case "${o}" in
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

lockfile=$path"/."`basename $0`".lock"
if [ -f $lockfile ]; then
    echo "*WARN - Found lock file in the folder: \""$path"/."$0".lock\"."
    echo "*ERRO - The script has already been run for this path. Execution aborted."
    exit 1
fi

for file in `find $path -type f`; do
    sed -i '1d' $file
done

touch $lockfile

exit 0
