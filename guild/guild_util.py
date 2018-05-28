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
