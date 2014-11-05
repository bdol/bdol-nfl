import sys

team_list_f = open(sys.argv[1])

team_names = []
for line in team_list_f:
    team_names.append(line.rstrip())
team_list_f.close()

team_names.sort()


team_ids_f = open(sys.argv[2], "w")
id = 0
for team_name in team_names:
    team_ids_f.write("{0}\t{1}\n".format(team_name, id))
    id += 1

team_ids_f.close()
