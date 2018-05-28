import requests
import os

from requests_oauthlib import OAuth2Session

from discord.colour import Colour
from discord.discorduser import DiscordUser
from wow.wowcharacter import WoWCharacter


def get_server_status_embed(region, realm):
    r = requests.get('https://%s.api.battle.net/wow/realm/status' % region,
                     params={"realms": realm, "apikey": os.getenv("US_KEY")})
    json = r.json()
    if "realms" in json and json['realms']:
        realm_json = json['realms'][0]
        embed = {
            "color": Colour.green().value if realm_json['status'] else Colour.red().value,
            "title": "%s - %s" % (realm_json['name'], region.upper()),
            "fields": [
                {
                    "name": "Status",
                    "value": "Online" if realm_json['status'] else "Offline",
                    "inline": True
                },
                {
                    "name": "Population",
                    "value": realm_json['population'],
                    "inline": True
                },
                {
                    "name": "Currently a Queue?",
                    "value": "Yes" if realm_json['queue'] else "No",
                    "inline": True
                }
            ]
        }
        return embed


def get_battlenet_oauth_login(event, context):
    region = event['pathParameters']['region']
    id = event['pathParameters']['id']
    scope = ["wow.profile"]
    redirect_uri = "https://api-dev.legendarybot.info/v2/oauth/battlenetcallback"
    oauth = OAuth2Session(os.getenv("US_KEY"), redirect_uri=redirect_uri, scope=scope)
    auth_url, state = oauth.authorization_url("https://%s.battle.net/oauth/authorize" % region, state="%s:%s" % (region, id))
    print("auth url: %s" % auth_url)
    return {
        "statusCode": 302,
        "headers": {
            "Location": auth_url
        }

    }


def get_battlnet_oauth_callback(event,context):
    code = event['queryStringParameters']['code']

    state = event['queryStringParameters']['state']
    region, id = state.split(":")[0]
    scope = ["wow.profile"]
    redirect_uri = "https://api-dev.legendarybot.info/v2/oauth/battlenetcallback"
    oauth = OAuth2Session(os.getenv("US_KEY"), redirect_uri=redirect_uri, scope=scope)
    oauth.fetch_token("https://%s.battle.net/oauth/token" % region, code=code, client_secret=os.getenv("US_SECRET"))
    r = oauth.get("https://%s.api.battle.net/wow/user/characters" % region)
    jsonEntry = r.json()
    character_array = []
    if 'characters' in jsonEntry:
        for character in jsonEntry['characters']:
            if 'guild' in character:
                character_array.append(WoWCharacter(region, character['realm'].lower(),character['name'], character['guild']))
            else:
                character_array.append(WoWCharacter(region, character['realm'].lower(),character['name']))
    du = DiscordUser(id)
    for character in du.compare_characters(character_array):
        du.remove_character(character)