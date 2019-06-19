#!/usr/bin/env python3

import sys
sys.path.append('generate_data')

import json
from generate_ticket import makeTicketActivies
import argparse

parser = argparse.ArgumentParser(description='Generate ticket activity data')

parser.add_argument('-n', dest='number_of_tickets',type=int, default=1000,help='Number of tickets to produce activities for')
parser.add_argument('-o', dest='output_file',default="activities.json",help='File to export ticket activity data to')

args = parser.parse_args()

print("Generating %s tickets" % str(args.number_of_tickets))

data = makeTicketActivies(args.number_of_tickets)

sys.path.pop()

with open(args.output_file, 'w') as file:
    file.write(json.dumps(data))

print("Generated %s activities to %s" % (str(data.get('metadata').get('activities_count')),args.output_file ))
