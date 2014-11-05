from dateutil import parser
import csv
import glob
import os
import re

def get_team_id_dict(filename):
    f = open(filename)
    team_ids = dict()
    for line in f:
        line = line.rstrip()
        team_name, team_id = line.split("\t")
        team_ids[team_name] = int(team_id)
        team_ids[int(team_id)] = team_name

    f.close()

    return team_ids

"""
Takes a directory, loads all of the files, and returns a large dictionary
keyed with the following GID (game id):

    year_week_awayteam_hometeam

All of the values are the raw values contained in the files. Further feature
generation is handled by other methods.
"""
def parse_all_stats(directory, team_ids):
    data_files = glob.glob(os.path.abspath(directory)+'/*.tsv')

    for filename in data_files:
        matches = re.findall(r'\d{4}', filename)
        year = matches[0]
        reader = csv.DictReader(open(filename), delimiter='\t')
        for row in reader:
            date = parser.parse(row["Date"])
            if year == "2000":
                print year
                print row["TeamName"], row["Opponent"], date, date.isocalendar()
                raw_input()



