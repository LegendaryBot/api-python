import json

import requests


def get_overwatch_stats(event,context):
    battletag = event['pathParameters']['battletag']
    region = event['pathParameters']['region'].lower()
    r = requests.get("https://owapi.net/api/v3/u/%s/stats" % battletag, headers={
        "User-Agent": "LegendaryBot API v2"
    })
    jsonEntry = r.json()
    if region in jsonEntry and jsonEntry[region]['stats']['competitive']:
        competitive_stats = jsonEntry[region]['stats']['competitive']['overall_stats']
        embed = {
            "title": "Player %s Overwatch %s Stats" % (battletag, region.upper()),
            "fields": [
                {
                    "name": "Rank",
                    "value": "%s (%s)" % (competitive_stats['tier'], competitive_stats['comprank']),
                    "inline": True
                },
                {
                    "name": "Wins",
                    "value": competitive_stats['wins'],
                    "inline": True
                },
                {
                    "name": "Losses",
                    "value": competitive_stats['losses'],
                    "inline": True
                },
                {
                    "name": "Ties",
                    "value": competitive_stats['ties'],
                    "inline": True
                },
                {
                    "name": "Win Rate",
                    "value": "%s %%" % competitive_stats['win_rate'],
                    "inline": True
                }
            ],
            "thumbnail": {
                "url": competitive_stats['avatar']
            }
        }

        return {
            "statusCode": 200,
            "body": json.dumps(embed)
        }

    return {
        "statusCode": 404
    }


