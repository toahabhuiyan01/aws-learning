import json

def lambda_handler(event, context):
    
    try:
        username = event["body"]["username"]
        password = event["body"]["password"]
        
    except:
        status_code = 400
        success = False
        message = {
                    "error": json.dumps('Request error')
                }
        
    if username == "demo" and password == "demo":
        status_code = 202
        success = True
        message = {
                    "username": username,
                    "password": password
                }
    else:
        status_code = 401
        success = False
        message = {
                    "error": json.dumps('Invalid username or password')
                }
    
    
    return {
        'statusCode': status_code,
        'body':{
            'success': success,
            'message': message
        }
    }
