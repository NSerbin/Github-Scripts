import re
from github import Github

# Provide your GitHub personal access token here
GITHUB_ACCESS_TOKEN = 'TOKEN'

# Provide the organization name
ORGANIZATION_NAME = 'ORGANIZATION'

# Provide the team name you want to add as Maintainer
TEAM_NAME = 'TEAM'

# Provide the permission to set 
PERMISSION = 'PERMISSION'

# Provide the regex pattern for repository exclusion
EXCLUDE_PATTERN = r'^(excluded_repo|another_excluded_repo)'

# Create a GitHub instance using the access token
g = Github(GITHUB_ACCESS_TOKEN)

# Get the organization
org = g.get_organization(ORGANIZATION_NAME)

team = next(
    (org_team for org_team in org.get_teams() if org_team.name == TEAM_NAME),
    None,
)
# Check if the team was found
if team is None:
    print(f"Team '{TEAM_NAME}' not found in the organization.")
    exit()

# Iterate over all repositories in the organization
for repo in org.get_repos():
    try:
        # Check if the repository name matches the exclusion pattern
        if re.match(EXCLUDE_PATTERN, repo.name):
            print(f"Excluded repository: '{repo.full_name}'")
            continue

        # Update the team's permission on the repository to "admin"
        team.set_repo_permission(repo, PERMISSION)
        print(f"Added '{TEAM_NAME}' as an admin to '{repo.full_name}'")
    except Exception as e:
        print(f"Error adding '{TEAM_NAME}' as an admin to '{repo.full_name}': {str(e)}")
