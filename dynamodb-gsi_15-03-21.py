import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
import uuid


"""
https://docs.google.com/document/d/12GLhvGRVdVLtAKbm9rI-x8AEWyJ_O9vEEbe-vgKmetI/edit        //AC

#######           SKETCH          #################
    functions:
    
        insertEmployeeData
        
        insertDeptData
        
        insertOrgData
        
        getAllDept
        
        isHead
        
        headsNonHeadsInParticularDept
        
        searchEmployeeByDept
        
        empToHead  //promote to head

        deleteInstanceFromEmp
        
        deleteInstanceFromDept
        
        updateInstanceFromEmp
        
        updateInstanceFromDept
        
"""

client = boto3.client('dynamodb')


def insertEmployeeData(data):
    response = client.put_item(
            Item = {
                'pk': {
                    'S': 'dept#' + data['dept_id']
                },
                'sk': {
                    'S': 'emp#' + data['emp_id']
                },
                'name': {
                    'S': 'emp#' + data['name']
                },
                'address': {
                    'S': 'emp#' + data['address']
                },
                'gsipk': {
                    'S': 'emp#' + data['is_head']
                },
                'gsisk': {
                    'S': 'dept#' + data['dept_id']+'emp#'+ data['emp_id']
                }
            },
            TableName= 'dept_emp_15'
        )
    return response
    
def insertDeptData(data):
    response = client.put_item(
            Item = {
                'pk': {
                    'S': 'org#' + data['org_id']
                },
                'sk': {
                    'S': 'dept#' + data['dept_id']
                },
                'name': {
                    'S': 'dept#' + data['name']
                },
                'address': {
                    'S': 'dept#' + data['address']
                }
            },
            TableName= 'dept_emp_15'
        )
    return response
    
    
def insertOrgData(data):
    response = client.put_item(
            Item = {
                'pk': {
                    'S': 'org#' + data['org_id']
                },
                'sk': {
                    'S': 'org#shadhin'
                }
            },
            TableName= 'dept_emp_15'
        )
    return response
    
def getAllDept(data, table):
    response = table.query(
            KeyConditionExpression = Key('pk').eq('org#' + data['org_id'])
        )
    return response['Items']
    

def isHead(data, table): # if a employee is dept head then ha can crud the data here we check is he dept head or not
    response = table.query(
            IndexName = 'gsipk-gsisk-index',
            KeyConditionExpression = Key('gsipk').eq('emp#' + data['is']) & Key('gsisk').eq('dept#' + data['dept_id'] + 'emp#' + data['emp_id'])
        )
    return bool(len(response['Items'])) 
    

def headsNonHeadsInParticularDept(data, table):
    response = table.query(
            IndexName = 'gsipk-gsisk-index',
            KeyConditionExpression = Key('gsipk').eq('emp#' + data['is']) & Key('gsisk').begins_with('dept#' + data['dept_id'])
        )
    return response['Items'] 
    
    
def searchEmployeeByDept(data, table):
    response = table.query(
            KeyConditionExpression = Key('pk').eq('dept#' + data['dept_id'])
        )
    return response['Items']
    
    
def empToHead(data_for_update, table):
    response = table.update_item(
            Key = {
                'pk': 'dept#' + data_for_update['dept_id'],
                'sk': 'emp#' + data_for_update['emp_id']
            },
            UpdateExpression = 'SET gsipk = :val1',
            ExpressionAttributeValues = {
                ':val1': 'emp#true'
            }
        )

def deleteInstanceFromEmp(data, table):
    table.delete_item(
        Key={
            'pk': 'dept#' + data['dept_id'],
            'sk': 'emp#' + data['emp_id']
        }
    )

def deleteInstanceFromDept(data, table):
    table.delete_item(
        Key={
            'pk': 'org#' + data['org_id'],
            'sk': 'dept#' + data['dept_id']
        }
    )
    
def updateInstanceFromEmp(datas, table):
    for data in datas['attrs']:
        table.update_item(
            Key={
                'pk': 'dept#' + datas['dept_id'],
                'sk': 'emp#' + datas['emp_id']
            },
            UpdateExpression='SET ' + data['attr'] + ' = :val1',
            ExpressionAttributeValues={
                ':val1': 'emp#' + data['value']
            }
        )
    
def updateInstanceFromDept(datas, table):
    for data in datas['attrs']:
        table.update_item(
            Key={
                'pk': 'org#' + data['org_id'],
                'sk': 'dept#' + data['dept_id']
            },
            UpdateExpression='SET ' + data['attr'] + ' = :val1',
            ExpressionAttributeValues={
                ':val1': 'emp#' + data['value']
            }
        )
    

    
def lambda_handler(event, context):
    # TODO implement
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('dept_emp_15')
        
    org_data = {
        'org_id': uuid.uuid4().hex,
    }
    # insertOrgData(org_data)
    
    dept_data = {
        'org_id': '61aaaf2d9c314a5e847734a29d3594fa',
        'dept_id': uuid.uuid4().hex,
        'name': 'it',
        'address': 'uttara, dhaka'
    }
    # insertDeptData(dept_data)
    
    emp_data = {
        'emp_id': uuid.uuid4().hex,
        'dept_id': 'eff9c79b15bf458c87f7540508609220',
        'name': 'haque',
        'address': 'comilla',
        'is_head': 'false',
    }
    # insertEmployeeData(emp_data)
    
    search_head_indevidual = {
        'is': 'true',
        'dept_id': 'eff9c79b15bf458c87f7540508609220',
        'emp_id': '720994c59b2f42cdb45b3dad172d096f' #085936a4eb9d4bacb035065a1d115800
    }
    # ishead = isHead(search_head_indevidual, table)
    # print(ishead)
    
    search_for_head = {
        'is': 'true',
        'dept_id': 'eff9c79b15bf458c87f7540508609220'
    }
    heads = headsNonHeadsInParticularDept(search_for_head, table)
    print(len(heads), heads)
    
    # emp_dept = searchEmployeeByDept(search_for_head, table)
    # print(len(emp_dept), emp_dept)
    
    emp_to_head = {
        'dept_id': 'eff9c79b15bf458c87f7540508609220',
        'emp_id': '11ecd22a880f47d2b65d6e8c050f143d'
    }
    
    # empToHead(emp_to_head, table)
    
    update_data = {
        'dept_id': 'eff9c79b15bf458c87f7540508609220',
        'emp_id': '11ecd22a880f47d2b65d6e8c050f143d',
        'attrs': [
                    {
                        'attr': 'address',
                        'value': 'dhaka gulsan'
                    }
                ]
    }
    # updateInstanceFromEmp(update_data, table)
    
    delete_emp = {
        'dept_id': 'eff9c79b15bf458c87f7540508609220',
        'emp_id': 'a1fb22873fa34f85a98f673fc0d2cf0b'
    }
    # deleteInstanceFromEmp(delete_emp, table)
    
    
    # print(response['Items']) 
    return {
        'statusCode': 200,
        'body': json.dumps('All is Well, from Lambda!')
    }
