#!/bin/sh
# Add your startup script
if [ -n "$FLAG" ]; then
    echo $FLAG > /home/pwn/flag
    chown root:pwn /home/pwn/flag
    chmod 640 /home/pwn/flag
    export FLAG=not_flag
    FLAG=not_flag
fi
/etc/init.d/xinetd start;
sleep infinity;