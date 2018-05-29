import json

from requests_html import HTMLSession

tier_data_img_src = {
    "rank-1.png": "Bronze",
    "rank-2.png": "Silver",
    "rank-3.png": "Gold",
    "rank-4.png": "Platinum",
    "rank-5.png": "Diamond",
    "rank-6.png": "Master",
    "rank-7.png": "Grandmaster"
}


def get_overwatch_stats(event, context):
    battletag = event['pathParameters']['battletag']
    session = HTMLSession()
    r = session.get("https://playoverwatch.com/en-us/career/pc/%s" % battletag)
    if r.html.find(".competitive-rank", first=True):
        rank = tier_data_img_src[r.html.find(".competitive-rank", first=True).find('img', first=True).attrs['src'].split("/")[-1]]
        avatar = r.html.find(".player-portrait", first=True).attrs['src']
        rank_int = r.html.find(".competitive-rank", first=True).find('div .u-align-center', first=True).text
        competitive = r.html.find("#competitive", first=True)
        stats_table = competitive.find('.data-table')[5]
        values = {}
        for tr in stats_table.find('tbody', first=True).find('tr'):
            values[tr.find('td', first=True).text] = tr.find('td')[1].text
        games_won = int(values['Games Won'])
        games_played = int(values['Games Played'])
        win_rate = games_won / games_played * 100
        embed = {
            "title": "Player %s Overwatch Stats" % battletag,
            "fields": [
                {
                    "name": "Rank",
                    "value": "%s (%s)" % (rank, rank_int),
                    "inline": True
                },
                {
                    "name": "Wins",
                    "value": values['Games Won'],
                    "inline": True
                },
                {
                    "name": "Losses",
                    "value": values['Games Lost'],
                    "inline": True
                },
                {
                    "name": "Ties",
                    "value": values['Games Tied'],
                    "inline": True
                },
                {
                    "name": "Win Rate",
                    "value": "%s%%" % int(win_rate),
                    "inline": True
                }
            ],
            "thumbnail": {
                "url": avatar
            }
        }
        return {
            "statusCode": 200,
            "body": json.dumps(embed)
        }
    return {
        "statusCode": 404
    }


