import requests
import json
import pandas as pd
import os
from getpass import getpass
from atlassian import Bitbucket

# Enter your Bitbucket credentials
username = 'jairam'
password = 'Crossfit0110!'
base_url = "https://git.cauliflower.com"

# Create a Bitbucket instance
bitbucket = Bitbucket(base_url, username, password)

project_info = bitbucket.project('TES')
print (type(project_info))
print (project_info)

repo_info = bitbucket.get_repo('TES', 'testing_repo')
print (type(repo_info))
print (repo_info)
