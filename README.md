# FAIMS Tools

FAIMS Tools is a collection of scripts to make module development easier.
This readme outlines what's contained in each directory. Further information
can often be found in individual readme files within directories.

1. formatter	
2. generators/christian	
 1. generate.sh	
 2. validate.sh
3. module-dev-scripts	
4. userManagement


## formatter 
TBD


## generators/christian

This folder contains the module autogenerator (also known as the "autogen"). The autogen produces
module definition files and wireframes from a single `module.xml` file.

The autogen can be invoked using the `generate.sh` and `validate.sh` scripts
found in the same directory as this readme (root directory of this repo).

## module-dev-scripts

This directory is for small scripts frequently used to ease development. In
includes `upload.py`, to upload modules and `as.py` to substitute arch16n values
into files. *If you are not sure what this means, do not interact with this directory.*

## userManagement

This is a collection of scripts which make it possible to manage user accounts
on a FAIMS server from a command-line interface. Illustrative examples of such
scripts are `addUser.py` to add a list of users to the server by one command and `delUser.py` to delete them, also using one command.
