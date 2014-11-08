from feature_creator import parse_gid, feat_score_diff
import ConfigParser
import sys


class Dataset:
    FEATURE_TYPE_RUNNING_AVG = 1
    TARGET_TYPE_SCORE_DIFF = 2

    def print_err(self, msg):
        print >> sys.stderr, msg
        sys.exit(1)

    def __init__(self):
        self.target_type = None
        self.feature_type = None
        self.data = None
        self.data_headers = None

        self.train_start_year = None
        self.train_start_week = None
        self.test_start_year = None
        self.test_start_week = None

        self.raw_and_avg_features = None
        self.features = None

    def gid_in_range(self, gid, start_year, start_week, end_year, end_week):
        gid_vals = parse_gid(gid)
        if int(gid_vals["year"]) < int(start_year):
            return False
        if int(gid_vals["year"]) > int(end_year):
            return False
        if int(gid_vals["week"]) < int(start_week):
            return False
        if int(gid_vals["week"]) > int(end_week):
            return False

        return True

    def date_in_range(self, year, week, start_year, start_week, end_year,
                      end_week):
        if int(year) < int(start_year):
            return False
        if int(year) > int(end_year):
            return False
        if int(week) < int(start_week):
            return False
        if int(week) > int(end_week):
            return False

        return True

    def compute_average_feature_vals(self, raw_data):
        # Initialize dictionaries. Each team has a top-level key. Within each
        # team, we will compute the averages over the features in raw_data.
        self.raw_and_avg_features = dict(raw_data)

        features = raw_data["0"]["2000"]["1"].keys()

        for k_team in sorted(raw_data):
            num_games = 1
            feature_sum = dict((k, 0.0) for k in features)

            for k_year in sorted(self.raw_and_avg_features[k_team]):
                if int(self.train_start_year) <= int(k_year) <= int(
                        self.train_end_year):
                    for k_week in range(1, 18):
                        try:
                            d = self.raw_and_avg_features[k_team][k_year][str(k_week)]
                        except: # bye week
                            self.raw_and_avg_features[k_team][k_year][str(
                                k_week)] = self.raw_and_avg_features[k_team][
                                k_year][str(k_week-1)]
                            continue

                        d["num_games"] = num_games
                        for f in features:
                            # Handle edge cases
                            if f == "Opponent":
                                continue
                            if f == "Date":
                                continue
                            if f == "TeamName":
                                continue

                            if f == "TimePossOff":
                                toks = d[f].split(":")
                                tp = float(toks[0]) + float(toks[1]) / 60.0
                                feature_sum[f] += tp
                                continue
                            if f == "TimePossDef":
                                toks = d[f].split(":")
                                tp = float(toks[0]) + float(toks[1]) / 60.0
                                feature_sum[f] += tp
                                continue
                            if f == "ThirdDownPctOff":
                                pct = float(d[f].replace("%", ""))
                                feature_sum[f] += pct
                                continue
                            if f == "ThirdDownPctDef":
                                pct = float(d[f].replace("%", ""))
                                feature_sum[f] += pct
                                continue

                            try:
                                feature_sum[f] += float(d[f])
                            except:
                                continue

                            d["avg_{0}".format(f)] = feature_sum[f] / float(
                                num_games)

    """
    Computed features include the stats up to the last week (we don't know
    the current week's stats yet).
    """
    def compute_features(self, include_features, gids):
        inc_feats = sorted(include_features)

        self.features = dict()
        for gid in gids:
            if self.gid_in_range(gid, self.train_start_year,
                                 self.train_start_week, self.train_end_year,
                                 self.train_end_week):
                vals = parse_gid(gid)
                if vals["week"] == "1":
                    continue

                vals["week"] = str(int(vals["week"]) - 1)

                self.features[gid] = dict()

                away_d = self.raw_and_avg_features[vals["away_team_id"]][vals[
                    "year"]][vals["week"]]
                home_d = self.raw_and_avg_features[vals["home_team_id"]][vals[
                    "year"]][vals["week"]]

                this_week = str(int(vals["week"])+1)
                away_score = self.raw_and_avg_features[vals["away_team_id"]][
                    vals["year"]][this_week]["ScoreOff"]
                home_score = self.raw_and_avg_features[vals["home_team_id"]][vals[
                    "year"]][this_week]["ScoreOff"]

                self.features[gid]["t_score_diff"] = float(home_score) - float(
                    away_score)
                self.features[gid]["t_home_team_won"] = "1" if float(
                    home_score) > float(away_score) else "0"

                for f in inc_feats:
                    if f == "c_away_team_id":
                        self.features[gid][f] = vals["away_team_id"]
                    if f == "c_home_team_id":
                        self.features[gid][f] = vals["home_team_id"]

                    if f == "n_game_week":
                        self.features[gid][f] = str(int(vals["week"]) + 1)

                    if f == "n_off_score_diff":
                        self.features[gid][f] = float(home_d["avg_ScoreOff"])\
                                                - float(away_d["avg_ScoreOff"])
                    if f == "n_def_score_diff":
                        self.features[gid][f] = float(home_d["avg_ScoreDef"]) \
                                                - float(away_d["avg_ScoreDef"])

                    if f == "n_off_rush_yds_diff":
                        self.features[gid][f] = float(home_d[
                            "avg_RushYdsOff"]) - float(away_d["avg_RushYdsOff"])
                    if f == "n_def_rush_yds_diff":
                        self.features[gid][f] = float(home_d[
                            "avg_RushYdsDef"]) - float(away_d["avg_RushYdsDef"])

                    if f == "n_off_pass_yds_diff":
                        self.features[gid][f] = float(home_d[
                            "avg_PassYdsOff"]) - float(away_d["avg_PassYdsOff"])
                    if f == "n_def_pass_yds_diff":
                        self.features[gid][f] = float(home_d[
                            "avg_PassYdsDef"]) - float(away_d["avg_PassYdsDef"])


    def create_dataset(self, conf_filename, team_ids, gids, raw_data):
        self.data = dict((k, None) for k in gids)
        self.data_headers = ["gid"]

        cfg = ConfigParser.ConfigParser()
        cfg.read(conf_filename)

        # Set the feature type
        if cfg.get("dataset", "feature_type") == "running_average":
            self.feature_type = self.FEATURE_TYPE_RUNNING_AVG
        else:
            self.print_err("Error: unrecognized feature type {0}".format(
                cfg.get("dataset", "feature_type")))

        # Set the target type
        if cfg.get("dataset", "target_type") == "score_diff":
            self.target_type = self.TARGET_TYPE_SCORE_DIFF
        else:
            self.print_err("Error: unrecognized target {0}".format(
                cfg.get("dataset", "target")))

        # Figure out the ranges for training and testing
        train_start = cfg.get("dataset", "train_start").split(",")
        self.train_start_year = train_start[0]
        self.train_start_week = train_start[1]
        train_end = cfg.get("dataset", "train_end").split(",")
        self.train_end_year = train_end[0]
        self.train_end_week = train_end[1]
        test_start = cfg.get("dataset", "test_start").split(",")
        self.test_start_year = test_start[0]
        self.test_start_week = test_start[1]
        test_end = cfg.get("dataset", "test_end").split(",")
        self.test_end_year = test_end[0]
        self.test_end_week = test_end[1]

        self.compute_average_feature_vals(raw_data)
        self.compute_features(cfg.options("features"), gids)

        self.write_dataset("../data/datasets/trainupto2013_test2013/train.csv")


    def write_dataset(self, filename):
        f = open(filename, "w")

        headers_written = False
        for k in sorted(self.features):
            headers = sorted(self.features[k])
            headers.remove("t_score_diff")
            headers.remove("t_home_team_won")

            if not headers_written:
                f.write("gid")
                f.write("\tt_score_diff")
                f.write("\thome_team_won")
                for h in headers:
                    f.write("\t{0}".format(h))
                f.write("\n")
                headers_written = True

            f.write("{0}".format(k))
            f.write("\t{0}".format(self.features[k]["t_score_diff"]))
            f.write("\t{0}".format(self.features[k]["t_home_team_won"]))
            for h in headers:
                f.write("\t{0}".format(self.features[k][h]))

            f.write("\n")


        f.close()

    def read_dataset(self, filename):
        pass
