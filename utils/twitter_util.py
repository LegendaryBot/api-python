import json

import twitter
import os

from discord.colour import Colour
from datetime import datetime

from utils.simple_utc import simple_utc


def get_blizzardcs_last_tweet(event, context):
    region = event['pathParameters']['region']
    api = twitter.Api(consumer_key=os.getenv("TWITTER_CONSUMER_KEY"),
                      consumer_secret=os.getenv("TWITTER_CONSUMER_SECRET"), application_only_auth=True)
    status = api.GetUserTimeline(screen_name="blizzardcs" if region.lower() == "us" else "blizzardcseu_en", include_rts=False,
                                 exclude_replies=True)

    date = datetime.strptime(status[0].created_at, "%a %b %d %H:%M:%S +0000 %Y")
    date = date.replace(tzinfo=simple_utc())
    embed = {
        "thumbnail": {
            "url": status[0].user.profile_image_url_https
        },
        "author": {
            "name": status[0].user.screen_name,
            "url": "https://twitter.com/%s" % status[0].user.screen_name
        },
        "description": status[0].text,
        "color": Colour.from_rgb(29,161,242).value,
        "timestamp": date.isoformat()
    }

    if status[0].media:
        embed["image"] = {
            "url": status[0].media[0].media_url_https
        }
    return {
        "statusCode": 200,
        "body": json.dumps(embed)
    }

