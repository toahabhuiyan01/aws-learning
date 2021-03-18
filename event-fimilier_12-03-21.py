import json

first_name = None
last_name = None

def lambda_handler(event, context):
   
    print(event)
    
    first_name  = event['body']["first_name"]
    last_name = event['body']["last_name"]
    
    http_method = ""
    if http_method == "GET":
        pass
    elif http_method == "POST":
        pass
    
    return {
        'statusCode': 200,
        'body': {
            'success': True,
            "message": {
                "username": first_name + last_name,
                "password": "ad" + first_name + "da" + last_name
            }
        }
    }
