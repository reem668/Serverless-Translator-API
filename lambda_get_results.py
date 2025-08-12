import boto3
import os
import json

dynamodb = boto3.resource('dynamodb')
TABLE_NAME = os.environ['TABLE_NAME']

def lambda_handler(event, context):
    table = dynamodb.Table(TABLE_NAME)

    # Get filename from query string
    params = event.get('queryStringParameters', {})
    if not params or 'filename' not in params:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'filename parameter is required'})
        }

    filename = params['filename']
    response = table.get_item(Key={'filename': filename})

    if 'Item' not in response:
        return {
            'statusCode': 404,
            'body': json.dumps({'error': 'File not found'})
        }

    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps(response['Item'])
    }
