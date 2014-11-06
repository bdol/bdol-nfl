from dateutil import parser
from feature_creator import create_gid
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
def parse_all_stats(directory, gids, team_ids):
    # First get the first week number of all seasons
    first_weeks = dict()
    first_week_f = csv.reader(open(os.path.abspath(directory)+'/first_weeks.tsv'), delimiter='\t')
    for row in first_week_f:
        first_weeks[row[0]] = int(row[1])

    data_files = glob.glob(os.path.abspath(directory)+'/*stats.tsv')

    raw_data = dict()
    for filename in data_files:
        matches = re.findall(r'\d{4}', filename)
        year = matches[0]
        reader = csv.DictReader(open(filename), delimiter='\t')
        for row in reader:
            date = parser.parse(row["Date"])
            week = date.isocalendar()[1]
            day = date.isocalendar()[2]

            nfl_week = week - first_weeks[year] + 1
            if day == 1 or day == 2: # Monday night game (or that weird Tuesday Philly game)
                nfl_week -= 1
            if nfl_week > 17 or nfl_week < 1:
                continue


            team_1_id = team_ids[row["TeamName"]]
            team_2_id = team_ids[row["Opponent"]]

            gid = create_gid(year, nfl_week, team_1_id, team_2_id)
            if gid in gids:
                raw_data[gid] = row

    return raw_data

