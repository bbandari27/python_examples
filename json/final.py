import json
import requests
import csv

def append_csv_values_to_json_groups(json_file_path, csv_file_path, output_file_path):
    # Load JSON data
    with open(json_file_path, 'r') as json_file:
        json_data = json.load(json_file)

    # Load CSV data
    csv_data = []
    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        csv_data = list(csv_reader)

    # Remove specified fields from JSON data
    json_data.pop('accessKeys', None)
    json_data.pop('id', None)
    json_data['matcher'].pop('active', None)
    json_data.pop('scope', None)
    json_data['users'] = [user['name'] for user in json_data['users']]

    # Extract existing groups from JSON
    existing_groups = json_data['groups']

    # Iterate over CSV rows
    for csv_row in csv_data:
        csv_groups = [group.strip() for group in csv_row[0].split(',')]
        csv_value = csv_row[1].strip()
        for group in csv_groups:
            if group in existing_groups:
                json_data['groups'].append(csv_value)

    # Save updated JSON data
    with open(output_file_path, 'w') as json_file:
        json.dump(json_data, json_file, indent=4)

    # Perform the example response POST request
    url = 'https://example.com/api/response'
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(json_data), headers=headers)
    print(response.text)

# Example usage:
append_csv_values_to_json_groups('data.json', 'data.csv', 'updated_data.json')
