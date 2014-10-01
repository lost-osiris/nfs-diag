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
      new_path="$(echo -e $path).update.sh"
      $new_path $path
   else
      new_path="$(echo -e $path).main.py"
      $new_path $all_args
   fi
   
fi
