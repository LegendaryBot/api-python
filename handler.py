import decimal
import json
import os

import boto3
from botocore.exceptions import ClientError


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


def hello(event, context):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table(os.getenv("DYNAMODB_TABLE_DISCORD_GUILD"))
    try:
        responseEntry = table.get_item(
            Key={
                'id': int(event['pathParameters']['guildId'])
            }
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print(responseEntry)
        if 'Item' in responseEntry:
            item = responseEntry['Item']
            if 'json' in item and 'settings' in item['json'] and event['pathParameters']['key'] in item['json']['settings']:
                body = {
                    "guildId": int(event['pathParameters']['guildId']),
                    "key": event['pathParameters']['key'],
                    "value": item['json']['settings'][event['pathParameters']['key']]
                }

                response = {
                    "statusCode": 200,
                    "body": json.dumps(body, cls=DecimalEncoder)
                }
            else:
                body = {
                    "guildId": int(event['pathParameters']['guildId']),
                    "error": "Setting entry not found"
                }
                response = {
                    "statusCode": 404,
                    "body": json.dumps(body, cls=DecimalEncoder)
                }

            return response

    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration
