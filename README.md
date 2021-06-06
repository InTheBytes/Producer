# Producer

A script that produces dummy data for the Stack Lunch api.

# Motivation

In order to properly test the robustness of our program and provide proof of concept for our analytics, dummy data is needed to populate all of the tables in our database.

# Dependencies

Python 3.7
Pandas
NumPy
BCrypt

# producer.py Description

Starting from parent tables and moving onto child tables, this script will produce random data based upon input data for names, customer addresses, restaurant names and addresses, and food.

# zip_map.py Description

This script maps customer addresses to zip codes based upon Baltimore, MD addresses and zip codes.

# Execution

Since customer addresses with mapped zip codes are already provided, only producer.py needs to be ran.
To do this, make sure an empty folder titled "csv" is in the working directory.
Then: run 'python producer.py'

