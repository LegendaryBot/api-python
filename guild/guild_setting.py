import os

import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table(os.getenv("DYNAMODB_TABLE_DISCORD_GUILD"))

def get_setting(id, key):
    try:
        response_entry = table.get_item(
            Key={
                'id': int(id)
            }
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        if 'Item' in response_entry:
            item = response_entry['Item']
            if 'json' in item and 'settings' in item['json'] and key in item['json'][
                'settings']:
                body = {
                    "guildId": int(id),
                    "key": key,
                    "value": item['json']['settings'][key]
                }

                response = {
                    "statusCode": 200,
                    "body": body
                }
            else:
                body = {
                    "guildId": int(id),
                    "key": key,
                    "error": "Setting not found."
                }
                response = {
                    "statusCode": 404,
                    "body": body
                }

            return response


def set_setting(id, key, value):
    try:
        response_entry = table.get_item(
            Key={
                'id': int(id)
            }
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        if 'Item' in response_entry and 'json' in response_entry['Item']:
            guild_json = response_entry['Item']['json']
            guild_json['settings'][key] = value
            table.put_item(
                Item={
                    'id': int(id),
                    'json': guild_json
                }
            )
        else:
            guild = {
                'settings': {
                    key: value
            }
            }
            table.put_item(
                Item={
                    'id': int(id),
                    'json': guild
                }
            )
    body = {
        "guildId": int(id),
        "key": key,
        "value": value
    }
    response = {
        "statusCode": 200,
        "body": body
    }
    return response


def remove_setting(id, key):
    try:
        response_entry = table.get_item(
            Key={
                'id': int(id)
            }
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        if 'Item' in response_entry and 'json' in response_entry['Item'] and 'settings' in response_entry['Item']['json'] and key in response_entry['Item']['json']['settings']:
            guild_json = response_entry['Item']['json']
            guild_json['settings'].pop(key)
            table.put_item(
                Item={
                    'id': int(id),
                    'json': guild_json
                }
            )
            body = {
                "guildId": int(id),
                "key": key,
            }
            response = {
                "statusCode": 200,
                "body": body
            }
        else:
            body = {
                "guildId": int(id),
                "key": key,
                "error": "Setting not found"
            }
            response = {
                "statusCode": 404,
                "body": body
            }
        return response
