import boto3
import os
from urllib.parse import unquote_plus
import json

s3 = boto3.client('s3')
translate = boto3.client('translate')
comprehend = boto3.client('comprehend')
dynamodb = boto3.resource('dynamodb')
sns = boto3.client('sns')

# Environment variables in Lambda
TABLE_NAME = os.environ['TABLE_NAME']
SNS_TOPIC_ARN = os.environ['SNS_TOPIC_ARN']

def lambda_handler(event, context):
    print("Event:", json.dumps(event))
    table = dynamodb.Table(TABLE_NAME)

    # Get bucket and file key from event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = unquote_plus(event['Records'][0]['s3']['object']['key'])

    # Read file content
    obj = s3.get_object(Bucket=bucket, Key=key)
    content = obj['Body'].read().decode('utf-8')

    # Translate to English
    translated = translate.translate_text(
        Text=content,
        SourceLanguageCode='auto',
        TargetLanguageCode='en'
    )['TranslatedText']

    # Detect sentiment
    sentiment = comprehend.detect_sentiment(
        Text=translated, LanguageCode='en'
    )['Sentiment']

    # Save to DynamoDB
    table.put_item(Item={
        'filename': key,
        'original_text': content,
        'translated_text': translated,
        'sentiment': sentiment
    })

    # If negative sentiment, send SNS alert
    if sentiment.lower() == 'negative':
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject="Negative Sentiment Alert",
            Message=f"File {key} had negative sentiment."
        )

    return {
        'statusCode': 200,
        'body': json.dumps({'filename': key, 'sentiment': sentiment})
    }
