import json
import boto3
import csv
import uuid

dynamodb = boto3.client('dynamodb')

def insertData(data):
    item = {}
    for key in data:
        item[key] = {
                    'S': data[key]
                }
                
    response = dynamodb.put_item(
            Item = item,
            TableName= 'toaha_s3_assignment'
        )
    return response 

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    
    region = "us-east-2"
    record_list = []
    
    try:
        origin = event["headers"]["origin"]
        keys = [key['Key'] for key in s3.list_objects(Bucket='practices3-18')['Contents']]

        if origin:
            return {
                'statusCode': 200,
                'body': json.dumps(keys)
            }
            
    except Exception as e:
        pass

    try:
        list_obj = []
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']

        csv_file = s3.get_object(Bucket = bucket, Key = key)
        record_list = csv_file['Body'].read().decode('utf-8').split('\n')
        csv_reader = csv.reader(record_list, delimiter=',')
        line_c = 0
        headers = []
        for row in csv_reader:
            if line_c == 0:
                line_c = line_c + 1
                headers = [header for header in row]
                continue
            
            items = {'pk': str(uuid.uuid4().hex)}
            for i, value in enumerate(row):
                items[headers[i]] = value
            insertData(items)
            
    except Exception as e:
        print(str(e))

    return {
        'statusCode': 200,
        'body': json.dumps("All is well")
    }
