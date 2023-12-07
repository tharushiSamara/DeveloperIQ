
import os
import json
import boto3

from datetime import datetime

from flask import Flask, request, jsonify

app = Flask(__name__)

# AWS DynamoDB configuration
DYNAMODB_REGION = 'ap-south-1'
DYNAMODB_TABLE_NAME = 'Developer-Tracking-Data'
AWS_ACCESS_KEY_ID = os.environ["aws_access_key_id"]
AWS_SECRET_ACCESS_KEY = os.environ["aws_secret_access_key"]

# Route to store the processed GitHub data in DynamoDB
@app.route('/store-processed-data', methods=['POST'])
def store_processed_data():
    data = request.json
    repo = data.get('repository')
    processed_data = data.get('processed_data')

    if not repo or not processed_data:
        return jsonify({"error": "Invalid request. Please provide 'repository' and 'processed_data' in the request body."}), 400

    # Store processed data in DynamoDB
    store_data_in_dynamodb(repo, processed_data)

    return jsonify({"message": "Processed data stored successfully in DynamoDB."})

# Function to securely store processed data in DynamoDB
def store_data_in_dynamodb(repo, processed_data):
    try:
        # Initialize DynamoDB client using IAM role credentials
        session = boto3.Session()
        dynamodb = session.resource('dynamodb', region_name=DYNAMODB_REGION, aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
        table = dynamodb.Table(DYNAMODB_TABLE_NAME)
        
        print(repo)
        print(processed_data)
        current_date = datetime.now()
        # Example: Store data with a unique identifier as the partition key
        unique_id = f'{repo}-processed-data_{current_date}'
        
        It = {'developer_username':unique_id, 'varibles':processed_data}
        table.put_item(Item=It)

        print("Data stored in DynamoDB successfully.")
    except Exception as e:
        print(f"Error storing data in DynamoDB: {str(e)}")

if __name__ == '__main__':
    app.run(port=5003)