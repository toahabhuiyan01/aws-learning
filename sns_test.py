import json
import boto3
import os

sns = boto3.client('sns')
sqs = boto3.client('sqs')

def send_request(body):
    response = sns.publish(
            TopicArn = os.environ['email_topic'],
            Message=body
        )
        
def lambda_handler(event, context):
    for record in event['Records']:
        send_request(record['body'])
    
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
