# Module Dev Scripts

This directory contains small scripts related to module development.

## arch16N_cleaner.py

Given an arch16N.properties, ui_schema.xml and data_schema.xml file,
this script removes entries from the arch16n file which aren't used in either of the others.

## as.py

Replaces the arch16n _keys_ in one file with their _values_, from another, arch16n file.

The usage message can be seen by running it without arguments.

## sql2plot.py

Takes an sqlite database and a query returning two numerical columns, and plots the results. The first and
second columns are interpreted as the x and y axes, respectively.

This script's usage message can be seen by running it without arguments.

## upload.py

This script has been moved to [faims26_template_repo](https://github.com/FAIMS/faims26_template_repo).
