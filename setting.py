import json


class docker(object):
    """docstring for docker_info"""

    def __init__(self, config_filename="config.json"):
        super(docker, self).__init__()
        with open(config_filename, "r") as file:
            config = json.loads(file.read())
        self.os = config["docker_info"]["os"]["release"] + ":" + config["docker_info"]["os"]["version"]
        self.flag = config["docker_info"]["flag"]
        self.port = config["docker_info"]["port"]
        self.bin_file = config["docker_info"]["filename"]
        self.xient_config_filename = config["docker_info"]["xient_config"]

    def dockerfile(self, docker_username="pwn",
                   work_dir="/home/pwn",
                   flag_filename="flag.txt",
                   startup_script_name="service.sh"):
        return \
            "FROM {os}\n" \
            "RUN sed -i 's/archive.ubuntu.com/mirrors.aliyun.com/g' /etc/apt/sources.list && apt update && apt-get install -y lib32z1 xinetd && rm -rf /var/lib/apt/lists/ && rm -rf /root/.cache && apt-get autoclean && rm -rf /tmp/* /var/lib/apt/* /var/cache/* /var/log/*\n" \
            "COPY ./{xient_config_filename} /etc/xinetd.d/pwn\n" \
            "COPY ./{startup_script_name} /{startup_script_name}\n" \
            "RUN chmod +x ./{startup_script_name}\n" \
            "#add user and flag\n" \
            "RUN useradd -m {username} &&echo '{flag}' > {work_dir}/{flag_filename}\n" \
            "#copy binary file\n" \
            "COPY ./bin/{filename} {work_dir}/{filename}\n" \
            "#set execution\n" \
            "RUN chown -R root:{username} {work_dir} && chmod -R 750 {work_dir} && chmod 740 {work_dir}/{flag_filename}\n" \
            "#copy lib,/bin\n" \
            "RUN cp -R /lib* {work_dir} && cp -R /usr/lib* {work_dir} && mkdir {work_dir}/dev && mknod {work_dir}/dev/null c 1 3 && mknod {work_dir}/dev/zero c 1 5 && mknod {work_dir}/dev/random c 1 8 && mknod {work_dir}/dev/urandom c 1 9 && chmod 666 {work_dir}/dev/* && cp /bin/sh {work_dir}/bin && cp /bin/ls {work_dir}/bin && cp /bin/cat {work_dir}/bin\n" \
            "CMD './{startup_script_name}'\n" \
                .format(
                os=self.os,
                username=docker_username,
                xient_config_filename=self.xient_config_filename,
                work_dir=work_dir,
                flag=self.flag,
                filename=self.bin_file,
                flag_filename=flag_filename,
                startup_script_name=startup_script_name
            )

    def docker_composer(self, version="2",
                        image_list=[],
                        container_name_list=[],
                        ):
        pass


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
            "service {name}\n" \
            "{{\n" \
            "    disable = no\n" \
            "    socket_type = stream\n" \
            "    protocol    = {protocol}\n" \
            "    wait        = no\n" \
            "    user        = {user}\n" \
            "    type        = UNLISTED\n" \
            "    port        = {port}\n" \
            "    bind        = 0.0.0.0\n" \
            "    server      = /usr/sbin/chroot   \n" \
            "    server_args = {server_arg}\n" \
            "    # safety options\n" \
            "    per_source  = 10 # the maximum instances of this service per source IP address\n" \
            "    rlimit_cpu  = 20 # the maximum number of CPU seconds that the service may use\n" \
            "    rlimit_as  = 100M # the Address Space resource limit for the service\n" \
            "    #access_times = 2:00-9:00 12:00-24:00\n" \
            "}}\n" \
                .format(
                name=self.service_name,
                protocol=self.protocol,
                user=self.user,
                port=self.port,
                server_arg=self.server_arg
            )
