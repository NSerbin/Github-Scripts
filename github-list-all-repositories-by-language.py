import argparse
from github import Github

def get_repositories_by_language(ORGANIZATION_NAME, language, GITHUB_ACCESS_TOKEN):
    g = Github(GITHUB_ACCESS_TOKEN)
    query = f"org:{ORGANIZATION_NAME} language:{language} fork:false"  # Constructing the search query

    repos = g.search_repositories(query=query)
    return list(repos)

def main():
    parser = argparse.ArgumentParser(description='Get repositories by language from a GitHub organization.')
    parser.add_argument('--token', help='GitHub Personal Access Token', required=True)
    parser.add_argument('--organization', help='GitHub Organization Name', required=True)
    parser.add_argument('--language', help='Desired programming language', required=True)
    args = parser.parse_args()

    GITHUB_ACCESS_TOKEN = args.token
    ORGANIZATION_NAME = args.organization
    DESIRED_LANGUAGE = args.language

    if (repositories := get_repositories_by_language(ORGANIZATION_NAME, DESIRED_LANGUAGE, GITHUB_ACCESS_TOKEN)):
        print(f"Repositories in {ORGANIZATION_NAME} using {DESIRED_LANGUAGE}:")
        for repo in repositories:
            print(repo.full_name)  # Adjust what data to print as per your needs
    else:
        print("No repositories found for the specified language in the organization.")

if __name__ == '__main__':
    main()
