from dateutil import parser
import csv
import glob
import os
import re
import sys

data_directory = sys.argv[1]
data_files = glob.glob(os.path.abspath(data_directory)+"/*.tsv")

first_weeks_dict = dict()
for filename in data_files:
    matches = re.findall(r'\d{4}', filename)
    year = matches[0]
    reader = csv.DictReader(open(filename), delimiter='\t')

    first_row = reader.next()
    date = parser.parse(first_row["Date"])
    first_week = date.isocalendar()[1]

    first_weeks_dict[int(year)] = first_week

first_weeks_file = open(sys.argv[2], "w")
for key in sorted(first_weeks_dict):
    first_weeks_file.write("{0}\t{1}\n".format(key, first_weeks_dict[key]))

first_weeks_file.close()
