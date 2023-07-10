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

# Specify the name of the CloudTrail to disable
trail_name = 'examplecloudtrail'

# Disable the CloudTrail
disable_cloudtrail(trail_name)
