#! /usr/bin/env python3
import os
from github import Github

LAB = 'hammerlab'
LOGINS = [
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

for member in g.get_organization(LAB).get_members():
    if member.login in LOGINS:
        evented_repos = set()
        evented_repos.update([event.repo.name
                              for event in member.get_events()
                              if not event.repo.name.startswith(member.login + '/')
                              and event.type in EVENT_TYPES.keys()])
        print(member.login, member.name, evented_repos)

