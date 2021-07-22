# Producer

A script to be placed in a lambda function that produces dummy data for the Stack Lunch api.

# Motivation

In order to properly test the robustness of our program and provide proof of concept for our analytics, dummy data is needed to populate all of the tables in our database.

# Dependencies

Python 3.7
Pandas
NumPy
BCrypt
Boto3

# producer.py Description

Starting from parent tables and moving onto child tables, this script will produce random data based upon input data from s3 buckets for names, customer addresses, restaurant 
names and addresses, and food. As the data is being produced, it is streamed in batches to a kinesis data stream to be grabbed by another lambda function which will upload it 
into our database.

# zip_map.py Description

This script maps customer addresses to zip codes based upon Baltimore, MD addresses and zip codes.

# Execution

This script is mean to be run as a lambda function inside of our aws cloud which will be called by an api gateway.
