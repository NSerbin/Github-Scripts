import re
import argparse
import concurrent.futures
from github import Github

# Create an argument parser
parser = argparse.ArgumentParser(description='Remove a team from repositories in a GitHub organization.')
parser.add_argument('--token', help='GitHub Personal Access Token')
parser.add_argument('--organization', help='GitHub Organization Name')
parser.add_argument('--team', help='Team Name to remove from the repositories')
parser.add_argument('--exclude-patterns', nargs='+', help='Regex patterns for repository exclusion')
args = parser.parse_args()

# Extract the provided arguments
GITHUB_ACCESS_TOKEN = args.token
ORGANIZATION_NAME = args.organization
TEAM_NAME = args.team
EXCLUDE_PATTERNS = args.exclude_patterns

# Create a GitHub instance using the access token
g = Github(GITHUB_ACCESS_TOKEN)

# Get the organization
org = g.get_organization(ORGANIZATION_NAME)

# Get the team
team = next((org_team for org_team in org.get_teams() if org_team.name == TEAM_NAME), None)

# Check if the team was found
if team is None:
    print(f"Team {TEAM_NAME} not found in the organization.")
    exit()

# Function to process a repository
def process_repository(repo):
    try:
        # Check if the repository name matches any of the exclusion patterns
        if EXCLUDE_PATTERNS and any(re.match(pattern, repo.name) for pattern in EXCLUDE_PATTERNS):
            print(f"Excluded repository: {repo.full_name}")
            return

        # Remove the team from the repository
        team.remove_from_repos(repo)
        print(f"Removed {TEAM_NAME} from {repo.full_name}")
    except Exception as e:
        print(f"Error removing {TEAM_NAME} from {repo.full_name}: {str(e)}")

# Iterate over all repositories in the organization
repositories = org.get_repos()

# Process repositories concurrently using multiple threads
with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = [executor.submit(process_repository, repo) for repo in repositories]
    # Wait for all tasks to complete
    concurrent.futures.wait(futures)
