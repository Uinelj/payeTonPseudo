# coding: utf-8
import requests
import json
import os.path

global DEBUG
global DB

DEBUG = True
DB = './db.json'
key_file = '/home/uj/dev/apis/keys.json'
if os.path.isfile(key_file): #TODO: Gérer file not found
    api_file = open(key_file, 'r')
    API_KEYS = json.loads(api_file.read())
class ChampionEntry():
    def __init__(self, champion_id, first_summoner_name):
        self.champion_id = champion_id
        self.summoner_list = [first_summoner_name]
    def get_champion_id(self):
        return self.champion_id
    def append(self, summoner_name):
        self.summoner_list.append(summoner_name)
    def get_summoner_list(self):
        return self.summoner_list
class Participant():
    def __init__(self, champion_id, summoner_name):
        self.champion_id = champion_id
        self.summoner_name = summoner_name
    def get_summoner_name(self):
        return self.summoner_name
    def get_champion_id(self):
        return self.champion_id
class Champions():
    """docstring for champions"""
    def __init__(self):
        if DEBUG:
            champion_list = open('dbg_champs.json', 'r')
            self.champions = json.loads(champion_list.read())
        else:
            req = "https://global.api.pvp.net/api/lol/static-data/na/v1.2/champion?dataById=true&api_key=" + API_KEYS['lol']
            self.champions = requests.get(req).json()
    def get_champion(self, id):
        return self.champions['data'][id]['name']
class FeaturedGames():
    def __init__(self):
        self.participant_list = []
        champions = Champions()
        if DEBUG:
            game_list = open('dbg_fgames.json', 'r')
            self.games = json.loads(game_list.read())
        else:
            req = "https://euw.api.pvp.net/observer-mode/rest/featured?api_key=" + API_KEYS['lol']
            self.games = requests.get(req).json()
        #print self.games['gameList']
        for game in self.games['gameList']:
            if game['gameMode'] == 'CLASSIC' and game['gameType'] == 'MATCHED_GAME':
                print "ID de game : %s" % game['gameId']
                for participant in game['participants']:
                    #print participant['summonerName']
                    #print u'%s joue %s' % (participant['summonerName'].encode('utf-8'), champions.get_champion(str(participant['championId'])))
                    #print(participant['summonerName'], "est en train de jouer", champions.get_champion(str(participant['championId'])))
                    self.participant_list.append(Participant(participant['championId'], participant['summonerName'].encode('utf-8')))
    def get_participants(self):
        return self.participant_list
class Db():
    def __init__(self):
        db_path = 'db.json'
        # if os.path.isfile(db_path): #TODO: Gérer file not found
        #     db_file = open(db_path, 'r')
        #     API_KEYS =json.loads(db_file.read())
        self.champion_entries = {}
        self.champions = Champions()
    def add_participant(self, participant):
        #print("On va add dans les entrées du champion d'ID ", participant.get_champion_id())
        #TODO: recup le CHampionEntry si il existe dans le dict
        # if participant.get_champion_id() in self.champion_entries:
        #     self.champion_entries[participant.get_champion_id()].append(participant.get_summoner_name)
        # else:
        #     self.champion_entries[participant.get_champion_id()] = ChampionEntry(participant.get_champion_id(), participant.get_summoner_name())
        if participant.get_champion_id() in self.champion_entries:
            tmp = self.champion_entries[participant.get_champion_id()]
            tmp.append(participant.get_summoner_name())
            self.champion_entries[participant.get_champion_id()] = tmp
        else:
            self.champion_entries[participant.get_champion_id()] = [participant.get_summoner_name()]
    def display_all(self):
        for key, champion_entry in self.champion_entries.iteritems():
            print(self.champions.get_champion(str(key)))
            print(champion_entry)
    def display_names(self, champion_id):
        for name in self.champion_entries[str(champion_id)].get_summoner_name():
            print(name)
    def get_champion_entries(self):
        return self.champion_entries
# class db():
#     def __init__(self):
#         if os.path.isfile(db): #TODO: Gérer file not found
#             db_file = open(db, 'r')
#             self.db = json.loads(db_file.read())
#
#champions = Champions()
featured_games = FeaturedGames()
db = Db()
part = featured_games.get_participants()
for parti in part:
    db.add_participant(parti)

db.display_all()

ce = ChampionEntry(1, "Supersuceur")
print(json.dumps(ce.__dict__))
#print champions.get_champion(str(2))
# print "URL of the request, getting basic information"
# url = "https://global.api.pvp.net/api/lol/static-data/na/v1.2/champion?dataById=true&api_key=" + API_KEYS['lol']
# ids_champs = requests.get(url)
# print url
# print "Result of the request"
# if ids_champs.ok :
#     j_data = json.loads(ids_champs.content)
#     print j_data
