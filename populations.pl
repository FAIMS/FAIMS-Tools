#!/usr/bin/perl -w

# Written by Vincent Tran

# Scrapes through a given ui_schema.xml file and generates all the necessary attribute population and
# bind nodesets. Note that it does not differentiate between hierarchical (dropdown|picture gallery)
# and non-hierarchical.

$found = 0;
while($line = <>) {
    if($line !~ "ref=\"control\"" && $found == 0) {
        next;
    }
    $found = 1;
    if($line =~ "<!--") {next;}
    if($line =~ "ref=\"([^\"]+)\"") {
        push(@path, $1);
        $path = join "/", @path;
        if($line =~ "<select[^1]" && $line !~ "type=\"camera\"" && $line =~ "faims_attribute_name=\"([^\"]+)\"") {
            push @pops, "makeVocab(\"CheckBoxGroup\", \"$path\", \"$1\");";
        } elsif($line =~ "<select1" && $line =~ "faims_attribute_name=\"([A-Za-z0-9 \-]+)\"") {
            $attr_name = $1;
            if($line =~ "appearance=\"full\"") {
                push @pops, "makeVocab(\"RadioGroup\", \"$path\", \"$1\");";
            } elsif($line =~ "appearance=\"compact\"") {
                push @pops, "makeVocab(\"List\", \"$path\", \"$1\");";
            } else {
                push @pops, "makeVocab(\"DropDown\", \"$path\", \"$1\");";
            }    
        } elsif ($line =~ "input" && $line =~ "faims_attribute_type=\"measure\"") {
            push @nodesets, "<bind nodeset=\"/faims/$path\" type=\"decimal\"/>";
        }
    }
    if($line =~ "</group|</input|</trigger|</select") {
        pop @path;
    }
}
print "ui_logic populations\n";
print join("\n", @pops);
print ("\n\nBind nodesets\n");
print join("\n", @nodesets);