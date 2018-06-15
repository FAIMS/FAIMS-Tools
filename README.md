# FAIMS Tools 
<img src="https://github.com/FAIMS/faimsWebsite/blob/master/images/FAIMS-CYMK-FULL-VECTOR.png" height="100" width="100">

FAIMS Tools is a collection of scripts to make module development easier. This readme outlines what's contained in each directory. Further information can often be found in individual readme files within directories. 

Further instructions how to use FAIMS Tools and the autogen can be found in the [User to Developer Instructions](https://github.com/FAIMS/UserToDev/blob/master/UserToDev.pdf). 

For information about FAIMS, visit the [FAIMS Webpage](https://www.fedarch.org/) or the [FAIMS Mobile Platform User Guide](https://faimsproject.atlassian.net/wiki/spaces/MobileUser/pages/4784159/Introduction).
Alternatively, you can contact us at enquiries@fedarch.org and we will get back to you within one business day.

1. formatter	
2. generators/christian	
3. module-dev-scripts	
4. userManagement
5. generate.sh	
6. validate.sh


## formatter 

Software in this directory allows you to execute SQLite queries as they would be in [the FAIMS app](https://github.com/FAIMS/faims-android). In particular, `formatter` deals with [format strings](https://faimsproject.atlassian.net/wiki/spaces/FAIMS/pages/3014726/FAIMS+Data+UI+and+Logic+Cook-Book#FAIMSData,UIandLogicCook-Book-AttributeFormatString) correctly, however it also allows queries which depend on spatialite to be run.

The most commonly used script is `testFormat.sh`. If `testFormat.sh` is given the path of a file containing a query as its first argument, another file will be created with that query's output. The file will be created in the current working directory.

A list of dependencies can be found in `formatter`'s readme.

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

## generate.sh	
See generators/christian for details.

## validate.sh
See generators/christian for details.
