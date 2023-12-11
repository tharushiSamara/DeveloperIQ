import os
import requests
from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# GitHub API endpoint
BASE_URL = "https://api.github.com"

# GitHub personal access token
GITHUB_TOKEN = os.environ.get('github_token')

# Data Processing Microservice URL
# DATA_PROCESSING_MICROSERVICE_URL = "http://127.0.0.1:5002/process-and-calculate"

# Repository information
# username = "MohamedSabthar"
# repo = "Smart-VAT"

# Define the headers with the authentication token
headers = {
    "Authorization": f"token {GITHUB_TOKEN}"
}

processor_microservice_url = 'http://10.105.112.250:8081/store-processed-data'

# Function to fetch the list of contributors for a repository from the GitHub API
def fetch_contributors(username, repo):
    print(username)
    print(repo)
    endpoint = f"repos/{username}/{repo}/contributors"
    contributors_data = fetch_github_data(endpoint)
    return contributors_data

# Function to fetch data from GitHub
def fetch_github_data(endpoint):
    url = f"{BASE_URL}/{endpoint}"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data from GitHub: {response.status_code}")
        return None

# Main function to get the list of contributors for a repository
def get_contributor_list(username, repo):
    contributors = fetch_contributors(username, repo)

    if contributors:
        contributor_list = [contributor['login'] for contributor in contributors]
        print("List of Contributors:")
        for contributor in contributor_list:
            print(contributor)
        return contributor_list
    else:
        print("Failed to fetch contributors.")
        return []

# Example usage
# contributor_list = get_contributor_list(username, repo)

# Function to fetch data from the GitHub API
def fetch_github_data2(endpoint, username, repo, params=None):
    url = f"{BASE_URL}/repos/{username}/{repo}/{endpoint}"
    # response = requests.get(url, headers={'Authorization': 'Bearer YOUR_GITHUB_ACCESS_TOKEN'}, params=params)
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data from GitHub: {response.status_code}")
        return None

# Route to collect data for a set of developers
@app.route('/collect-developer-metrics')
def collect_developer_metrics():
    data = request.json
    username = data.get('username')
    repo = data.get('repo')
    developers = get_contributor_list(username,repo)
    print(GITHUB_TOKEN);
    if not username or not repo or not developers:
        return jsonify({"error": "Invalid request. Please provide 'username', 'repo', and 'developers' in the request body."}), 400

    developer_metrics = {}
    for developer in developers:
        # Fetch commit count
        commits_data = fetch_github_data2('commits', username, repo, params={"author": developer})
        commit_count = len(commits_data) if commits_data else 0

        # Fetch issues (including resolved ones)
        issues_data = fetch_github_data2('issues', username, repo, params={"creator": developer, "state": "all"})
        resolved_issues_count = sum(1 for issue in issues_data if issue.get('state') == 'closed')

        # Fetch pull requests
        pull_requests_data = fetch_github_data2('pulls', username, repo, params={"creator": developer, "state": "all"})
        pull_requests_count = len(pull_requests_data) if pull_requests_data else 0

        developer_metrics[developer] = {
            'developer_username' : developer,
            'commit_count': commit_count,
            'resolved_issues_count': resolved_issues_count,
            'pull_requests_count': pull_requests_count
        }

    #processor_response = requests.post(processor_microservice_url, json=developer_metrics)
    #print(processor_response)
    data_json = {"repository": repo, "developer_metrics": developer_metrics}
    print(data_json)
    processor_response = requests.post(processor_microservice_url, json=data_json)
    print(processor_response)
    return jsonify({"repository": repo, "developer_metrics": developer_metrics})

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080)

