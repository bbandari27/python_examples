# Parse the JSON input
data = json.loads(input_json)

# Check if 'dev ops' is present in the 'groups' value
if 'Dev Ops' in data['groups']:
    # Modify the JSON based on the condition
    data['groupNames'] = []
    data['groups'] = ['new devops group']
    data['scope'].pop('resourceId', None)
    data['userSlugs'] = []
    data['users'] = []

# Convert the modified JSON back to a string
output_json = json.dumps(data, indent=4)

print(output_json)
