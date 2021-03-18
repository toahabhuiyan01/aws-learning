import json
import boto3
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.client('dynamodb')

def createTable(dynamodb):
    table = dynamodb.create_table(
        TableName = 'users_14',
        KeySchema=[
                {
                    'AttributeName': 'email',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'id',
                    'KeyType': 'RANGE'
                }
            ],
        AttributeDefinitions=[
                {
                    'AttributeName': 'email',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'id',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        

def insertData(datas):
    response = dynamodb.put_item(
            Item = {
                'email': {
                    'S': 'user#' + datas['email']
                },
                'id': {
                    'S': 'user#' + datas['id']
                },
                'name': {
                    'S': 'user#' + datas['name']
                },
                'education': {
                    'S': 'user#' + datas['education']
                },
                'job_status': {
                    'BOOL': datas['job_status']
                }
            },
            TableName= 'users_14'
        )
    return response

    
def getItem(data_for_fetch, table):
    response = table.get_item(
            Key={
                'email': 'user#' + data_for_fetch['email'],
                'id': 'user#' + data_for_fetch['id']
            }
        )
    return response


def queryItem(data, table):
    response = table.query(
            KeyConditionExpression = Key('email').eq('user#' + data)
        )
    return response
    
    
def scanItem(attr, data, table):
    response = table.scan(
            FilterExpression = Attr(attr).eq(data)
        )
    return response


def updateItem(data_for_update, table):
    response = table.update_item(
            Key = {
                'email': 'user#' + data_for_update['email'],
                'id': 'user#' + data_for_update['id']
            },
            UpdateExpression = 'SET job_status = :val1',
            ExpressionAttributeValues = {
                ':val1': True
            }
        )


def lambda_handler(event, context):
    # TODO implement
    dd = boto3.resource('dynamodb')
    table = dd.Table('users_14')
    
    data_for_create = {
        'email': 'tahmid@gmail.com',
        'id': '0006',
        'name': 'md tahmid',
        'education': 'HSC',
        'job_status': False
    }
    
    # response = insertData(data_for_create)
    
    data_for_fetch_update = {
        'email': 'tahmid@gmail.com',
        'id': '0006'
    }
    
    # response = getItem(data_for_fetch_update, table)
    # response = updateItem(data_for_fetch_update, table)
    # response = getItem(data_for_fetch_update, table)
    
    # response = queryItem('tanzel@gmail.com', table)
    # print(response['Items'])
    
    # response = scanItem('job_status', True, table)
    
    
    response = table.query(
            IndexName = 'pk-sk-index',
            KeyConditionExpression = Key('pk').eq('true')
            
        )
    print(len(response['Items']))
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
