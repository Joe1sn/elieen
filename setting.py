import json


class docker(object):
    """docstring for docker_info"""

    def __init__(self, config_filename="config.json"):
        super(docker, self).__init__()
        with open(config_filename, "r") as file:
            config = json.loads(file.read())
        self.os = config["docker_info"]["os"]["unix"] + ":" + config["docker_info"]["os"]["version"]
        self.libc_version = config["docker_info"]["libc_version"]
        self.image_name = config["docker_info"]["docker_image_name"]
        self.container_name = config["docker_info"]["docker_container_name"]
        self.flag = config["docker_info"]["flag"]
        self.port = config["docker_info"]["port"]
        self.bin_file = config["docker_info"]["filename"]
        self.xient_config_filename = config["docker_info"]["xient_config"]

    def dockerfile(self, docker_username="pwn",
                   work_dir="/home/pwn",
                   flag_filename="flag.txt"):
        return \
            '''FROM {os}
            
            RUN sed -i 's/archive.ubuntu.com/asia-east1.gce.archive.ubuntu.com/g' /etc/apt/sources.list && apt update && apt-get install -y lib32z1 xinetd && rm -rf /var/lib/apt/lists/ && rm -rf /root/.cache && apt-get autoclean && rm -rf /tmp/* /var/lib/apt/* /var/cache/* /var/log/*
            
            COPY ./{xient_config_filename} /etc/xinetd.d/pwn
            
            #add user and flag
            RUN useradd -m {username} &&echo '{flag}' > {work_dir}/{flag_filename}
            
            #copy binary file
            COPY ./bin/{filename} {work_dir}/{filename}
            
            #set execution
            RUN chown -R root:{username} {work_dir} && chmod -R 750 {work_dir} && chmod 740 {work_dir}/{flag_filename}
            
            #copy lib,/bin
            RUN cp -R /lib* {work_dir} && cp -R /usr/lib* {work_dir} && mkdir {work_dir}/dev && mknod {work_dir}/dev/null c 1 3 && mknod {work_dir}/dev/zero c 1 5 && mknod {work_dir}/dev/random c 1 8 && mknod {work_dir}/dev/urandom c 1 9 && chmod 666 {work_dir}/dev/* && cp /bin/sh {work_dir}/bin && cp /bin/ls {work_dir}/bin && cp /bin/cat {work_dir}/bin
            '''.format(
                os=self.os,
                username=docker_username,
                xient_config_filename=self.xient_config_filename,
                work_dir=work_dir,
                flag=self.flag,
                filename=self.bin_file,
                flag_filename=flag_filename
            )


class xient(object):
    """docstring for xient_info"""

    def __init__(self, config_filename="config.json"):
        super(xient, self).__init__()
        with open(config_filename, "r") as file:
            config = json.loads(file.read())
        self.service_name = config["xient_info"]["service_name"]
        self.user = config["xient_info"]["user"]
        self.port = config["xient_info"]["port"]
        self.protocol = config["xient_info"]["protocol"]
        self.server_arg = config["xient_info"]["server_arg"]

    def xient_file(self):
        return \
            '''service {name}
            {{
                disable = no
                socket_type = stream
                protocol    = {protocol}
                wait        = no
                user        = {user}
                type        = UNLISTED
                port        = {port}
                bind        = 0.0.0.0
                server      = /usr/sbin/chroot   
                server_args = {server_arg}
                # safety options
                per_source  = 10 # the maximum instances of this service per source IP address
                rlimit_cpu  = 20 # the maximum number of CPU seconds that the service may use
                rlimit_as  = 100M # the Address Space resource limit for the service
                #access_times = 2:00-9:00 12:00-24:00
            }}'''.format(
                name=self.service_name,
                protocol=self.protocol,
                user=self.user,
                port=self.port,
                server_arg=self.server_arg
            )
