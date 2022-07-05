import re
import requests
from requests.adapters import HTTPAdapter, Retry
from bs4 import BeautifulSoup
import csv
from time import sleep

import argparse


parser = argparse.ArgumentParser(
    description="Download a dependency graph based on github"
)
parser.add_argument("repo", metavar="REPO", type=str, help="Repo to download")
parser.add_argument(
    "--csv",
    metavar="CSV",
    type=str,
    help="CSV target file. Default is repo_dependency.csv",
    default="repo_dependency.csv",
)
args = parser.parse_args()
repo = args.repo
csv_file = args.csv

resp_main = requests.get(f"https://github.com/{repo}")
used_by = BeautifulSoup(resp_main.text, parser="html.parser", features="lxml").find(
    text=re.compile("Used by")
)
if used_by is None:
    raise ValueError(
        "Cannot find used by in page. Maybe the repo doesnt have a used by link or is not a valid repo"
    )
used_by_link = used_by.find_parent()["href"]
link = f"https://github.com{used_by_link}"
session = requests.Session()
retries = Retry(total=5, backoff_factor=1, status_forcelist=[429, 504, 502])
session.mount("https://", HTTPAdapter(max_retries=retries))
f = open(csv_file, "w")
writer = csv.DictWriter(f, ["repo_name", "stars", "forks"])
writer.writeheader()
while True:
    dependency_page = session.get(link)
    sleep(0.5)
    soup = BeautifulSoup(dependency_page.text, parser="html.parser", features="lxml")
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

    for d in dependents:
        writer.writerow(get_info(d))
    next_text = soup.find(text="Next")
    if next_text is None:
        break
    next_button = next_text.find_parent()
    if next_button and "href" in next_button.attrs:
        link = next_button["href"]
    else:
        break
f.close()
