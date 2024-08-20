check_directories() {
    directories=(
        "/etc/ftp-dir/GZKA/LOG1_A/"
        "/etc/ftp-dir/GZKA/RF_VOLT/"
        "/etc/ftp-dir/MOLO/LOG1_A/"
        "/etc/ftp-dir/Q189/LOG1_A/"
        "/etc/ftp-dir/Q189/RF_VOLT/"
        "/etc/ftp-dir/Q204/LOG1_A/"
        "/etc/ftp-dir/Q204/RF_VOLT/"
        "/etc/ftp-dir/Q208/LOG1_A/"
        "/etc/ftp-dir/Q208/RV_VOLT/"
        "/etc/ftp-dir/HWPP/LOG1_A/"
        "/etc/ftp-dir/HWPP/RF_VOLT/"
        "/etc/ftp-dir/TULA/LOG1_A/"
        "/etc/ftp-dir/TULA/RF_VOLT/"
    )

    today=$(date +"%b %e")
    missing_files=0

    for dir in "${directories[@]}"; do
        if ! ls -l "$dir" | grep -q "$today"; then
            echo "$dir"
            missing_files=1
        fi
    done

    if [ $missing_files -eq 0 ]; then
        echo "Ok"
    fi
}

# Call the function
check_directories

