#! /usr/bin/env python3
from datetime import datetime as dt, timedelta as td
import os

from github import Github
from pandas import DataFrame

LAB = 'hammerlab'
MEMBERS = [
    'arahuja',
    'hammer',
    'iskandr',
    'nealsid',
    'timodonnell',
    'smondet',
]
EVENT_TYPES = {
    'CreateEvent': ['ref_type', 'ref', 'description', 'master_branch', 'pusher_type'],
    'IssuesEvent': None,
    'PullRequestEvent': None,
    'PushEvent': None,
    'ReleaseEvent': None,
}

github_user = os.environ.get('GITHUB_USER')
github_password = os.environ.get('GITHUB_PASSWORD')
g = Github(github_user, github_password)

def get_member_events():
    df = []
    for member in g.get_organization(LAB).get_members():
        if member.login in MEMBERS:
            evented_repos = set()
            evented_repos.update([event.repo.name
                                  for event in member.get_events()
                                  if not event.repo.name.startswith(member.login + '/')
                                  and event.type in EVENT_TYPES.keys()])
            for repo in evented_repos:
                df.append({
                    "member_login": member.login,
                    "member_name": member.name,
                    "evented_repo": repo,
                })
    return DataFrame(df)


def get_lab_branches():
    df = []
    for repo in g.get_organization(LAB).get_repos():
        for branch in repo.get_branches():
            last_modified = dt.strptime(branch.last_modified, "%a, %d %b %Y %H:%M:%S %Z")
            df.append({
                "repo": repo.name,
                "branch": branch.name,
                "last_modified": last_modified,
                "last_commit_author": branch.commit.author.login,
            })
    return DataFrame(df)


if __name__ == "__main__":
    print(get_member_events())
    print(get_lab_branches())


