import argparse
from github import Github

def add_users_to_organization(g, org, usernames):
    successful_invites = []
    failed_invites = []

    for username in usernames:
        try:
            user = g.get_user(username)
            org.invite_user(user.login, role="member")  # Change role if needed (member, admin, etc.)
            successful_invites.append(username)
        except Exception as e:
            failed_invites.append((username, str(e)))
    
    return successful_invites, failed_invites

def main():
    parser = argparse.ArgumentParser(description='Add Users to a GitHub organization.')
    parser.add_argument('--token', help='GitHub Personal Access Token')
    parser.add_argument('--organization', help='GitHub Organization Name')
    parser.add_argument('--users', nargs='+', help='Github Users')
    args = parser.parse_args()

    if not args.token or not args.organization or not args.users:
        print("Please provide GitHub access token, organization name, and user list.")
        return

    github_access_token = args.token
    organization_name = args.organization
    users = args.users

    g = Github(github_access_token)
    org = g.get_organization(organization_name)

    successful_invites, failed_invites = add_users_to_organization(g, org, users)

    for username in successful_invites:
        print(f"Invitation sent to {username} successfully.")
    
    for username, error in failed_invites:
        print(f"Failed to send invitation to {username}. Error: {error}")

if __name__ == "__main__":
    main()
