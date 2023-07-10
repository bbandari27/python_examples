import pandas as pd

# JSON response
json_response = {
    "isLastPage": True,
    "limit": 25,
    "size": 8,
    "start": 0,
    "values": [
        # JSON data
    ]
}

# Extract values from JSON
values = json_response["values"]

# Create an empty DataFrame
data = pd.DataFrame()

# Iterate over the values and populate the DataFrame
for item in values:
    project_permissions = {
        "Project": item["scope"]["resourceId"],
        "Permission Users": [user["displayName"] for user in item["users"]],
        "Permission Groups": item["groups"]
    }
    data = data.append(project_permissions, ignore_index=True)

# Display the DataFrame
print(data)
