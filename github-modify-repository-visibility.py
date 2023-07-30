import re
import argparse
import requests
import concurrent.futures
from github import Github

# Create an argument parser
parser = argparse.ArgumentParser(description='Change the repository visibility of an organization.')
parser.add_argument('--token', help='GitHub Personal Access Token')
parser.add_argument('--organization', help='GitHub Organization Name')
parser.add_argument('--visibility', help='Visibility to set for the repositories')
parser.add_argument('--exclude-patterns', nargs='+', help='Regex patterns for repository exclusion')
args = parser.parse_args()

# Extract the provided arguments
GITHUB_ACCESS_TOKEN = args.token
ORGANIZATION_NAME = args.organization
VISIBILITY = args.visibility
EXCLUDE_PATTERNS = args.exclude_patterns

# Create a GitHub instance using the access token
g = Github(GITHUB_ACCESS_TOKEN)

# Get the organization
org = g.get_organization(ORGANIZATION_NAME)

# Function to process a repository
def process_repository(repo):
    try:
        # Check if the repository name matches any of the exclusion patterns
        if EXCLUDE_PATTERNS and any(re.match(pattern, repo.name) for pattern in EXCLUDE_PATTERNS):
            print(f"Excluded repository: {repo.full_name}")
            return

        # Update the repository visibility using GitHub REST API
        headers = {
            'Authorization': f'Token {GITHUB_ACCESS_TOKEN}',
            'Accept': 'application/vnd.github.nebula-preview+json'  # Enable preview API for visibility parameter
        }
        data = {
            'visibility': VISIBILITY
        }
        url = f'https://api.github.com/repos/{repo.full_name}'
        response = requests.patch(url, headers=headers, json=data)

        if response.status_code == 200:
            print(f"Changed visibility of {repo.full_name} to {VISIBILITY}")
        else:
            print(f"Failed to change visibility of {repo.full_name}: {response.json().get('message')}")

    except Exception as e:
        print(f"Error changing visibility of {repo.full_name}: {str(e)}")

# Iterate over all repositories in the organization
repositories = org.get_repos()

# Process repositories concurrently using multiple threads
with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = [executor.submit(process_repository, repo) for repo in repositories]
    # Wait for all tasks to complete
    concurrent.futures.wait(futures)
