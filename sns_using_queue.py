import json
import boto3
import os

sns = boto3.client('sns')
sqs = boto3.client('sqs')



def sent_message():
    queue_url = 'https://sqs.us-east-2.amazonaws.com/534678543881/ToahaTestQueOne'

    response = sqs.send_message(
        QueueUrl=queue_url,
        DelaySeconds=1,
        MessageAttributes={
            'Title': {
                'DataType': 'String',
                'StringValue': 'Lets get started'
            },
            'Author': {
                'DataType': 'String',
                'StringValue': 'Toaha Bhuiyan'
            }
        },
        MessageBody=(
            'Its to inform that please attach your personal information '
            'by this week'
        )
    )


def lambda_handler(event, context):
    sent_message()
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
