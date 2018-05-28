import json

import requests
from requests_html import HTMLSession

from discord.colour import Colour


def get_token_price(event, context):
    region = event['pathParameters']['region']
    region = "NA" if region.casefold() == "US".casefold() else region
    r = requests.get("https://data.wowtoken.info/snapshot.json")
    jsonEntry = r.json()
    print(jsonEntry)
    if region in jsonEntry:
        region_json = jsonEntry[region]['formatted']
        embed = {
            "title": "Price for 1 WoW Token in the %s region" % region,
            "thumbnail": {
                "url": "http://wow.zamimg.com/images/wow/icons/large/wow_token01.jpg"
            },
            "color": Colour.from_rgb(255, 215, 0).value,
            "fields": [
                {
                    "name": "Current Price",
                    "value": region_json['buy'],
                    "inline": True
                },
                {
                    "name": "Minimum 24H",
                    "value": region_json['24min'],
                    "inline": True
                },
                {
                    "name": "Maximum 24H",
                    "value": region_json['24max'],
                    "inline": True
                },
                {
                    "name": "Percentage 24H range",
                    "value": "%s %%" % region_json['24pct'],
                    "inline": True
                }
            ],
            "footer": {
                "text": "Information taken from https://wowtoken.info",
                "icon_url": "http://wow.zamimg.com/images/wow/icons/large/wow_token01.jpg"
            }
        }
        response = {
            "statusCode": 200,
            "body": json.dumps(embed)
        }
        return response
    response = {
        "statusCode": 404
    }
    return response


def get_legion_building(event, context):
    region = event['pathParameters']['region'].lower()
    session = HTMLSession()
    r = session.get("https://wowhead.com")
    # .attrs['style'].split("(")[1].split(")")[0].replace("//", "https://")
    status = r.html.find(".tiw-bs-status")
    states = r.html.find(".tiw-bs-status-state")
    percents = r.html.find(".tiw-bs-status-progress")
    if region == "us":
        embed = {
            "title": "Broken Shore Building Status",
            "fields": [
                {
                    "name": "Mage Tower",
                    "value": "%s - %s" % (states[0].text, percents[0].text),
                    "inline": True
                },
                {
                    "name": "Command Center",
                    "value": "%s - %s" % (states[1].text, percents[1].text),
                    "inline": True
                },
                {
                    "name": "Nether Disruptor",
                    "value": "%s - %s" % (states[2].text, percents[2].text),
                    "inline": True
                }
            ]
        }
        if states[0].text == "Completed":
            embed["color"] = Colour.green().value
            embed['image'] = {
                "url": status[0].attrs['style'].split("(")[1].split(")")[0].replace("//", "https://")
            }
        elif states[1].text == "Completed":
            embed["color"] = Colour.green().value
            embed['image'] = {
                "url": status[1].attrs['style'].split("(")[1].split(")")[0].replace("//", "https://")
            }
        elif states[2].text == "Completed":
            embed["color"] = Colour.green().value
            embed['image'] = {
                "url": status[2].attrs['style'].split("(")[1].split(")")[0].replace("//", "https://")
            }
        elif states[0].text == "Under Attack":
            embed["color"] = Colour.from_rgb(255, 255, 0).value
            embed['image'] = {
                "url": status[0].attrs['style'].split("(")[1].split(")")[0].replace("//", "https://")
            }
        elif states[1].text == "Under Attack":
            embed["color"] = Colour.from_rgb(255, 255, 0).value
            embed['image'] = {
                "url": status[1].attrs['style'].split("(")[1].split(")")[0].replace("//", "https://")
            }
        elif states[2].text == "Under Attack":
            embed["color"] = Colour.from_rgb(255, 255, 0).value
            embed['image'] = {
                "url": status[2].attrs['style'].split("(")[1].split(")")[0].replace("//", "https://")
            }
        else:
            embed["color"] = Colour.red().value
            embed['image'] = {
                "url": status[0].attrs['style'].split("(")[1].split(")")[0].replace("//", "https://")
            }
    else:
        embed = {
            "title": "Broken Shore Building Status",
            "fields": [
                {
                    "name": "Mage Tower",
                    "value": "%s - %s" % (states[3].text, percents[3].text),
                    "inline": True
                },
                {
                    "name": "Command Center",
                    "value": "%s - %s" % (states[4].text, percents[4].text),
                    "inline": True
                },
                {
                    "name": "Nether Disruptor",
                    "value": "%s - %s" % (states[5].text, percents[5].text),
                    "inline": True
                }
            ]
        }
        if states[3].text == "Completed":
            embed["color"] = Colour.green().value
            embed['image'] = {
                "url": status[3].attrs['style'].split("(")[1].split(")")[0].replace("//", "https://")
            }
        elif states[4].text == "Completed":
            embed["color"] = Colour.green().value
            embed['image'] = {
                "url": status[4].attrs['style'].split("(")[1].split(")")[0].replace("//", "https://")
            }
        elif states[5].text == "Completed":
            embed["color"] = Colour.green().value
            embed['image'] = {
                "url": status[5].attrs['style'].split("(")[1].split(")")[0].replace("//", "https://")
            }
        elif states[3].text == "Under Attack":
            embed["color"] = Colour.from_rgb(255, 255, 0).value
            embed['image'] = {
                "url": status[3].attrs['style'].split("(")[1].split(")")[0].replace("//", "https://")
            }
        elif states[4].text == "Under Attack":
            embed["color"] = Colour.from_rgb(255, 255, 0).value
            embed['image'] = {
                "url": status[4].attrs['style'].split("(")[1].split(")")[0].replace("//", "https://")
            }
        elif states[5].text == "Under Attack":
            embed["color"] = Colour.from_rgb(255, 255, 0).value
            embed['image'] = {
                "url": status[5].attrs['style'].split("(")[1].split(")")[0].replace("//", "https://")
            }
        else:
            embed["color"] = Colour.red().value
            embed['image'] = {
                "url": status[3].attrs['style'].split("(")[1].split(")")[0].replace("//", "https://")
            }
    return {
        "statusCode": 200,
        "body": json.dumps(embed)
    }
