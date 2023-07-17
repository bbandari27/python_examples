import requests
import json
import pandas as pd
import os
from getpass import getpass
from atlassian import Bitbucket
import csv

# Enter your Bitbucket credentials
username = 'user1'
password = 'Crossfit0110!'
base_url = "https://git.cauliflower.com"

#defining class for branch permissions
class BranchPermissionsAPI:
    def __init__(self, base_url):
        self.base_url = base_url
    def get_project_branch_permissions(self, project_key):
        url = f"{self.base_url}/rest/branch-permissions/latest/projects/{project_key}/restrictions".format(project_key=project_key)
        headers = {
            "Accept": "application/json"
        }
        response = requests.get(url, auth=(username, password), headers=headers)
        if response.status_code == 200:
            return json.loads(response.text)
        else:
            print(f"Error: {response.status_code}")
            return None
    def get_repository_branch_permissions(self, project_key, repository_slug):
        url = f"{self.base_url}/rest/branch-permissions/latest/projects/{project_key}/repos/{repository_slug}/restrictions".format(project_key=project_key, repository_slug=repository_slug)
        headers = {
            "Accept": "application/json"
        }
        response = requests.get(url, auth=(username, password), headers=headers)
        if response.status_code == 200:
            return json.loads(response.text)
        else:
            print(f"Error: {response.status_code}")
            return None
    def set_project_branch_permissions(self, project_key, payload):
        url = f"{self.base_url}/rest/branch-permissions/latest/projects/{project_key}/restrictions".format(project_key=project_key)
        headers = {
          "Accept": "application/json",
          "Content-Type": "application/json"
        }
        response = requests.post(url, auth=(username, password), data=payload, headers=headers)
        if response.status_code == 200:
            return json.loads(response.text)
        else:
            print(f"Error: {response.status_code}")
            print(f"Error: {response.text}") 
            return None
    def set_repo_branch_permissions(self, project_key, repository_slug, payload):
        url = f"{self.base_url}/rest/branch-permissions/latest/projects/{project_key}/repos/{repository_slug}/restrictions".format(project_key=project_key, repository_slug=repository_slug)
        headers = {
          "Accept": "application/json",
          "Content-Type": "application/json"
        }
        response = requests.post(url, auth=(username, password), data=payload, headers=headers)
        if response.status_code == 200:
            return json.loads(response.text)
        else:
            print(f"Error: {response.status_code}")
            return None

# Create a Bitbucket instance
bitbucket = Bitbucket(base_url, username, password)

# Get projects using atlassian module
#projects = bitbucket.project_list()
projects = ["TES"]

# Iterate over projects
for project in projects:
    #project_key = project["key"]
    project_key = project
    #Get project permissions
    branch_permissions_api = BranchPermissionsAPI(base_url)
    project_branch_permissions = branch_permissions_api.get_project_branch_permissions(project_key)
    if project_branch_permissions is not None:
        print(" *************** Project {project_key} permissions *************** ".format(project_key=project_key))
        json_response_str = json.dumps(project_branch_permissions, sort_keys=True, indent=4, separators=(",", ": "))
        # parse and extract the json response string 
        json_response = json.loads(json_response_str)
        values = json_response["values"]
        print (" *************** Project {project_key} scanned *************** ".format(project_key=project_key))

        # Load CSV data
        csv_data = []
        with open('./input.csv', 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            csv_data = list(csv_reader)

        # Remove specified fields from JSON data
        for item in values:
            item.pop('accessKeys', None)
            item.pop('id', None)
            item['matcher'].pop('active', None)
            item.pop('scope', None)
            item['users'] = [user['name'] for user in item['users']]

            # Extract existing groups from JSON
            existing_groups = item['groups']

            # Iterate over CSV rows
            for csv_row in csv_data:
                csv_groups = [group.strip() for group in csv_row[0].split(',')]
                csv_value = csv_row[1].strip()
                for group in csv_groups:
                    if group in existing_groups:
                        item['groups'].append(csv_value)
            
            payload = json.dumps(item)

            set_project_branch_permissions = branch_permissions_api.set_project_branch_permissions(project_key, payload)
            json_res_str = json.dumps(set_project_branch_permissions, sort_keys=True, indent=4, separators=(",", ": "))
    else: 
        print("no branch permisisons for project {project_key}: project_branch_permissions.status_code".format(project_key=project_key))

    # Get repositories in the project
    repositories = bitbucket.repo_list(project_key)
    # Iterate over repositories
    for repository in repositories:
        repository_slug = repository["slug"]
        #filtering the unarchived repositories
        repo_info = bitbucket.get_repo(project_key, repository_slug)
        if not repo_info['archived']:
            # Get branch permissions for the repository
            branch_permissions_api = BranchPermissionsAPI(base_url)
            repository_branch_permissions = branch_permissions_api.get_repository_branch_permissions(project_key, repository_slug)
            if repository_branch_permissions is not None:
                print(" *************** Project {project_key}/{repository_slug} permissions *************** ".format(project_key=project_key, repository_slug=repository_slug))
                json_response_str = json.dumps(repository_branch_permissions, sort_keys=True, indent=4, separators=(",", ": "))
                # parse and extract the json response string 
                json_response = json.loads(json_response_str)
                values = json_response["values"]
                print(" *************** Project {project_key}/{repository_slug} scanned *************** ".format(project_key=project_key, repository_slug=repository_slug))
                # Load CSV data
                csv_data = []
                with open('./input.csv', 'r') as csv_file:
                    csv_reader = csv.reader(csv_file)
                    csv_data = list(csv_reader)

                # Remove specified fields from JSON data
                for item in values:
                    item.pop('accessKeys', None)
                    item.pop('id', None)
                    item['matcher'].pop('active', None)
                    item.pop('scope', None)
                    item['users'] = [user['name'] for user in item['users']]

                    # Extract existing groups from JSON
                    existing_groups = item['groups']

                    # Iterate over CSV rows
                    for csv_row in csv_data:
                        csv_groups = [group.strip() for group in csv_row[0].split(',')]
                        csv_value = csv_row[1].strip()
                        for group in csv_groups:
                            if group in existing_groups:
                                item['groups'].append(csv_value)
                    
                    payload = json.dumps(item)

                    set_repo_branch_permissions = branch_permissions_api.set_repo_branch_permissions(project_key, repository_slug, payload)
                    json_res_str = json.dumps(set_repo_branch_permissions, sort_keys=True, indent=4, separators=(",", ": "))
            else: 
                print("no branch permisisons for Project/Respository {project_key}/{repository_slug}: repository_branch_permissions.status_code".format(project_key=project_key, repository_slug=repository_slug))
        else:
            print("Project/Respository {project_key}/{repository_slug}: is archived".format(project_key=project_key, repository_slug=repository_slug))
