FROM ubuntu:16.04
RUN sed -i 's/archive.ubuntu.com/mirrors.aliyun.com/g' /etc/apt/sources.list && apt update && apt-get install -y lib32z1 xinetd && rm -rf /var/lib/apt/lists/ && rm -rf /root/.cache && apt-get autoclean && rm -rf /tmp/* /var/lib/apt/* /var/cache/* /var/log/*
COPY xinetd.conf /etc/xinetd.d/babyheap
COPY service.sh /service.sh
RUN chmod +x ./service.sh
#add user and flag
RUN useradd -m pwn1 && echo 'flag{5a105e8b9d40e1329780d62ea2265d8a}' > /home/pwn1/flag
#copy binary file
COPY babyheap /home/pwn1/babyheap
COPY ./catflag /home/pwn1/bin/sh
#set execution
RUN chown -R root:pwn1 /home/pwn1 && chmod -R 750 /home/pwn1 && chmod 740 /home/pwn1/flag
#copy lib,/bin
RUN cp -R /lib* /home/pwn1 && cp -R /usr/lib* /home/pwn1 && mkdir /home/pwn1/dev && mknod /home/pwn1/dev/null c 1 3 && mknod /home/pwn1/dev/zero c 1 5 && mknod /home/pwn1/dev/random c 1 8 && mknod /home/pwn1/dev/urandom c 1 9 && chmod 666 /home/pwn1/dev/* && cp /bin/sh /home/pwn1/bin && cp /bin/ls /home/pwn1/bin && cp /bin/cat /home/pwn1/bin
CMD './service.sh'
