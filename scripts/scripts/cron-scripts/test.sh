#!/bin/bash

# List of script paths
scripts=(
    "/home/ec2-user/scripts/cron-scripts/ftp-file-check-TULA.py"
    "/home/ec2-user/scripts/cron-scripts/ftp-file-check-TULA-RF.py"
    "/home/ec2-user/scripts/cron-scripts/ftp-file-check-HWPP.py"
    "/home/ec2-user/scripts/cron-scripts/ftp-file-check-HWPP-RF.py"
    "/home/ec2-user/scripts/cron-scripts/ftp-file-check-GZKA.py"
    "/home/ec2-user/scripts/cron-scripts/ftp-file-check-GZKA-RF.py"
    "/home/ec2-user/scripts/cron-scripts/ftp-file-check-MOLO.py"
    "/home/ec2-user/scripts/cron-scripts/ftp-file-check-Q208.py"
    "/home/ec2-user/scripts/cron-scripts/ftp-file-check-Q208-RF.py"
    "/home/ec2-user/scripts/cron-scripts/ftp-file-check-Q204.py"
    "/home/ec2-user/scripts/cron-scripts/ftp-file-check-Q204-RF.py"
    "/home/ec2-user/scripts/cron-scripts/ftp-file-check-Q189.py"
    "/home/ec2-user/scripts/cron-scripts/ftp-file-check-Q189-RF.py"
)

# Check if each script exists
all_exist=true
for script in "${scripts[@]}"; do
    if [ ! -f "$script" ]; then
        echo "Missing: $script"
        all_exist=false
    fi
done

if $all_exist; then
    echo "All scripts exist."
else
    echo "Some scripts are missing."
fi

