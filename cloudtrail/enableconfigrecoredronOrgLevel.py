import boto3

def enable_config_recorder():
    # Create a Config service client
    client = boto3.client('config')

    # Enable the Config recorder at the organization level
    try:
        response = client.put_organization_config_rule(
            OrganizationConfigRuleName='EnableOrganizationConfigRule',
            OrganizationManagedRuleMetadata={
                'RuleIdentifier': 'AWS_CONFIG_ENABLED',
                'Description': 'Enables AWS Config Recorder at organization level',
                'RuleName': 'Enable AWS Config Recorder at organization level',
                'MaximumExecutionFrequency': 'TwentyFour_Hours',
                'ResourceIdScope': 'Organization',
                'ResourceTypesScope': [],
                'InputParameters': '{}',
                'ResourceValue': {},
                'TagKeyScope': '',
                'TagValueScope': ''
            }
        )
        print("AWS Config recorder has been enabled at the organization level.")

    except client.exceptions.OrganizationAccessDeniedException:
        print("Error: You do not have sufficient permissions to enable AWS Config recorder at the organization level.")


# Enable the Config recorder at the organization level
enable_config_recorder()
