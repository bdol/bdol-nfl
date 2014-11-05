def create_gid(year, week, away_team_id, home_team_id):
    return "{0}_{1}_{2}_{3}".format(year, week, away_team_id, home_team_id)

def parse_gid(gid):
    pass