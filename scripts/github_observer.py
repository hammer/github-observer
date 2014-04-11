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
    'CreateEvent': [{'ref_type': ['repository', 'branch', 'tag']}, 'ref', 'description', 'master_branch', 'pusher_type'],
    'IssuesEvent': [{'action': ['opened', 'closed', 'reopened']}, 'issue'],
    'PullRequestEvent': [{'action': ['opened', 'closed', 'reopened', 'synchronize']}, 'number', 'pull_request'],
    'PushEvent': ['head', 'ref', 'size', 'commits'],
    'ReleaseEvent': [{'action': 'published'}, 'release'],
}

github_user = os.environ.get('GITHUB_USER')
github_password = os.environ.get('GITHUB_PASSWORD')
g = Github(github_user, github_password)


def to_dt(s):
    return dt.strptime(s, "%a, %d %b %Y %H:%M:%S %Z")


def get_lab_events():
    df = []
    lab_members = [m for m in g.get_organization(LAB).get_members() if m.login in MEMBERS]
    for member in lab_members:
        member_events = [e for e in member.get_events()
                         if e.type in EVENT_TYPES.keys()]
        for event in member_events:
            df.append({
                "member": member.login,
                "last_modified": to_dt(event.last_modified),
                "repo": event.repo.name,
                "type": event.type[:-5],
                "action": event.payload.get("action")
            })
    return DataFrame(df)


def get_lab_branches():
    df = []
    for repo in g.get_organization(LAB).get_repos():
        for branch in repo.get_branches():
            df.append({
                "repo": repo.name,
                "branch": branch.name,
                "last_modified": to_dt(branch.last_modified),
                "last_commit_author": branch.commit.author.login,
            })
    return DataFrame(df)


def get_lab_commits():
    df = []
    last_week = dt.now() - td(days=7)
    for repo in g.get_organization(LAB).get_repos():
        for commit in repo.get_commits(since=last_week):
            if commit.author.login in MEMBERS:
                df.append({
                    "repo": repo.name,
                    "author": commit.author.login,
                    "message": commit.commit.message,
                    "last_modified": to_dt(commit.last_modified),
                    "size": commit.stats.total,
                })
    return DataFrame(df)



