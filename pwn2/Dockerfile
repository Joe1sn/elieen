FROM ubuntu:18.04
RUN sed -i 's/archive.ubuntu.com/mirrors.aliyun.com/g' /etc/apt/sources.list && apt update && apt-get install -y lib32z1 xinetd && rm -rf /var/lib/apt/lists/ && rm -rf /root/.cache && apt-get autoclean && rm -rf /tmp/* /var/lib/apt/* /var/cache/* /var/log/*
COPY xinetd.conf /etc/xinetd.d/babyheap
COPY service.sh /service.sh
RUN chmod +x ./service.sh
#add user and flag
RUN useradd -m pwn2 && echo 'flag{ad0234829205b9033196ba818f7a872b}' > /home/pwn2/flag
#copy binary file
COPY babyheap /home/pwn2/babyheap
COPY ./catflag /home/pwn2/bin/sh
#set execution
RUN chown -R root:pwn2 /home/pwn2 && chmod -R 750 /home/pwn2 && chmod 740 /home/pwn2/flag
#copy lib,/bin
RUN cp -R /lib* /home/pwn2 && cp -R /usr/lib* /home/pwn2 && mkdir /home/pwn2/dev && mknod /home/pwn2/dev/null c 1 3 && mknod /home/pwn2/dev/zero c 1 5 && mknod /home/pwn2/dev/random c 1 8 && mknod /home/pwn2/dev/urandom c 1 9 && chmod 666 /home/pwn2/dev/* && cp /bin/sh /home/pwn2/bin && cp /bin/ls /home/pwn2/bin && cp /bin/cat /home/pwn2/bin
CMD './service.sh'
