import requests
import json

# Enter your Bitbucket credentials
username = 'username'
password = 'password!'
url = "https://git.cauliflower.com/rest/branch-permissions/latest/projects/TES/restrictions"

headers = {
  "Accept": "application/json",
  "Content-Type": "application/json"
}

payload = json.dumps( {
  "accessKeyIds": [],
  "accessKeys": [],
  "groupNames": [],
  "groups": [
    "new_group"
  ],
  "matcher": {
    "displayId": "main",
    "id": "main",
    "type": {
      "id": "BRANCH",
      "name": "Branch"
    }
  },
  "type": "fast-forward-only",
  "userSlugs": [],
  "users": []
} )

response = requests.request(
   "POST",
   url,
   auth=(username, password),
   data=payload,
   headers=headers
)

print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))
