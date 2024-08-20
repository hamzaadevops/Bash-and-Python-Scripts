import boto3
import os
import datetime as dt


def main():
    topicArn = 'arn:aws:sns:us-west-1:644620976720:Chris_ftp-server_file-check_Topic'
    snsClient = boto3.client(
        'sns',
        region_name='us-west-1'
    )
    response: object = snsClient.publish(TopicArn=topicArn,
                                         Message='Dear Team, please check TULA RF_VOLT location, today\'s file is not recieved',
                                         Subject='Alert: FTP Server TULA File Check'
                                         )
    print('This is the SNS topic')
def check_file_exist(file_path):
    today = dt.datetime.now().date()
    list = []
    index = 0
    for file in os.listdir(file_path):
        filetime = dt.datetime.fromtimestamp(
            os.path.getctime(file_path + file))
        if filetime.date() == today:
            list.append(index + 1)

    if not len(list) > 0:
        main()

check_file_exist('/etc/ftp-dir/TULA/RF_VOLT/')
