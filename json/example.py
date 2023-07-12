import json

def convert_json(json_data):
    converted_data = {
        'groups': json_data['groups'],
        'matcher': {
            'displayId': json_data['matcher']['displayId'],
            'id': json_data['matcher']['id'],
            'type': {
                'id': json_data['matcher']['type']['id'],
                'name': json_data['matcher']['type']['name']
            }
        },
        'type': json_data['type'],
        'users': [user['name'] for user in json_data['users']]
    }
    return converted_data

# Convert JSON data
converted_json = convert_json(json_data)

# Print converted JSON
print(json.dumps(converted_json, indent=4))
