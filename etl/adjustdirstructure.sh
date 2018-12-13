#!/bin/bash

manual(){
   echo "ADJUST DIRECTORY STRUCTURE SCRIPT ($0):

For the initial crawler routine files were being saved on a flat folder, without any t5reatment for special chars in the file name.
This script goes through every artivle file, from every feeder, and convert the to the path structure /feeder/yyyyMM/file.
The procedure is specially important to reduce latence when performing searchs and ls commands.
"
}

usage() {
   echo "Usage:
         $0 [-i <source folder>] [-i <destination folder>] [-h]
Where:
        -i: The path from which the original article files will be retrieved.
        -o: The path where the new directory structure will be saved to. The files will be kept as is, they will be just copied to the new path.
        -h: Prints the manual and the usage.";
}

sourcefolder="."
#destination="/media/jduarte/Mestrado/data"
destination="$HOME/data.to20171216.fix"
while getopts ":i:o:h" o; do
    case "${o}" in
        i)
            sourcefolder=${OPTARG}
            ;;
        o)
            destination=${OPTARG}
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

logerr=`pwd`"/"$0".log"
cd $sourcefolder

echo "" > $logerr

for folder in `ls -d */`
do 
   #if [ ! "$folder" = "estadao.com.br/" ]; then
   #if [ ! "$folder" = "exame.abril.com.br/" ]; then
   #if [ ! "$folder" = "forbes.com/" ]; then
   #if [ ! "$folder" = "g1.globo.com/" ]; then
   if [ ! "$folder" = "infomoney.com.br/" ]; then
      continue
   fi

   echo "INFO* Visiting \"$folder\"."
   echo "INFO* Visiting \"$folder\"." >> $logerr
   cd $folder

   counter=0

   # This handles all filenames, but uses bash-specific extensions:
   while IFS="" read -r -d "" file ; do 
      # Use "$file" not $file everywhere.
      # You can set variables, and they'll stay set.
      #echo "*DEBUG - Filename: \"$file\"."
      #continue

   #for file in `find . -name "*.txt" -type f`
   #do
      fnametemp=`basename "$file"`
      fname=`echo $fnametemp | sed 's/[^a-z A-Z 0-9]//g' | sed 's/txt//g'`
      fnametest=`echo $fname | sed 's/[0-9]//g'`

      if [ ${#fnametest} -lt 5 ]; then
         continue
      fi

      yearmonth=`echo ${file:2:6}`
#      yearmonthtest=`echo $yearmonth | sed 's/[0-9]//g'`
#
#      if [[ "$yearmonthtest" -eq "" ]]; then
#         yearmonth="default"
#      fi

      tofolder="$destination/$folder/$yearmonth"

      #if [ -f $tofolder"/"$fname".txt" ]; then
      #   continue
      #fi

      mkdir -p $tofolder
      targetFile=$tofolder"/"$fname".txt"
      cp -f "$file" "$targetFile"
      
      rc=$?
      if [[ "$rc" -ne "0" ]]; then
         echo "ERR* Failed on:
	source: \"$file\".
	target: \"$tofolder/$file\"."
         echo "ERR* Failed on \"$tofolder/$file\"." >> $logerr
      fi

      counter=$((counter + 1))

      if [ `echo "$counter % 500" | bc` -eq 0 ]; then
         echo "INFO* $counter files processed."
         echo "INFO* $counter files processed." >> $logerr
      fi
   #done
   done < <(find . -name "*.txt" -type f -print0)

   echo "INFO* $folder concluded, $counter files processed."
   echo "INFO* $folder concluded, $counter files processed." >> $logerr
   cd ..
done

exit 0
