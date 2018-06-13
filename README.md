# FAIMS Tools

FAIMS Tools is a collection of scripts to make module development easier.
This readme outlines what's contained in each directory. Further information
can often be found in readme files within directories.

## generators/christian

This contains the module autogenerator ("autogen"). The autogen produces
module definition files and wireframes from a single `module.xml` file.

The autogen can be invoked using the `generate.sh` and `validate.sh` scripts
found in the same directory as this readme.

## userManagement

This is a collection of scripts which make it possible to manage user accounts
on a FAIMS server from a command-line interface. Illustrative examples of such
scripts are `addUser.py` to add a user and `delUser.py` to delete them.

## module-dev-scripts

This directory is for small scripts frequently used to ease development. In
includes `upload.py`, to upload modules and `as.py` to substitute arch16n values
into files.
