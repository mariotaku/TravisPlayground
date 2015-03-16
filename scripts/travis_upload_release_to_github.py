#!/usr/bin/env python2
# -*- coding: utf-8 -*-

__author__ = 'mariotaku'
git_https_url_prefix = 'https://github.com/'
git_ssh_url_prefix = 'git@github.com:'
git_file_suffix = '.git'
github_header_accept = 'application/vnd.github.v3+json'

import os
import httplib
import urllib
import urlparse
import json
import fnmatch
import re
from os import getenv
from subprocess import check_output
from subprocess import CalledProcessError

DEVNULL = open(os.devnull, 'w')
repo_url = None

try:
    repo_url = check_output(['git', 'config', '--get', 'remote.origin.url']).splitlines()[0]
except CalledProcessError:
    print('No remote url for this project, abort')
    exit(0)

user_repo_name = None
if repo_url.startswith(git_ssh_url_prefix):
    user_repo_name = repo_url[len(git_ssh_url_prefix):]
elif repo_url.startswith(git_https_url_prefix):
    user_repo_name = repo_url[len(git_https_url_prefix):]

if not user_repo_name:
    print('Not a github repo, abort')
    exit(0)

if user_repo_name.endswith(git_file_suffix):
    user_repo_name = user_repo_name[:-len(git_file_suffix)]

print user_repo_name
current_tag = None
try:
    current_tag = check_output(['git', 'describe'], stderr=DEVNULL)
except CalledProcessError:
    print('This commit doesn\'t have tag, abort')
    exit(0)

github_access_token = getenv('GITHUB_ACCESS_TOKEN')

if not github_access_token:
    print('No access token given, abort')
    exit(0)

github_authorization_header = "token %s" % github_access_token

print('Creating release for tag %s', current_tag)

req_headers = {'Accept': github_header_accept}

conn = httplib.HTTPSConnection('api.github.com')
conn.request('POST', '/repos/%s/releases' % user_repo_name,
             body=json.dumps({
                 'tag_name': current_tag,
                 'name': "Version %s" % current_tag,
                 'body': 'Build and uploaded by Travis'
             }),
             headers={
                 'Accept': github_header_accept,
                 'Authorization': github_authorization_header,
                 'Content-Type': 'application/json'
             })
response = conn.getresponse()
response_values = json.loads(response.read())

upload_url = urlparse.urlparse(re.sub('\{\?([\w\d_\-]+)\}', '', response_values['upload_url']))
conn = httplib.HTTPSConnection(upload_url.hostname)
for root, dirnames, filenames in os.walk(os.getcwd()):
    for filename in fnmatch.filter(filenames, '*-release.apk'):
        conn.request('POST', "%s?%s" % (upload_url.path, urllib.urlencode({'name': filename})),
                     body=os.path.join(root, filename),
                     headers={
                         'Accept': github_header_accept,
                         'Authorization': github_authorization_header,
                         'Content-Type': 'application/json'
                     })