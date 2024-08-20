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

    # Function to list all prefixes recursively
    def list_prefixes(prefix):
        prefixes = []
        paginator = s3.get_paginator('list_objects_v2')
        for page in paginator.paginate(Bucket=bucket_name, Prefix=prefix, Delimiter='/'):
            if 'CommonPrefixes' in page:
                for common_prefix in page['CommonPrefixes']:
                    prefixes.append(common_prefix['Prefix'])
                    prefixes.extend(list_prefixes(common_prefix['Prefix']))
        return prefixes

    all_prefixes = list_prefixes('')

    # Check each prefix for today's uploads
    for prefix in all_prefixes:
      has_today_uploads = False  # Flag to track uploads in current prefix
      for obj in list_objects_recursive(prefix):
        last_modified = obj['LastModified'].date()
        if last_modified == today:
          has_today_uploads = True
          break  # Exit inner loop if upload found

    # Check flag after inner loop
      if not has_today_uploads:
        return 'No uploads today in prefix: {}'.format(prefix)  # Customize message

    return 'Ok '
bucket_name = 'chris-rv55-vpn-setup-logs'
status = check_s3_uploads_today(bucket_name)
print(status)
