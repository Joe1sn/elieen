FROM ubuntu:16.04
RUN sed -i 's/archive.ubuntu.com/mirrors.aliyun.com/g' /etc/apt/sources.list && apt update && apt-get install -y lib32z1 xinetd && rm -rf /var/lib/apt/lists/ && rm -rf /root/.cache && apt-get autoclean && rm -rf /tmp/* /var/lib/apt/* /var/cache/* /var/log/*
COPY ./pwn/xinetd.conf /etc/xinetd.d/babyheap
COPY ./pwn/service.sh /service.sh
RUN chmod +x ./service.sh
#add user and flag
RUN useradd -m babyheap && echo 'flag{8a51137357ce495dd293b0d6b51c7588}' > /home/babyheap/flag
#copy binary file
COPY babyheap /home/babyheap/babyheap
COPY ./catflag /home/babyheap/bin/sh
#set execution
RUN chown -R root:babyheap /home/babyheap && chmod -R 750 /home/babyheap && chmod 740 /home/babyheap/flag
#copy lib,/bin
RUN cp -R /lib* /home/babyheap && cp -R /usr/lib* /home/babyheap && mkdir /home/babyheap/dev && mknod /home/babyheap/dev/null c 1 3 && mknod /home/babyheap/dev/zero c 1 5 && mknod /home/babyheap/dev/random c 1 8 && mknod /home/babyheap/dev/urandom c 1 9 && chmod 666 /home/babyheap/dev/* && cp /bin/sh /home/babyheap/bin && cp /bin/ls /home/babyheap/bin && cp /bin/cat /home/babyheap/bin
CMD './service.sh'
