#! /bin/bash

# create a user for postgres 
createuser certificate_manager
# create a new database for the project
createdb certificate_manager
# add a database password for the user
psql -d template1 -c "alter user certificate_manager with encrypted password 'password';"
# grant blanket permissions to the user
psql -d template1 -c "grant all privileges on database certificate_manager to certificate_manager;"
