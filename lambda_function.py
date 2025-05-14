import json
import boto3
import datetime
import os

# Initialize S3 client
s3_client = boto3.client('s3')

# Define the target S3 bucket (replace by your bucket name)
BUCKET_NAME = 'your-bucket-name'

# Retrieve VERIFY_TOKEN from environment variables
VERIFY_TOKEN = os.environ.get('VERIFY_TOKEN', 'undefined_token')

def lambda_handler(event, context):
    print("Event received:", json.dumps(event))
    print("Context received:", context)
    print(f"Environment VERIFY_TOKEN: '{VERIFY_TOKEN}'")

    try:
        http_method = event.get('httpMethod', '')
        print(f"HTTP Method: {http_method}")

        # Handle GET request for webhook verification
        if http_method == 'GET':
            params = event.get('queryStringParameters') or {}
            mode = params.get('hub.mode')
            token = params.get('hub.verify_token')
            challenge = params.get('hub.challenge')

            # Verify the token and respond with the challenge
            if mode == 'subscribe' and token == VERIFY_TOKEN:
                print("Token verified successfully")
                return {
                    'statusCode': 200,
                    'body': challenge
                }
            else:
                print("Token verification failed")
                return {
                    'statusCode': 403,
                    'body': json.dumps({'error': 'Invalid verification token'})
                }

        # Handle POST request to receive and store webhook data
        elif http_method == 'POST':
            timestamp = datetime.datetime.utcnow().isoformat()
            body = event.get('body', '{}')
            print(f"Received POST body: {body}")

            object_key = f"{timestamp}.json"

            # Store the payload in S3
            s3_client.put_object(
                Bucket=BUCKET_NAME,
                Key=object_key,
                Body=body,
                ContentType='application/json'
            )

            print("✔ Webhook payload saved to S3")

            return {
                'statusCode': 200,
                'body': json.dumps({'message': 'Webhook received successfully'})
            }

        # Handle unsupported HTTP methods
        else:
            print(f"Unsupported HTTP method: {http_method}")
            return {
                'statusCode': 405,
                'body': json.dumps({'error': f'Method {http_method} not allowed'})
            }

    except Exception as e:
        print(f"✘ Exception occurred: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
