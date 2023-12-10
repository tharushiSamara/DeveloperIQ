
import os
import json
import boto3

from datetime import datetime

from flask import Flask, request, jsonify

app = Flask(__name__)

# AWS DynamoDB configuration
DYNAMODB_REGION = 'ap-south-1'
DYNAMODB_TABLE_NAME = 'Developer-Tracking-Data'
AWS_ACCESS_KEY_ID = os.environ.get('aws_access_key_id')
AWS_SECRET_ACCESS_KEY = os.environ.get('aws_secret_access_key')

# Route to store the processed GitHub data in DynamoDB
@app.route('/store-developer_metrics', methods=['POST'])
def store_developer_metrics():
    data = request.json
    repo = data.get('repository')
    developer_metrics = data.get('developer_metrics')

    if not repo or not developer_metrics:
        return jsonify({"error": "Invalid request. Please provide 'repository' and 'developer_metrics' in the request body."}), 400

    # Store processed data in DynamoDB
    store_data_in_dynamodb(repo, developer_metrics)

    return jsonify({"message": "Processed data stored successfully in DynamoDB."})

# Function to securely store processed data in DynamoDB
def store_data_in_dynamodb(repo, developer_metrics):
    try:
        # Initialize DynamoDB client using IAM role credentials
        session = boto3.Session()
        dynamodb = session.resource('dynamodb', region_name=DYNAMODB_REGION, aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
        table = dynamodb.Table(DYNAMODB_TABLE_NAME)
        
        print(repo)
        print(developer_metrics)
        current_date = datetime.now()
        # Example: Store data with a unique identifier as the partition key
        unique_id = f'{repo}-developer_metrics_{current_date}'
        
        It = {'developer_username':unique_id, 'varibles':developer_metrics}
        table.put_item(Item=It)

        print("Data stored in DynamoDB successfully.")
    except Exception as e:
        print(f"Error storing data in DynamoDB: {str(e)}")

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8081)
