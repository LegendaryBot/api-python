import datetime
import json
import os

import requests

import guild.guild_setting as gs
from utils.simple_utc import simple_utc


def get_guild_latest_log(event, context):
    guild_id = event['pathParameters']['guildId']
    region = gs.get_setting(guild_id, "WOW_REGION_NAME")
    server = gs.get_setting(guild_id, "WOW_SERVER_NAME")
    guild = gs.get_setting(guild_id, "GUILD_NAME")
    if region['statusCode'] == 200 and server['statusCode'] == 200 and guild['statusCode'] == 200:
        r = requests.get("https://www.warcraftlogs.com/v1/reports/guild/%s/%s/%s" % (guild['body']['value'], server['body']['value'], region['body']['value']), params={"api_key": os.getenv("WARCRAFTLOGS_KEY")})
        logsList = r.json()
        try:
            lastEntry = logsList[-1]
        except IndexError as e:
            print(e)
            body = {
                "error": "Guild not found"
            }
            response = {
                "statusCode": 404,
                body: json.dumps(body)
            }
            return response
        else:
            date = datetime.datetime.utcfromtimestamp(lastEntry["start"] / 1000)
            date = date.replace(tzinfo=simple_utc())
            date.isoformat()
            zones = requests.get("https://www.warcraftlogs.com/v1/zones", params={"api_key": os.getenv("WARCRAFTLOGS_KEY")})
            zones_json = zones.json()
            embed = {
                "title": lastEntry["title"],
                "url": "https://www.warcraftlogs.com/reports/%s" % lastEntry['id'],
                "thumbnail": {
                    "url": "https://www.warcraftlogs.com/img/icons/warcraft/zone-%s-small.jpg" % lastEntry['zone']
                },
                "timestamp": date.isoformat(),
                "fields": [
                    {
                        "name": "Created by",
                        "value": lastEntry['owner'],
                        "inline": True
                    }
                ]
            }
            for zone in zones_json:
                if lastEntry['zone'] == zone['id']:
                    embed['fields'].append({
                        "name": "Zone",
                        "value": zone['name'],
                        "inline": True
                    })
            print(embed)
            response = {
                "statusCode": 200,
                "body": json.dumps(embed)
            }
            return response


def get_guild_raid_rank(event,context):
    guild_id = event['pathParameters']['guildId']
    region = gs.get_setting(guild_id, "WOW_REGION_NAME")
    server = gs.get_setting(guild_id, "WOW_SERVER_NAME")
    guild = gs.get_setting(guild_id, "GUILD_NAME")
    query_parameters = {
        "region": region['body']['value'],
        "realm": server['body']['value'],
        "name": guild['body']['value'],
        "fields": "raid_rankings"
    }
    r = requests.get("https://raider.io/api/v1/guilds/profile", query_parameters)
    json_entry = r.json()
    if "error" not in json_entry:
            raid_rankings = json_entry['raid_rankings']
            embed = {
                "title": "%s-%s Raid Rankings" % (query_parameters['name'], query_parameters['realm']),
                "fields": [
                    {
                        "name": "Antorus The Burning Throne",
                        "value": __format_ranking(raid_rankings['antorus-the-burning-throne']),
                        "inline": True
                    },
                    {
                        "name": "Tomb of Sargeras",
                        "value": __format_ranking(raid_rankings['tomb-of-sargeras']),
                        "inline": True
                    },
                    {
                        "name": "The Nighthold",
                        "value": __format_ranking(raid_rankings['the-nighthold']),
                        "inline": True
                    },
                    {
                        "name": "Trial of Valor",
                        "value": __format_ranking(raid_rankings['trial-of-valor']),
                        "inline": True
                    },
                    {
                        "name": "The Emerald Nightmare",
                        "value": __format_ranking(raid_rankings['the-emerald-nightmare']),
                        "inline": True
                    }
                ]
            }
            return {
                "statusCode": 200,
                "body": json.dumps(embed)
            }
    return {
        "statusCode": 404
    }


def __format_ranking(raid_json):
    return_string = ""
    normal = raid_json['normal']
    heroic = raid_json['heroic']
    mythic = raid_json['mythic']
    if normal['world'] != 0 and heroic['world'] == 0 and mythic['world'] == 0:
        return_string += "**Normal**\n"
        return_string += __sub_format_ranking(normal)
    elif heroic['world'] != 0 and mythic['world'] == 0:
        return_string += "\n**Heroic**\n"
        return_string += __sub_format_ranking(heroic)
    elif mythic['world'] != 0:
        return_string += "\n**Mythic**\n"
        return_string += __sub_format_ranking(mythic)
    else:
        return_string += __sub_format_ranking(None)
    return return_string


def __sub_format_ranking(difficulty):
    if difficulty is not None:
        ranking = "World: **%s**\n" % difficulty['world']
        ranking += "Region: **%s**\n" % difficulty['region']
        ranking += "Realm: **%s**\n" % difficulty['realm']
    else:
        ranking = "**Not started**\n"
    return ranking
