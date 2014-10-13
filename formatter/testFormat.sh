#!/bin/bash

echo $1

rvm use 2.1.1@faims

$(rvm which ruby) string_formatter_tester.rb db.sqlite3 $1 > $1.output

cat $1.output