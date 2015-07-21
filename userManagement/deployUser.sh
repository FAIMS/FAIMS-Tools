#!/bin/bash

if [[ $# -ne 1 ]]; then
	echo "./deployUser.sh email"
	exit 1;
fi

insert=$(sqlite3 /var/www/faims/db/faims.sqlite3 "select 'REPLACE into user (userid, fname, lname, email) VALUES(' || id || ', ''' || first_name || ''', '''|| last_name || ''', ''' || email || ''');' from users where email = '$1'; ")


