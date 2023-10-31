import argparse
from github import Github

# Create an argument parser
parser = argparse.ArgumentParser(description='List all the branches of an organization.')
parser.add_argument('--token', help='GitHub Personal Access Token')
parser.add_argument('--organization', help='GitHub Organization Name')
args = parser.parse_args()
# Provide your GitHub personal access token here
GITHUB_ACCESS_TOKEN = args.token

# Replace 'organization_name' with your organization's name
ORGANIZATION_NAME = args.organization

def get_branch_protection_status(repo, branch_name):
    try:
        branch = repo.get_branch(branch_name)
        protection = branch.get_protection()
        return protection.enabled
    except Exception as e:
        return f"Error: {e}"

def main():
    # Authenticate using your access token
    g = Github(GITHUB_ACCESS_TOKEN)

    org = g.get_organization(ORGANIZATION_NAME)

    for repo in org.get_repos():
        print(f"Repository: {repo.full_name}")
        branches = repo.get_branches()
        for branch in branches:
            print(f"  Branch: {branch.name}")
            protection_status = get_branch_protection_status(repo, branch.name)
            print(f"    Protection enabled: {protection_status}")
        print()

if __name__ == "__main__":
    main()
