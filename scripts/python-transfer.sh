#!/bin/sh

sudo find /etc/ftp-dir/GZKA/LOG1_A -type f -mtime -1 -exec sudo python3 /home/ec2-user/scripts/unavco_datain_upload.py "{}"  \;
