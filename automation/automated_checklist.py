## Environment variable
# ADMIN USER and PASSWORD line 84 and 85
# Instance USER and PASS line 165 and 166

import boto3
import paramiko
import gspread
import requests
from oauth2client.service_account import ServiceAccountCredentials
from datetime import date
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def check_instance_health(region_name, instance_id):
    """Check the health of an EC2 instance."""
    try:
        ec2 = boto3.client('ec2', region_name=region_name)
        response = ec2.describe_instance_status(InstanceIds=[instance_id])
        instance_statuses = response.get('InstanceStatuses', [])

        if not instance_statuses:
            return "Not Ok"

        instance_status = instance_statuses[0]
        system_status = instance_status.get('SystemStatus', {}).get('Status')
        instance_status_state = instance_status.get('InstanceStatus', {}).get('Status')

        if system_status != "ok" or instance_status_state != "ok":
            return "Not Ok"
        return "Ok"
    except boto3.exceptions.Boto3Error as e:
        logging.error(f"Error checking instance health for {instance_id}: {str(e)}")
        return "Not Ok"

def check_url_status(url):
    """Check the status of a URL."""
    try:
        response = requests.get(url, timeout=8)
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        logging.error(f"Error checking {url}: {str(e)}")
        return False

def get_status(urls):
    """Check the status of multiple URLs."""
    all_up = True
    for url in urls:
        if check_url_status(url):
            logging.info(f"{url} is UP")
        else:
            logging.info(f"{url} is DOWN")
            all_up = False
    return "Ok" if all_up else "Not Ok"

def create_new_sheet_and_update_status(credentials_file, sheet_id, status_data, row_indices):
    """Create a new Google Sheets sheet and update it with the given status data."""
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scope)
        client = gspread.authorize(creds)

        sheet = client.open_by_key(sheet_id)
        sheets = sheet.worksheets()
        last_worksheet = sheets[0]

        today = date.today().strftime("%Y-%m-%d")
        new_worksheet = last_worksheet.duplicate(new_sheet_name=today)

        # Update cells with status data
        for row, (status, remark) in zip(row_indices, status_data):
            new_worksheet.update_cell(row, 2, status)
            new_worksheet.update_cell(row, 4, remark)
            new_worksheet.update_cell(row, 3, "")  # Clear status column

    except gspread.exceptions.GSpreadException as e:
        logging.error(f"Error updating Google Sheet: {str(e)}")

def check_streaming():
    """Check the streaming status of sensors."""
    url = "http://172.31.13.223:9000/haproxy_stats"
    username = os.getenv('STREAM_USERNAME', 'ADMIN')
    password = os.getenv('STREAM_PASSWORD', 'PASSWORD')

    sensors = ["Q208", "Q204", "Q189", "DWR6", "GZKA", "DWR7"]
    non_matching_sensors = []

    try:
        response = requests.get(url, auth=(username, password))
        response.raise_for_status()

        for sensor in sensors:
            count = response.text.count(sensor)
            if count != 15:
                non_matching_sensors.append(sensor)

        return "Ok" if not non_matching_sensors else f"Sensors not equal to 15 occurrences: {', '.join(non_matching_sensors)}"
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

def run_remote_script(hostname, port, username, password, remote_script_path):
    """Run a remote script via SSH and return the output."""
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname, port, username, password)

        commands = [
            "/usr/bin/python3 ~/scripts/automation_scripts/s3-4char.py",
            "~/scripts/automation_scripts/today_files_received.sh",
            "/usr/bin/python3 ~/scripts/automation_scripts/health-check.py",
            "~/scripts/automation_scripts/check_before_60.sh",
            "/usr/bin/python3 ~/scripts/automation_scripts/sg.py"
        ]

        results = {}
        for command in commands:
            stdin, stdout, stderr = ssh.exec_command(command)
            result = stdout.read().decode().strip()
            error = stderr.read().decode().strip()
            if error:
                logging.error(f"Error running remote script '{command}': {error}")
                return None
            results[command] = result

        ssh.close()
        return results
    except (paramiko.AuthenticationException, paramiko.SSHException, paramiko.BadHostKeyException) as e:
        logging.error(f"SSH error: {str(e)}")
        return None

if __name__ == "__main__":
    sensor_urls = [
        "http://10.128.0.2/",
        "http://10.128.0.18/",
        "http://10.128.0.26/",
        "http://10.128.0.34/",
        "http://10.128.0.42/",
        "http://10.128.0.66/",
        "http://10.128.0.74/"
    ]

    routers_urls = [
        "http://10.128.0.1:9191/",
        "http://10.128.0.17:9191/",
        "http://10.128.0.25:9191/",
        "http://10.128.0.33:9191/",
        "http://10.128.0.41:9191/",
        "http://10.128.0.65:9191/",
        "http://10.128.0.73:9191/"
    ]

    sensors_remarks = get_status(sensor_urls)
    sensors_status = 'Not Ok' if sensors_remarks != 'Ok' else "Ok "
    routers_remarks = get_status(routers_urls)
    routers_status = 'Not Ok' if routers_remarks != 'Ok' else "Ok "

    stream_remarks = check_streaming()
    stream_status = 'Not Ok' if stream_remarks != 'Ok' else "Ok "

    hostname = "172.31.15.57"
    port = 22
    username = os.getenv('SSH_USERNAME', 'USER')
    password = os.getenv('SSH_PASSWORD', 'PASS')
    remote_script_path = "./scripts/s3.py"

    remote_results = run_remote_script(hostname, port, username, password, remote_script_path)
    if not remote_results:
        logging.error("Failed to retrieve remote script results")
        exit(1)

    s3_remarks = remote_results.get("/usr/bin/python3 ~/scripts/automation_scripts/s3-4char.py", "Not Ok")
    files_status = remote_results.get("~/scripts/automation_scripts/today_files_received.sh", "Not Ok")
    server_status = remote_results.get("/usr/bin/python3 ~/scripts/automation_scripts/health-check.py", "")
    old_remarks = remote_results.get("~/scripts/automation_scripts/check_before_60.sh", "Not Ok")
    sg_remarks = remote_results.get("/usr/bin/python3 ~/scripts/automation_scripts/sg.py", "Failed to get details")

    vpn_status, ftp_status, haproxy_status = [status.strip() for status in server_status.split()]

    old_status = 'Ok ' if old_remarks == 'Ok' else 'Not Ok'
    old_remarks = "Old Files are deleted successfully" if old_status == 'Ok' else old_remarks

    vpn_remarks = 'Instance Health and System Health are Okay' if vpn_status == '0' else "Instance Health Check has some issues. Please check"
    vpn_status = 'Ok ' if vpn_status == '0' else 'Not Ok'

    ftp_remarks = 'Instance Health and System Health are Okay' if ftp_status == '0' else "Instance Health Check has some issues. Please check"
    ftp_status = 'Ok ' if ftp_status == '0' else 'Not Ok'

    haproxy_remarks = 'Instance Health and System Health are Okay' if haproxy_status == '0' else "Instance Health Check has some issues. Please check"
    haproxy_status = 'Ok ' if haproxy_status == '0' else 'Not Ok'

    s3_status = "Ok " if s3_remarks == 'Ok' else "Not Ok"
    s3_remarks = "All Files Received" if s3_status == "Ok " else s3_remarks

    file_status = "Ok " if files_status == "Ok" else "Not Ok"
    files_status = "All Ok" if file_status == "Ok " else files_status

    sg_status = "Not Ok" if sg_remarks == "Failed to get details" else "Ok "

    status_data = [
        (ftp_status, ftp_remarks),
        (vpn_status, vpn_remarks),
        (haproxy_status, haproxy_remarks),
        (file_status, files_status),
        (old_status, old_remarks),
        (s3_status, s3_remarks),
        (sensors_status, sensors_remarks),
        (routers_status, routers_remarks),
        (stream_status, stream_remarks),
        (sg_status, sg_remarks)
    ]

    credentials_file = "credentials.json"
    sheet_id = "1h8BuXsl4jtkKAL9sWDfxyljRHWtXrfwxIyHuORykgB4" # orignal
    row_indices = [2, 3, 4, 5, 6, 9, 10, 11, 12, 13]
    create_new_sheet_and_update_status(credentials_file, sheet_id, status_data, row_indices)


