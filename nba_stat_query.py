from nba_api.stats.static import players
from nba_api.stats.endpoints import playerfantasyprofile
import json as js

#This will retreive all current active players
def retrieve_all_players():

    nba_roster = []
    player = players.get_active_players()

    for player_id in player:
        nba_roster.append(player_id['id'])
    return nba_roster


#This will retrieve all active player stats in the season and dump them into a JSON file
def get_player_stats(nba_season):

    all_player_stats = []
    for nba_player in nba_roster:
        s = players.find_player_by_id(nba_player)
        print(s['full_name'])

        try:
            x = playerfantasyprofile.PlayerFantasyProfile(per_mode36="PerGame", plus_minus_no="N", rank_no="N",
                                                          season= nba_season, player_id=nba_player)
            z = x.get_normalized_dict()
            b = z['Overall']
            b[0]['Name'] = s['full_name']
            all_player_stats.append(b[0])

        except:
            pass

    with open("nba_stats.json", "w") as outfile:
        js.dump(all_player_stats, outfile)


