import boto3

def get_security_group_inbound_rules(security_group_id, region_name='us-east-1'):
    # Initialize a session using Amazon EC2
    ec2 = boto3.client('ec2', region_name=region_name)
    
    try:
        # Describe the security group
        response = ec2.describe_security_groups(GroupIds=[security_group_id])
        
        # Extract the security group details
        security_group = response['SecurityGroups'][0]
        inbound_rules = security_group['IpPermissions']
        
        for rule in inbound_rules:
            from_port = rule.get('FromPort', 'All')
            to_port = rule.get('ToPort', 'All')
            
            # Filter for ports 2000 to 2006
            if from_port in range(2000, 2007) or to_port in range(2000, 2007):
                ip_protocol = rule.get('IpProtocol', 'All')
                ip_ranges = [ip_range['CidrIp'] for ip_range in rule.get('IpRanges', [])]
                ipv6_ranges = [ipv6_range['CidrIpv6'] for ipv6_range in rule.get('Ipv6Ranges', [])]
                prefix_list_ids = [pl['PrefixListId'] for pl in rule.get('PrefixListIds', [])]
                user_id_group_pairs = [pair['GroupId'] for pair in rule.get('UserIdGroupPairs', [])]
                
                print(f"On Port: {from_port}-{to_port} allowed IPs are {ip_ranges}") 
    
    except boto3.exceptions.Boto3Error as e:
        logging.error(f"Error retrieving security group rules: {str(e)}")
if __name__ == "__main__":
    # Replace with your security group ID and region
    security_group_id = 'sg-0c226b85cd93250df'
    region_name = 'us-west-1'
    get_security_group_inbound_rules(security_group_id, region_name)
