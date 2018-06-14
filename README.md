# FAIMS Tools 
![alt text](https://github.com/FAIMS/faimsWebsite/blob/master/images/FAIMS-Med-BO.png "FAIMS Logo")

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

## generate.sh	
See generators/christian for details.

## validate.sh
See generators/christian for details.
