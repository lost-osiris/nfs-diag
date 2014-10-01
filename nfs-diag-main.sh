#!/bin/bash
ARG=($@)
PATH=false
UPDATE=false
path=""
all_args=""
if [ "$ARG" != "" ]; then
   for x in "${ARG[@]}"; do
      case $x in
         "-p" | "--path")
            path=true
         ;;
         "-u" | "--update")
            UPDATE=true
         ;;
         *)
            if [[ $path == true ]]; then
               path=$(echo -e $x)
            else
               all_args="$all_args $x"
            fi
         continue
      esac
   done
   if [[ $UPDATE == true ]]; then
      sh $(echo -e $path)update_script.sh $path
   else
      python $(echo -e $path)main.py $all_args
   fi
   
fi
