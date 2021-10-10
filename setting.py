import json
from hashlib import md5
from elieen_help import *
import os
import shutil


def basicfile_transport(filename):
    pass


class docker(object):
    """docstring for docker_info"""

    def __init__(self, config_filename="config.json"):
        super(docker, self).__init__()
        with open(config_filename, "r") as file:
            config = json.loads(file.read())
        self.project_path = config["project_path"]
        self.os = config["docker_info"]["os"]["release"] + ":" + config["docker_info"]["os"]["version"]
        self.flag = "flag{" + md5(bytes(config["docker_info"]["flag"], encoding="utf-8")).hexdigest() + "}"
        self.port = config["docker_info"]["port"]
        self.bin_filename = config["filename"]
        self.bin_file = os.path.join(self.project_path,config["filename"])
        self.xinetd_config_filename = config["docker_info"]["xinetd_config"]
        self.xinetd_config_file = os.path.join(self.project_path, config["docker_info"]["xinetd_config"])

        if not os.path.exists(self.project_path):
            warn(self.project_path + "is not exists")
            warn("now automatic create path " + self.project_path)
            try:
                os.makedirs(self.project_path)
                succed("path is created")
            except Exception as e:
                error("path in config.json create failed!")
                error(e)

    def dockerfile(self, docker_username="pwn",
                   work_dir="/home/pwn",
                   flag_filename="flag",
                   startup_script_name="service.sh"):
        return \
            "FROM {os}\n" \
            "RUN sed -i 's/archive.ubuntu.com/mirrors.aliyun.com/g' /etc/apt/sources.list && apt update && apt-get install -y lib32z1 xinetd && rm -rf /var/lib/apt/lists/ && rm -rf /root/.cache && apt-get autoclean && rm -rf /tmp/* /var/lib/apt/* /var/cache/* /var/log/*\n" \
            "COPY {project_path}{xinetd_config_filename} /etc/xinetd.d/pwn\n" \
            "COPY {project_path}{startup_script_name} /{startup_script_name}\n" \
            "RUN chmod +x ./{startup_script_name}\n" \
            "#add user and flag\n" \
            "RUN useradd -m {username} &&echo '{flag}' > {work_dir}/{flag_filename}\n" \
            "#copy binary file\n" \
            "COPY {filename} {work_dir}/{filename}\n" \
            "COPY ./catflag /home/pwn/bin/sh\n" \
            "#set execution\n" \
            "RUN chown -R root:{username} {work_dir} && chmod -R 750 {work_dir} && chmod 740 {work_dir}/{flag_filename}\n" \
            "#copy lib,/bin\n" \
            "RUN cp -R /lib* {work_dir} && cp -R /usr/lib* {work_dir} && mkdir {work_dir}/dev && mknod {work_dir}/dev/null c 1 3 && mknod {work_dir}/dev/zero c 1 5 && mknod {work_dir}/dev/random c 1 8 && mknod {work_dir}/dev/urandom c 1 9 && chmod 666 {work_dir}/dev/* && cp /bin/sh {work_dir}/bin && cp /bin/ls {work_dir}/bin && cp /bin/cat {work_dir}/bin\n" \
            "CMD './{startup_script_name}'\n" \
                .format(
                os=self.os,
                username=docker_username,
                xinetd_config_filename=self.xinetd_config_filename,
                work_dir=work_dir,
                flag=self.flag,
                filename=self.bin_filename,
                flag_filename=flag_filename,
                startup_script_name=startup_script_name,
                project_path=self.project_path
            )

    def set_dockerfile(self, dockerfile_name="Dockerfile"):
        try:
            with open(os.path.join(self.project_path,dockerfile_name), "w", encoding="utf-8") as file:
                file.write(docker().dockerfile())
            succed("{filename} is generated".format(filename=dockerfile_name))
            tips("now copy the basic files")
            shutil.copy("./service.sh", self.project_path)
            shutil.copy("./catflag", self.project_path)
            shutil.copy(self.bin_filename, self.project_path)
            tips("using command below to build and run docker")
            tips("sudo docker build -f <project dir>/Dockerfile -t <image_name> .")
            tips("sudo docker run -p <expose_port>:<docker_port> -d <image_name>")

        except (Exception, BaseException) as e:
            error("{filename} ocurrd ERROR".format(filename=dockerfile_name))
            error(e)

    def docker_composer(self, version="2",
                        image_list=[],
                        container_name_list=[],
                        ):
        pass


class xinetd(object):
    """docstring for xient_info"""

    def __init__(self, config_filename="config.json"):
        super(xinetd, self).__init__()
        with open(config_filename, "r") as file:
            config = json.loads(file.read())
        self.filename = config["filename"]
        self.project_path = config["project_path"]
        self.service_name = config["xinetd_info"]["service_name"]
        self.user = config["xinetd_info"]["user"]
        self.port = config["xinetd_info"]["port"]
        self.protocol = config["xinetd_info"]["protocol"]
        self.server_arg = config["xinetd_info"]["server_arg"]+self.filename
        if not os.path.exists(self.project_path):
            warn(self.project_path + "is not exists")
            warn("now automatic create path " + self.project_path)
            try:
                os.makedirs(self.project_path)
                succed("path is created")
            except Exception as e:
                error("path in config.json create failed!")
                error(e)

    def xinetd_file(self):
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

    def set_xinetd(self, xinetd_filename="xinetd.conf"):
        try:
            with open(os.path.join(self.project_path,xinetd_filename),"w") as file:
                file.write(xinetd().xinetd_file())
            succed("xinetd config file is generated")
        except (Exception, BaseException) as e:
            error("xinetd config file ocurrd ERROR")
            error(e)
