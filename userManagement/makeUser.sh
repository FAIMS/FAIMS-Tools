#!/usr/bin/expect -f
log_user 1


set fname [lindex $argv 0]
set lname [lindex $argv 1]
set email [lindex $argv 2]
set pass  [lindex $argv 3]

if { $fname == "" || $lname == "" || $email == "" || $pass == "" } {
	puts "Usage fName lName email pass"
	exit 1 
}

spawn bash -c "cd /var/www/faims; rake users:create"

expect "First name of user: " 
send "$fname\n"

expect "Last name of user: "
send "$lname\n"


expect "Email of user: "
send "$email\n"


expect "Password: "
send "$pass\n"


expect "Confirm Password: "
send "$pass\n"

interact

spawn bash -c "/home/ubuntu/deployUser.sh $email"

interact

spawn python addUser.py $fname $lname

interact
