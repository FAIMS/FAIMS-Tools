 #!/bin/bash

echo $1 $2


set -euo pipefail
source ~/.profile

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

export PATH="$HOME/.rbenv/bin:$PATH"
eval "$(rbenv init -)"

#$HOME/.rbenv/bin/rbenv local 2.3.1

$($HOME/.rbenv/bin/rbenv which ruby) $DIR/string_formatter_tester.rb db.sqlite3 $1 > $1.output

echo "Start output"
cat $1.output
echo "Stop output"


 


 
