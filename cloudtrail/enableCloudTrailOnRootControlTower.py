import boto3

def enable_cloudtrail():
    # Create a CloudTrail client
    client = boto3.client('cloudtrail')

    # Enable CloudTrail at the organization level
    try:
        response = client.create_trail(
            Name='OrganizationTrail',
            S3BucketName='your-bucket-name',
            IsMultiRegionTrail=True,
            IsOrganizationTrail=True
        )
        print("AWS CloudTrail has been enabled at the organization level.")

    except client.exceptions.TrailAlreadyExistsException:
        print("Error: CloudTrail 'OrganizationTrail' already exists.")

    except client.exceptions.CloudTrailAccessNotEnabledException:
        print("Error: CloudTrail access has not been enabled at the organization level.")


# Enable AWS CloudTrail at the organization level
enable_cloudtrail()
