import re
import requests
from bs4 import BeautifulSoup
import csv

import argparse


parser = argparse.ArgumentParser(
    description="Download a dependency graph based on github"
)
parser.add_argument("repo", metavar="N", type=str, help="Repo to download")
args = parser.parse_args()
repo = args.repo

resp_main = requests.get(f"https://github.com/{repo}")
used_by = BeautifulSoup(resp_main.text, parser="html.parser").find(
    text=re.compile("Used by")
)
if used_by is None:
    raise ValueError(
        "Cannot find used by in page. Maybe the repo doesnt have a used by link or is not a valid repo"
    )
used_by_link = used_by.find_parent()["href"]
link = f"https://github.com{used_by_link}"
resps = []

while True:
    dependency_page = requests.get(link)
    soup = BeautifulSoup(dependency_page.text, parser="html.parser")
    dependents = soup.findAll(attrs={"data-test-id": "dg-repo-pkg-dependent"})

    def get_info(dependent):
        repo_name = dependent.find(attrs={"data-hovercard-type": "repository"})["href"]
        repo_name = repo_name[1:]  # Remove leading /
        stars = dependent.find(class_="octicon octicon-star").find_parent().text.strip()
        forks = (
            dependent.find(class_="octicon octicon-repo-forked")
            .find_parent()
            .text.strip()
        )
        return {
            "repo_name": repo_name,
            "stars": int(stars.replace(",", "")),  # convert 1,000 to 1000
            "forks": int(forks.replace(",", "")),  # convert 1,000 to 1000
        }

    data = [get_info(d) for d in dependents]
    resps += data

    next_text = soup.find(text="Next")
    next_button = next_text.find_parent()
    if next_button and "href" in next_button.attrs:
        link = next_button["href"]
    else:
        break

with open("repo_dependency.csv", "w") as f:
    writer = csv.DictWriter(f, ["repo_name", "stars", "forks"])
    writer.writeheader()
    for dict in resps:
        writer.writerow(dict)
