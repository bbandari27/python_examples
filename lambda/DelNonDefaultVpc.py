import json
import boto3
import json
import os
  
def lambda_handler(event, context):
 
  # Client setup
  region = os.environ['AWS_REGION']
  ec2 = boto3.client("ec2", region_name=region)
  client = boto3.client('ec2')
  vpc_list = []
  vpcs = client.describe_vpcs(
    Filters=[
      {
        'Name' : 'isDefault',
        'Values' : [
          'false',
        ],
      },
    ]
  )
  vpcs_str = json.dumps(vpcs)
  resp = json.loads(vpcs_str)
  data = json.dumps(resp['Vpcs'])
  vpcs = json.loads(data)
 
  for vpc in vpcs:
    vpc_list.append(vpc['VpcId'])  
    
  for vpc in vpc_list:
    client.delete_vpc(VpcId = vpc)
    print ("Deleted the vpc = " + vpc)
