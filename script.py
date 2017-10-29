import requests
import json
import csv

api_key = "UDGc32qk8z0fXvxtpngsrNC5OoF9IYmJ"

def get_team_games(team_abbrv):
    array = []
    for i in range(2016, 2017):
        temp = get_team_useful_stuff(team_abbrv, i)
        for elements in temp:
            array.append(elements)
    return array

def get_all_team_games():
    teams = get_all_teams_ids()
    
    games = []

    for team_info in teams:
        arrays = (get_team_games(team_info["abbreviation"]))
        for element in arrays:
            games.append(element)
    #games = {value["game_id"]:value for value in games}.values()
    games = sorted(games, key=lambda k : k["game_id"])

def get_game_results(team_id, season):
    team_id = get_team_id(team_id)
    url = "http://api.probasketballapi.com/boxscore/team"
    payload = {
        "api_key": api_key,
        "team_id": team_id,
        "season": season
    }
    response = requests.post(url=url, params=payload).json()
    response = sorted(response, key=lambda k : k["game_id"])
    return response
 
def get_team_head_to_head(abbrev, season):
    teams = get_all_teams_ids()
    team_ids = [team_info["id"] for team_info in teams]
    number_of_games_played = dict.fromkeys(["2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017"])
    number_of_games_played["2010"] = dict.fromkeys(team_ids)
    number_of_games_played["2011"] = dict.fromkeys(team_ids)
    number_of_games_played["2012"] = dict.fromkeys(team_ids)
    number_of_games_played["2013"] = dict.fromkeys(team_ids)
    number_of_games_played["2014"] = dict.fromkeys(team_ids)
    number_of_games_played["2015"] = dict.fromkeys(team_ids)
    number_of_games_played["2016"] = dict.fromkeys(team_ids)
    number_of_games_played["2017"] = dict.fromkeys(team_ids)

    games = get_team_games(abbrev)
    results = get_game_results(abbrev, season)
    head_to_head = []
    counter = 0

    for game in games:
        print("Starting {0} of {1}:".format(int(counter)+1, len(games)))
        team_id = game["team_id"]
        opponent_id = game["opponent_id"]
        season = game["season"]
        teama = get_team_summary(team_id, season) if (number_of_games_played[season][team_id] is not None) else get_team_summary(team_id, int(season)-1)
        teamb = get_team_summary(opponent_id, season) if (number_of_games_played[season][opponent_id] is not None) else get_team_summary(opponent_id, int(season)-1)
        teama_gamesplayed = number_of_games_played[season][team_id] if (number_of_games_played[season][team_id] is not None) else 82
        teamb_gamesplayed = number_of_games_played[season][opponent_id] if (number_of_games_played[season][opponent_id] is not None) else 82
        number_of_games_played[season][team_id] = teama_gamesplayed + 1 if (number_of_games_played[season][team_id] is not None) else 1
        number_of_games_played[season][opponent_id] = teamb_gamesplayed + 1 if (number_of_games_played[season][opponent_id] is not None) else 1
        teama = get_season_averages(teama[:teama_gamesplayed], True)
        teamb = get_season_averages(teamb[:teamb_gamesplayed], False)
        winner = "Yes" if (int(results[counter]["plus_minus"]) > 0) else "No"
        teama.update(teamb)
        teama["winner"] = winner
        teama["teama_id"] = team_id
        teama["teamb_id"] = opponent_id
        teama.update(results[counter])
        home_team = get_home_team(game["game_id"])
        teama["teama_net_rating"] = teama["teama_off_rating"] - teama["teama_def_rating"] + 3 if (home_team == teama["teama_id"]) else teama["teama_off_rating"] - teama["teama_def_rating"]
        teama["teamb_net_rating"] = teamb["teamb_off_rating"] - teama["teamb_def_rating"] + 3 if (home_team == teama["teamb_id"]) else teamb["teamb_off_rating"] - teamb["teamb_def_rating"]
        print("Done with {0}, printing response:".format(int(counter)+1))
        print(str(teama))
        head_to_head.append(list(teama.values()))
        counter += 1

    return head_to_head

def get_home_team(game_id):
    url = "http://api.probasketballapi.com/game"
    payload = {
        "api_key": api_key,
        "game_id": game_id
    }
    response = requests.post(url=url, params=payload).json()
    return response[0]["home_id"]

def get_head_to_head():
    game_data = open('/tmp/GameData.csv', 'w')
    csvwriter = csv.writer(game_data)
    header = ["teama_off_rating", "teama_def_rating", "teama_ast_pct", "teama_ast_tov", "teama_ast_ratio", "teama_oreb_pct", "teama_dreb_pct", "teama_treb_pct", "teama_tm_tov_pct", "teama_efg_pct", "teama_ts_pct", "teama_usg_pct", "teama_pace", "teama_pie", "teamb_off_rating", "teamb_def_rating", "teamb_ast_pct", "teamb_ast_tov", "teamb_ast_ratio", "teamb_oreb_pct", "teamb_dreb_pct", "teamb_treb_pct", "teamb_tm_tov_pct", "teamb_efg_pct", "teamb_ts_pct", "teamb_usg_pct", "teamb_pace", "teamb_pie", "winner", "teama_id", "teamb_id"]
    csvwriter.writerow(header)
    teams = get_all_teams_ids()
    team_ids = [team_info["id"] for team_info in teams]
    number_of_games_played = dict.fromkeys(["2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017"])
    number_of_games_played["2010"] = dict.fromkeys(team_ids)
    number_of_games_played["2011"] = dict.fromkeys(team_ids)
    number_of_games_played["2012"] = dict.fromkeys(team_ids)
    number_of_games_played["2013"] = dict.fromkeys(team_ids)
    number_of_games_played["2014"] = dict.fromkeys(team_ids)
    number_of_games_played["2015"] = dict.fromkeys(team_ids)
    number_of_games_played["2016"] = dict.fromkeys(team_ids)
    number_of_games_played["2017"] = dict.fromkeys(team_ids)

    games = get_all_team_games()
    head_to_head = []

    for i in games:
        print(str(i))
    for game in games:
        team_id = game["team_id"]
        opponent_id = game["opponent_id"]
        season = game["season"]
        teama = get_team_summary(team_id, season) if (number_of_games_played[season][team_id] is not None) else get_team_summary(team_id, int(season)-1)
        teamb = get_team_summary(opponent_id, season) if (number_of_games_played[season][opponent_id] is not None) else get_team_summary(opponent_id, int(season)-1)
        teama_gamesplayed = number_of_games_played[season][team_id] if (number_of_games_played[season][team_id] is not None) else 82
        teamb_gamesplayed = number_of_games_played[season][opponent_id] if (number_of_games_played[season][opponent_id] is not None) else 82
        number_of_games_played[season][team_id] = teama_gamesplayed + 1 if (number_of_games_played[season][team_id] is not None) else 1
        number_of_games_played[season][opponent_id] = teamb_gamesplayed + 1 if (number_of_games_played[season][opponent_id] is not None) else 1
        teama = get_season_averages(teama[:teama_gamesplayed], True)
        teamb = get_season_averages(teamb[:teamb_gamesplayed], False)
        winner = "Yes" if (game["off_rating"] > game["def_rating"]) else "No"
        teama.update(teamb)
        teama["winner"] = winner
        teama["teama_id"] = team_id
        teama["teamb_id"] = opponent_id
        head_to_head.append(teama)
    print(str(head_to_head))
    csvwriter.writerow(head_to_head)

        
def get_season_averages(array, boolean):
    averages = ["off_rating","def_rating","ast_pct","ast_tov","ast_ratio","oreb_pct","dreb_pct","treb_pct","tm_tov_pct","efg_pct","ts_pct","usg_pct","pace","pie"]

    array = [[float(row[averages[i]]) for row in array] for i in range(len(averages))]
    array = [sum(row)/len(row) for row in array]

    current_season_stats = {}
    averages = ["teama_"+key for key in averages] if (boolean is True) else ["teamb_"+key for key in averages]
    for i in range(len(averages)):
        current_season_stats[averages[i]] = array[i]

    return current_season_stats

def get_all_teams_ids():
    url = "http://api.probasketballapi.com/team"
    payload = {
        "api_key": api_key
    }
    response = requests.post(url=url, params=payload)
    return response.json()

def get_team_useful_stuff(team_abbrv, season):
    team_id = get_team_id(team_abbrv)
    team_json = get_team_summary(team_id, season)
    return team_json

def get_team_summary(team_id, season):
    assert(team_id is not None)
    assert(season is not None)
    url = "http://api.probasketballapi.com/advanced/team"
    payload = {
        "api_key": api_key,
        "team_id": team_id,
        "season": season
    }
    response = requests.post(url=url, params=payload).json()
    return response

def get_team_id(abbreviation):
    assert(abbreviation)
    url = "http://api.probasketballapi.com/team"
    payload = {
        "api_key": api_key,
        "team_abbrv": abbreviation
    }
    team_id = requests.post(url=url, params=payload).json()[0]["id"]
    return team_id


the_json = get_all_teams_ids()
ids = [the_json[i]["abbreviation"] for i in range(len(the_json))]
game_data = open('csvfile.csv', 'w')
csvwriter = csv.writer(game_data)
header = ["teama_off_rating", "teama_def_rating", "teama_ast_pct", "teama_ast_tov", "teama_ast_ratio", "teama_oreb_pct", "teama_dreb_pct", "teama_treb_pct", "teama_tm_tov_pct", "teama_efg_pct", "teama_ts_pct", "teama_usg_pct", "teama_pace", "teama_pie", "teamb_off_rating", "teamb_def_rating", "teamb_ast_pct", "teamb_ast_tov", "teamb_ast_ratio", "teamb_oreb_pct", "teamb_dreb_pct", "teamb_treb_pct", "teamb_tm_tov_pct", "teamb_efg_pct", "teamb_ts_pct", "teamb_usg_pct", "teamb_pace", "teamb_pie", "winner", "teama_id", "teamb_id", "game_id", "team_id", "opponent_id", "period", "season", "min", "fgm", "fga", "fg3m", "fg3a", "ftm", "fta", "oreb", "dreb", "ast", "blk", "stl", "to", "pf", "pts", "plus_minus", "teama_net_rating", "teamb_net_rating"]
csvwriter.writerow(header)

for i in ids:
    array = get_team_head_to_head(i, 2016)
    for elements in array:
        csvwriter.writerow(elements)
