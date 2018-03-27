ITGRecv -l recv_log_file
ITGSend -a 10.0.0.2 -T UDP -C 100 -c 500
./ITGSend d-itg_script.sh -l send_log_file -L 10.0.0.1 UDP -X 10.0.0.1 UDP -x recv_log_file
