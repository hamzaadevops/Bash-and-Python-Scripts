import boto3

def check_instance_health(region_name, instance_ids):
    # Create an EC2 client
    ec2 = boto3.client('ec2', region_name=region_name)
    
    # Initialize an empty list to store statuses
    instance_statuses = []
    
    for instanceid in instance_ids:
        # Describe instance status
        response = ec2.describe_instance_status(InstanceIds=[instanceid])
        
        instance_status = response.get('InstanceStatuses', [])
        
        if not instance_status:
            instance_statuses.append("Not Found")
        else:
            # Assuming there's only one instance status record, retrieve its status
            instance_status = instance_status[0]
            system_status = instance_status.get('SystemStatus', {}).get('Status')
            instance_status_state = instance_status.get('InstanceStatus', {}).get('Status')

            # Check if both system and instance statuses are "Ok"
            if system_status == "ok" and instance_status_state == "ok":
                instance_statuses.append("Ok")
            else:
                instance_statuses.append("Not Ok")
    
    return instance_statuses

if __name__ == "__main__":
    region_name = 'us-west-1'  # Change this to your region
    list_of_instanceids = ['i-00bf9c0ebe10b4fcd', 'i-0c74ac8441685cb29', 'i-0f7451a703f97a74f']

    # Call function to get instance health statuses
    instance_health_statuses = check_instance_health(region_name, list_of_instanceids)
    list_of_statuses = []
    # Print the instance health statuses as a comma-separated string
    for health in instance_health_statuses:
        if health == "Ok":
            print(0)
        else:
            print(1)

