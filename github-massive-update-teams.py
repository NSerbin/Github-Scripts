import re
import concurrent.futures
from github import Github

# Provide your GitHub personal access token here
GITHUB_ACCESS_TOKEN = 'CHANGE-ME'

# Provide the organization name
ORGANIZATION_NAME = 'CHANGE-ME'

# Provide the team name you want to add as Maintainer
TEAM_NAME = 'CHANGE-ME'

# Provide the permission to set
PERMISSION = 'maintain'

# Provide the regex pattern for repository exclusion
EXCLUDE_PATTERN = r'^(excluded_repo|another_excluded_repo)'

# Create a GitHub instance using the access token
g = Github(GITHUB_ACCESS_TOKEN)

# Get the organization
org = g.get_organization(ORGANIZATION_NAME)

# Get the team
team = next((org_team for org_team in org.get_teams() if org_team.name == TEAM_NAME), None)

# Check if the team was found
if team is None:
    print(f"Team '{TEAM_NAME}' not found in the organization.")
    exit()

# Function to process a repository
def process_repository(repo):
    try:
        # Check if the repository name matches the exclusion pattern
        if re.match(EXCLUDE_PATTERN, repo.name):
            print(f"Excluded repository: '{repo.full_name}'")
            return

        # Update the team's permission on the repository
        team.set_repo_permission(repo, PERMISSION)
        print(f"Added '{TEAM_NAME}' as an '{PERMISSION}' to '{repo.full_name}'")
    except Exception as e:
        print(f"Error adding '{TEAM_NAME}' as an '{PERMISSION}' to '{repo.full_name}': {str(e)}")

# Iterate over all repositories in the organization
repositories = org.get_repos()

# Process repositories concurrently using multiple threads
with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = [executor.submit(process_repository, repo) for repo in repositories]
    # Wait for all tasks to complete
    concurrent.futures.wait(futures)