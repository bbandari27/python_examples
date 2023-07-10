import boto3

def disable_config_recorder(recorder_name):
    # Create a Config service client
    client = boto3.client('config')
    
    # Check if the specified recorder exists
    try:
        response = client.describe_configuration_recorder_status(ConfigurationRecorderNames=[recorder_name])
        recorders = response['ConfigurationRecordersStatus']
        
        if len(recorders) == 1:
            recorder = recorders[0]
            
            # Disable the recorder
            if recorder['Recording']:
                client.stop_configuration_recorder(ConfigurationRecorderName=recorder_name)
                print(f"AWS Config recorder '{recorder_name}' has been disabled.")
            else:
                print(f"AWS Config recorder '{recorder_name}' is already disabled.")
        else:
            print(f"AWS Config recorder '{recorder_name}' does not exist.")
    
    except client.exceptions.NoSuchConfigurationRecorderException:
        print(f"AWS Config recorder '{recorder_name}' does not exist.")

# Specify the name of the Config recorder to disable
recorder_name = 'exampleconfig'

# Disable the Config recorder
disable_config_recorder(recorder_name)
