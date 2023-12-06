
import requests
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

data_microservice_url = 'http://localhost:5003/store-processed-data'

# Function to calculate developer productivity score
def calculate_productivity_score(commit_count, issue_resolved_count, pull_request_count):
    # Your scoring logic here
    # This is a simplified example, adjust weights and scoring criteria as needed
    COMMIT_WEIGHT = 1
    ISSUE_RESOLVED_WEIGHT = 2
    PULL_REQUEST_WEIGHT = 3

    score = (
        commit_count * COMMIT_WEIGHT +
        issue_resolved_count * ISSUE_RESOLVED_WEIGHT +
        pull_request_count * PULL_REQUEST_WEIGHT
    )
    return score

# Route to process and calculate productivity score
@app.route('/process-and-calculate', methods=['POST'])
def process_and_calculate():
    data = request.get_json()
    print(data)
    repo = data.get('repository')
    developer_metrics = data.get('developer_metrics')
    print(repo)

    if not repo or not developer_metrics:
        return jsonify({"error": "Invalid request. Please provide 'repository' and 'developer_metrics' in the request body."}), 400

    processed_data = {}
    for developer, metrics in developer_metrics.items():
        commit_count = metrics.get('commit_count', 0)
        resolved_issues_count = metrics.get('resolved_issues_count', 0)
        pull_requests_count = metrics.get('pull_requests_count', 0)

        # Calculate productivity score
        productivity_score = calculate_productivity_score(commit_count, resolved_issues_count, pull_requests_count)

        processed_data[developer] = {
            'developer_username' : developer,
            'commit_count': commit_count,
            'resolved_issues_count': resolved_issues_count,
            'pull_requests_count': pull_requests_count,
            'productivity_score': productivity_score
        }
    
    data_json = {"repository": repo, "processed_data": processed_data}
    print(data_json)
    processor_response = requests.post(data_microservice_url, json=data_json)
    print(processor_response)

    return jsonify({"repository": repo, "processed_data": processed_data})


if __name__ == '__main__':
    app.run(port=5002)