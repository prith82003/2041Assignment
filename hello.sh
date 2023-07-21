#!/bin/dash
a="hello "
b=world

test=$a$b

str="Sentence: $a $b" 

for file in *.py
do
    echo $file
done

exit 1