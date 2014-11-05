import sys
from data_reader import get_team_id_dict, parse_all_stats

team_ids = get_team_id_dict(sys.argv[1])
parse_all_stats(sys.argv[2], team_ids)
