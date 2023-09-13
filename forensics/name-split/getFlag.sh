#!/bin/bash

found=1
next='starthere.zip'

while [ ${found} -eq 1 ]; do
    echo "Unzipping - $next"
    tmp=$(zipinfo -1 $next)
    printf %s `zipinfo -1 $next` >> flagEncoded.txt
    unzip $next
    rm $next
    next=$tmp
    if [ "$next" = "==" ];
    then
        rm $next
        found=0
    fi
done
cat flagEncoded.txt | base64 -d > flagDecoded.txt
exit 0

#General writeup:
#Every zip-file name is two characters of the base64 encoded flag
#Unzip every zip manually, or make a script to do it
#Then just piece output together and base64 decode it