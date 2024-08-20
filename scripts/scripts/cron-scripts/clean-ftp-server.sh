#!/bin/sh

find /etc/ftp-dir/ -type f -mtime +60 -exec sudo rm -rf {} \;
