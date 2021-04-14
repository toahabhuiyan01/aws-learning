import json
import boto3

ses = boto3.client('ses')

def create_template_ses():
    response = ses.create_template(
            Template = {
                'TemplateName': 'test_ses_email',
                'SubjectPart': 'Test email',
                'TextPart': 'We have received a request to authorize this email address for use with Amazon SES and Amazon Pinpoint',
                'HtmlPart': '<p>Congratulations</p><p>Now products {{product_name}} has been created seccessfully.</p>'
            }
        )

def lambda_handler(event, context):
    
    response = ses.send_templated_email(
            Source = 'toahabhuiyan@gmail.com',
            Destination={
                'ToAddresses': [
                    'toahabhuiyan@gmail.com'
                ],
                # 'CcAddresses': [
                #     'rezabaiust@gmail.com'    
                # ]
            },
            Template='test_ses_email',
            TemplateData='{"product_name": "chaldal"}'
        )
    
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
