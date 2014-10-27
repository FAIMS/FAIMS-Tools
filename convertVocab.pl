#!/usr/bin/perl

# Written by Vincent Tran

# Converts makeVocab commands from FAIMS 1.3 to the FAIMS 2.0 format.

while($line = <>) {
    if($line =~ "populate([A-Za-z]+)\\\(\"([^\"]+).*makeVocab\\\(\"([^\"]+)") {
        $type = $1;
        $path = $2;
        $attrib = $3;
        next if $type =~ "Hierarchical";
        if($type =~ "Picture") {
            print "makePictureGallery(\"$path\", \"$attrib\");\n";
        } else {
            print "makeVocab(\"$type\", \"$path\", \"$attrib\");\n";    
        }
    }
}