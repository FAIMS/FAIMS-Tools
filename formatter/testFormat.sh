#!/bin/bash
rvm use 2.1.1@faims
$(rvm which ruby) string_formatter_tester.rb db.sqlite3 $1