import csv
import glob
import os
import re

def create_gid(year, week, away_team_id, home_team_id):
    return "{0}_{1}_{2}_{3}".format(year, week, away_team_id, home_team_id)

def parse_gid(gid):
    toks = gid.split("_")
    vals = dict()
    vals["year"] = toks[0]
    vals["week"] = toks[1]
    vals["away_team_id"] = toks[2]
    vals["home_team_id"] = toks[3]
    return vals

def create_game_keys(directory, team_ids):
    data_files = glob.glob(os.path.abspath(directory)+'/*games.tsv')
    gids = []

    for filename in data_files:
        matches = re.findall(r'\d{4}', filename)
        year = matches[0]
        reader = csv.DictReader(open(filename), delimiter='\t')

        for row in reader:
            away_team_id = None
            home_team_id = None
            if row["Away"] == "@":
                away_team_id = team_ids[row["Winner/tie"]]
                home_team_id = team_ids[row["Loser/tie"]]
            else:
                home_team_id = team_ids[row["Winner/tie"]]
                away_team_id = team_ids[row["Loser/tie"]]

            week = row["Week"]
            gid = create_gid(year, week, away_team_id, home_team_id)
            gids.append(gid)

    return gids

def feat_score_diff(raw_data):
    score_diff = dict()
    for k,v in raw_data.iteritems():
        score_diff[k] = int(v["ScoreOff"]) - int(v["ScoreDef"])

    return score_diff
