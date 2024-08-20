#!/bin/bash

# Define the directories to check
directories=(
    "/etc/ftp-dir/GZKA/LOG1_A/"
    "/etc/ftp-dir/GZKA/RF_VOLT/"
    "/etc/ftp-dir/MOLO/LOG1_A/"
    "/etc/ftp-dir/MOLO/RF_VOLT/"
    "/etc/ftp-dir/Q189/LOG1_A/"
    "/etc/ftp-dir/Q189/RF_VOLT/"
    "/etc/ftp-dir/Q204/LOG1_A/"
    "/etc/ftp-dir/Q204/RF_VOLT/"
    "/etc/ftp-dir/Q208/LOG1_A/"
    "/etc/ftp-dir/Q208/RF_VOLT/"
    "/etc/ftp-dir/HWPP/LOG1_A/"
    "/etc/ftp-dir/HWPP/RF_VOLT/"
    "/etc/ftp-dir/TULA/LOG1_A/"
    "/etc/ftp-dir/TULA/RF_VOLT/"
)

# Initialize a variable to track if all directories are safe
all_safe=true
unsafe_dirs=()

# Loop through directories to find files older than 60 days
for dir in "${directories[@]}"; do
    if [ -d "$dir" ]; then
        old_files=$(find "$dir" -type f -mtime +60)
        
        if [ -n "$old_files" ]; then
            all_safe=false
            unsafe_dirs+=("$dir")
        fi
    else
        echo "Directory $dir does not exist."
    fi
done

# Print the result
if $all_safe; then
    echo "Ok"
else
    echo "Directories containing files older than 60 days:"
    for dir in "${unsafe_dirs[@]}"; do
        echo "$dir"
    done
fi

