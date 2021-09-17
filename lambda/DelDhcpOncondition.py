import json
import boto3
import json
import os

def lambda_handler(event, context):

    # Client setup
    region = os.environ['AWS_REGION']
    ec2 = boto3.client("ec2", region_name=region)
    client = boto3.client('ec2')
    dhcp_list = []
    dhcps = client.describe_dhcp_options(
      Filters=[
        {
            'Name' : 'value',
            'Values' : [
                'example.com',
            ],
        },
      ],
    )
    dhcps_str = json.dumps(dhcps)
    resp = json.loads(dhcps_str)
    data = json.dumps(resp['DhcpOptions'])
    dhcps = json.loads(data)
    
    for dhcp in dhcps:
        dhcp_list.append(dhcp['DhcpOptionsId']) 
    
    for dhcp in dhcp_list:
        client.delete_dhcp_options( DhcpOptionsId = dhcp)
        print ("Deleted the dhcp = " + dhcp)
