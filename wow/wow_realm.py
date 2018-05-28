import json

import battlenet.battlenet as bnet


def get_realm_status(event, context):
    realm = event['pathParameters']['realm']
    region = event['pathParameters']['region']
    embed = bnet.get_server_status_embed(region, realm)
    print(embed)
    if embed:
        response = {
            "statusCode": 200,
            "body": json.dumps(embed)
        }
        return response
    else:
        body = {
            "realm": realm,
            "region": region,
            "error": "Realm not found"
        }
        response = {
            "statusCode": 200,
            "body": json.dumps(body)
        }
        return response
