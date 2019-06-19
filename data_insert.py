#!/usr/bin/env python3

from load_data.db_interface import getConnection
from load_data.get_data import loadFileData

import argparse

parser = argparse.ArgumentParser(description='Generate ticket activity data')

parser.add_argument('-i', dest='input_file', default='activities.json',help='JSON file with data to be loaded')
parser.add_argument('-d', dest='output_db',default="test.db",help='SQLite database to load data into')

args = parser.parse_args()

data = loadFileData(args.input_file)
activities = data.get('activities_data')

conn = getConnection(args.output_db)

cursor = conn.cursor()

for a in activities:
    cursor.execute("insert into stg_activity ( ticket_id, performed_at, status ) values (?, ?, ?)",(a.get('ticket_id'), a.get('performed_at'), a.get('status')))
conn.commit()
cursor.close()
conn.close()

print("Loaded %s into %s" % (args.input_file, args.output_db))
