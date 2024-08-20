#!/bin/sh

# TULA
python3 /home/ec2-user/scripts/cron-scripts/ftp-file-check-TULA.py;
python3 /home/ec2-user/scripts/cron-scripts/ftp-file-check-TULA-RF.py;

# QHWPP
python3 /home/ec2-user/scripts/cron-scripts/ftp-file-check-HWPP.py;
python3 /home/ec2-user/scripts/cron-scripts/ftp-file-check-HWPP-RF.py;

# GZKA
python3 /home/ec2-user/scripts/cron-scripts/ftp-file-check-GZKA.py;
python3 /home/ec2-user/scripts/cron-scripts/ftp-file-check-GZKA-RF.py;

# MOLO
python3 /home/ec2-user/scripts/cron-scripts/ftp-file-check-MOLO.py;

# Q208
python3 /home/ec2-user/scripts/cron-scripts/ftp-file-check-Q208.py;
python3 /home/ec2-user/scripts/cron-scripts/ftp-file-check-Q208-RF.py;

# Q204
python3 /home/ec2-user/scripts/cron-scripts/ftp-file-check-Q204.py;
python3 /home/ec2-user/scripts/cron-scripts/ftp-file-check-Q204-RF.py;

# Q189
python3 /home/ec2-user/scripts/cron-scripts/ftp-file-check-Q189.py;
python3 /home/ec2-user/scripts/cron-scripts/ftp-file-check-Q189-RF.py;

