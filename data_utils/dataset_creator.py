import sys
from data_reader import get_team_id_dict, parse_all_stats
from feature_creator import create_game_keys, feat_score_diff

team_ids = get_team_id_dict(sys.argv[1])
gids = create_game_keys(sys.argv[2], team_ids)
raw_data = parse_all_stats(sys.argv[2], gids, team_ids)


feat_score_diff(raw_data)
