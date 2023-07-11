import requests
import json
import pandas as pd
import os
from getpass import getpass
from atlassian import Bitbucket

# Enter your Bitbucket credentials
username = input('Enter your bitbucket username: ')
password = getpass('Enter your Bitbucket password: ')
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

# Create a Bitbucket instance
bitbucket = Bitbucket(base_url, username, password)

# Get projects using atlassian module
projects = bitbucket.project_list()

# Iterate over projects
for project in projects:
    project_key = project["key"]
    #create directory to store the csv files
    os.makedirs('/Users/' + username + '/Desktop/Bitbucket_Permissions/' + project_key)
    #Get project permissions
    branch_permissions_api = BranchPermissionsAPI(base_url)
    project_branch_permissions = branch_permissions_api.get_project_branch_permissions(project_key)
    if project_branch_permissions is not None:
        print("{project_key}.csv is saving to the desired directory".format(project_key=project_key))
        json_response_str = json.dumps(project_branch_permissions, sort_keys=True, indent=4, separators=(",", ": "))
        # parse and extract the json response string 
        json_response = json.loads(json_response_str)
        values = json_response["values"]
        # Create an empty DataFrame
        project_permissions=[]
        # Iterate over the values and populate the DataFrame
        for item in values:
            project_permission = {
                "Project": project_key,
                "Permission Type": item["type"],
                "Branch": item["matcher"]["displayId"],
                "Permission Groups": item["groups"],
                "Permission Users": [user["displayName"] for user in item["users"]]
            }
            project_permissions.append(project_permission)
        # Display the DataFrame
        project_permission_df = pd.DataFrame(project_permissions)
        filepath = '/Users/' + username + '/Desktop/Bitbucket_Permissions/' + project_key + '/' + project_key + '.csv'
        project_permission_df.to_csv(filepath, index=False)
    else: 
        print("no branch permisisons for project {project_key}: project_branch_permissions.status_code".format(project_key=project_key, repository_slug=repository_slug))

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
                print("{project_key}/{repository_slug}.csv is saving to the desired directory".format(project_key=project_key, repository_slug=repository_slug))
                json_response_str = json.dumps(repository_branch_permissions, sort_keys=True, indent=4, separators=(",", ": "))
                # parse and extract the json response string 
                json_response = json.loads(json_response_str)
                values = json_response["values"]
                # Create an empty DataFrame
                repo_permissions=[]
                # Iterate over the values and populate the DataFrame
                for item in values:
                    repo_permission = {
                        "Project": project_key,
                        "Repository": repository_slug,
                        "Permission Type": item["type"],
                        "Branch": item["matcher"]["displayId"],
                        "Permission Groups": item["groups"],
                        "Permission Users": [user["displayName"] for user in item["users"]]
                    }
                    repo_permissions.append(repo_permission)
                # Display the DataFrame
                repo_permission_df = pd.DataFrame(repo_permissions)
                filepath = '/Users/' + username + '/Desktop/Bitbucket_Permissions/' + project_key + '/' + repository_slug + '.csv'
                repo_permission_df.to_csv(filepath, index=False)
            else: 
                print("no branch permisisons for Project/Respository {project_key}/{repository_slug}: repository_branch_permissions.status_code".format(project_key=project_key, repository_slug=repository_slug))
        else:
            print("Project/Respository {project_key}/{repository_slug}: is archived".format(project_key=project_key, repository_slug=repository_slug))
