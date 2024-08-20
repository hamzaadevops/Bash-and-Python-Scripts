import boto3
from datetime import datetime, timezone

def check_s3_uploads_today(bucket_name):
    # Create an S3 client
    s3 = boto3.client('s3')

    # Get the current date in UTC
    today = datetime.now(timezone.utc).date()

    # Function to list objects recursively
    def list_objects_recursive(prefix):
        paginator = s3.get_paginator('list_objects_v2')
        for page in paginator.paginate(Bucket=bucket_name, Prefix=prefix):
            if 'Contents' in page:
                for obj in page['Contents']:
                    yield obj

    # Function to list all prefixes recursively, excluding the specified folder
    def list_prefixes(prefix):
        prefixes = []
        paginator = s3.get_paginator('list_objects_v2')
        for page in paginator.paginate(Bucket=bucket_name, Prefix=prefix, Delimiter='/'):
            if 'CommonPrefixes' in page:
                for common_prefix in page['CommonPrefixes']:
                    current_prefix = common_prefix['Prefix']
                    # Exclude '4CHAR/' folder
                    if '4CHAR/' not in current_prefix:
                        prefixes.append(current_prefix)
                        prefixes.extend(list_prefixes(current_prefix))
        return prefixes

    # Get all prefixes in the bucket recursively, excluding '4CHAR/'
    all_prefixes = list_prefixes('')

    # Check each prefix for today's uploads
    for prefix in all_prefixes:
        for obj in list_objects_recursive(prefix):
            # Get the last modified date of the object
            last_modified = obj['LastModified'].date()
            
            # Check if the object was uploaded today
            if last_modified == today:
                return 'Ok '

    return 'Not Ok'

# Example usage
bucket_name = 'chris-rv55-vpn-setup-logs'
status = check_s3_uploads_today(bucket_name)
print(status)

