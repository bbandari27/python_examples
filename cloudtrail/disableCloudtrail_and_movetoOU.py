import boto3

def disable_cloudtrail(trail_name):
    # Create a CloudTrail client
    client = boto3.client('cloudtrail')

    # Check if the specified trail exists
    try:
        response = client.describe_trails(trailNameList=[trail_name])
        trails = response['trailList']

        if len(trails) == 1:
            trail = trails[0]

            # Disable the trail
            if trail['IsLogging']:
                client.stop_logging(Name=trail_name)
                print(f"CloudTrail '{trail_name}' has been disabled.")
            else:
                print(f"CloudTrail '{trail_name}' is already disabled.")
        else:
            print(f"CloudTrail '{trail_name}' does not exist.")

    except client.exceptions.TrailNotFoundException:
        print(f"CloudTrail '{trail_name}' does not exist.")


def move_to_managed_ou(trail_name, destination_ou_id):
    # Create an Organizations client
    organizations_client = boto3.client('organizations')

    # Check if the specified OU exists
    try:
        response = organizations_client.describe_organizational_unit(
            OrganizationalUnitId=destination_ou_id
        )
        destination_ou = response['OrganizationalUnit']

        # Move the CloudTrail to the destination OU
        client = boto3.client('cloudtrail')
        client.update_trail(
            Name=trail_name,
            IsOrganizationTrail=True,
            TrailARN=destination_ou['Arn']
        )
        print(f"CloudTrail '{trail_name}' has been moved to the destination OU.")

    except organizations_client.exceptions.OrganizationalUnitNotFoundException:
        print(f"Destination OU with ID '{destination_ou_id}' does not exist.")


# Specify the name of the CloudTrail and the destination OU ID
trail_name = 'examplecloudtrail'
destination_ou_id = 'ou-xxxxxxxxx'  # Replace with the actual destination OU ID

# Disable the CloudTrail
disable_cloudtrail(trail_name)

# Move the CloudTrail to the Control Tower managed OU
move_to_managed_ou(trail_name, destination_ou_id)
