 #!/bin/bash

echo $1 $2


export PATH="$HOME/.rbenv/bin:$PATH"
eval "$(rbenv init -)"

ruby string_formatter_tester.rb $2/db.sqlite3 $1 > /$1.output

echo "Start output"
cat $1.output
echo "Stop output"