#!/bin/sh

rsync -ratlz --rsh="sshpass-1.08/sshpass -p Password123!@# ssh -o StrictHostKeyChecking=no -l verquin" /etc/ftp-dir/Q208/ user@EIP:/home/verquin/ftp/GNSSraw/Q208/RAW_15S/ 
rsync -ratlz --rsh="sshpass-1.08/sshpass -p Password123!@# ssh -o StrictHostKeyChecking=no -l verquin" /etc/ftp-dir/Q204/ user@EIP:/home/verquin/ftp/GNSSraw/Q204/RAW_15S/ 
rsync -ratlz --rsh="sshpass-1.08/sshpass -p Password123!@# ssh -o StrictHostKeyChecking=no -l verquin" /etc/ftp-dir/Q189/ user@EIP:/home/verquin/ftp/GNSSraw/Q189/RAW_15S/
rsync -ratlz --rsh="sshpass-1.08/sshpass -p Password123!@# ssh -o StrictHostKeyChecking=no -l verquin" /etc/ftp-dir/MOLO/ user@EIP:/home/verquin/ftp/GNSSraw/MOLO/RAW_15S/ 
rsync -ratlz --rsh="sshpass-1.08/sshpass -p Password123!@# ssh -o StrictHostKeyChecking=no -l verquin" /etc/ftp-dir/GZKA/ user@EIP:/home/verquin/ftp/GNSSraw/GZKA/RAW_15S/ 
rsync -ratlz --rsh="sshpass-1.08/sshpass -p Password123!@# ssh -o StrictHostKeyChecking=no -l verquin" /etc/ftp-dir/TULA/ user@EIP:/home/verquin/ftp/GNSSraw/TULA/RAW_15s/
rsync -ratlz --rsh="sshpass-1.08/sshpass -p Password123!@# ssh -o StrictHostKeyChecking=no -l verquin" /etc/ftp-dir/HWPP/ user@EIP:/home/verquin/ftp/GNSSraw/HWPP/RAW_15s/
