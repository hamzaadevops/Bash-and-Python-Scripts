#!/bin/sh

rsync -ratlz --rsh="sshpass-1.08/sshpass -p ntsg1234 ssh -o StrictHostKeyChecking=no -l username" /etc/ftp-dir/MOLO GNSS@extserv17.ntsg.umt.edu:/home/GNSS

#rsync -ratlz --rsh="sshpass-1.08/sshpass -p ntsg1234 ssh -o StrictHostKeyChecking=no -l username" /etc/ftp-dir/GZKA GNSS@extserv17.ntsg.umt.edu:/home/GNSS
