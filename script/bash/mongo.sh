#!/bin/bash

# Start mongo shell with your database and execute queries
mongo <<EOF
use scraperDatabase

# Show all collections
show collections

# Fetch all documents from 'crunchbase_data' collection and display them
print("Fetching data from crunchbase_data collection...")
db.crunchbase_data.find().pretty()

# FetIt looks like you are trying to access MongoDB over HTTP on the native driver port.ch all documents from 'google_data' collection and display them
print("Fetching data from google_data collection...")
db.google_data.find().pretty()

# Fetch all documents from 'extracted_emails' collection and display them
print("Fetching data from extracted_emails collection...")
db.extracted_emails.find().pretty()

EOF
