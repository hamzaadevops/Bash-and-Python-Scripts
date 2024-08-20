import boto3
from datetime import datetime, timezone

def get_snapshots_for_today(region_name):
    # Create an EC2 client
    ec2 = boto3.client('ec2', region_name=region_name)
    
    # Get the current date in UTC
    today = datetime.now(timezone.utc).date()
    
    # Describe all snapshots owned by the account
    response = ec2.describe_snapshots(OwnerIds=['self'])

    # Extract snapshot information
    snapshots = response['Snapshots']
    
    # Filter snapshots to include only those created today
    todays_snapshots = [snapshot for snapshot in snapshots if snapshot['StartTime'].date() == today]

    return todays_snapshots

def check_snapshots(region_name):
    todays_snapshots = get_snapshots_for_today(region_name)
    
    # Check the number of snapshots created today
    num_snapshots_today = len(todays_snapshots)
    
    return num_snapshots_today

if __name__ == "__main__":
    region_name = 'us-west-1'  # Change this to your region if needed

    num_snapshots_today = check_snapshots(region_name)
    print(f"Number of snapshots created today in {region_name}: {num_snapshots_today}")

