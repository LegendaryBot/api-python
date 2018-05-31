import json
import os
import boto3

client = boto3.client('cloudwatch')


def add_point(event, context):
    body = json.loads(event['body'])
    for point in body:
        metric_data = {
            'MetricName': point['name'],
            'Dimensions': [
                {
                    'Name': 'Environment',
                    'Value': os.getenv("STATS_DIMENSION")
                }
            ],
            'Value': point['value'],
            'Unit': 'Count'

        }
        client.put_metric_data(Namespace='LegendaryBot', MetricData=metric_data)
