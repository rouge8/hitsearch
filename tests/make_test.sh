#!/bin/bash

# puts a ghost in the house
# usage: makeGhost file-to-be-ghosted house
function makeGhost {
    ln -s ../../$2 $1$2
}

if [ -f $1 ]
    then
        echo "${1} already exists.  delete it and try again."
        exit 1
    else
        mkdir $1
        for f in `ls ../`
            do
                #echo $f RULESBRO
                makeGhost "${1}/" $f
            done
fi
