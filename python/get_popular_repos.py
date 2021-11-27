import requests
import json
import time


def get_popular_repos(token, min_stars=50, min_forks=5):
    """
        Get python repositories with min_stars and min_forks requirements.
    """
    page_count = 1
    repos = []
    while True:
        response = requests.get(f"https://api.github.com/search/repositories?q=language:python&q=stars:>={min_stars}&q=forks>={min_forks}&sort=stars&order=desc&per_page=100&page={page_count}", headers={"Authorization": "token %s" % token})
        time.sleep(1)
        data = json.loads(response.text)
        if len(data["items"]) == 0:
            break
    
        for f in data["items"]:
            repos += [f["full_name"]]
        page_count += 1
        print("Size of repository list: %d/%d" % (len(repos), data["total_count"]))
    return repos


if __name__ == "__main__":
    token = "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"
    repos = get_popular_repos(token)

    with open("python_repos.txt", 'w') as f:
        for repo in repos:
            f.write(repo + "\n")
