import guild.guild_setting as gs
import json

from aws import DecimalEncoder


def get_setting(event, context):
    result = gs.get_setting(event['pathParameters']['guildId'], event['pathParameters']['key'])
    result['body'] = json.dumps(result['body'], cls=DecimalEncoder.DecimalEncoder)
    return result


def set_setting(event, context):
    result = gs.set_setting(event['pathParameters']['guildId'], event['pathParameters']['key'], event['body'])
    result['body'] = json.dumps(result['body'], cls=DecimalEncoder.DecimalEncoder)
    return result


def remove_setting(event, context):
    result = gs.remove_setting(event['pathParameters']['guildId'], event['pathParameters']['key'])
    result['body'] = json.dumps(result['body'], cls=DecimalEncoder.DecimalEncoder)
    return result
