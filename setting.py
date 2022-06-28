import json
from hashlib import md5
from sys import float_repr_style
from elieen_help import *
import os
import shutil


def read_config(config_filename="config.json"):
    try:
        with open(config_filename, "r") as file:
            return json.loads(file.read())
    except Exception as e:
        error("open config file ERROR")
        error(e)


class pwn_docker(object):
    """docstring for docker_info"""

    def __init__(self):
        super(pwn_docker, self).__init__()
        self.docker_list = []
        self.compose_header = "version: '2'\n" \
                              "services:\n"
        config = read_config()

        for docker in config["pwn_dockers"]:
            self.docker_list.append(docker)

        for docker in self.docker_list:
            project_path = docker["project_path"]
            if not os.path.exists(project_path):
                warn(project_path + "is not exists")
                warn("now automatic create path " + project_path)
                try:
                    os.makedirs(project_path)
                    succed("path is created")
                except Exception as e:
                    error("path in config.json create failed!")
                    error(e)

    def dockerfile(self, tmp_docker, flag_filename="flag",
                   startup_script_name="service.sh"):
            str = "FROM {os}\n"
            str += "RUN sed -i 's/archive.ubuntu.com/mirrors.aliyun.com/g' /etc/apt/sources.list && apt update && apt-get install -y lib32z1 xinetd && rm -rf /var/lib/apt/lists/ && rm -rf /root/.cache && apt-get autoclean && rm -rf /tmp/* /var/lib/apt/* /var/cache/* /var/log/*\n"
            str += "COPY {xinetd_config_filename} /etc/xinetd.d/{filename}\n"
            str += "COPY {startup_script_name} /{startup_script_name}\n"
            str += "RUN chmod +x ./{startup_script_name}\n"
            str += "#add user and flag\n"
            str += "RUN useradd -m {username} && echo '{flag}' > {work_dir}/{flag_filename}\n"
            str += "#copy binary file\n"
            str += "COPY {filename} {work_dir}/{filename}\n"
            str += "COPY ./catflag {work_dir}/bin/sh\n"
            str += "#set execution\n"
            str += "RUN chown -R root:{username} {work_dir} && chmod -R 750 {work_dir} && chmod 740 {work_dir}/{flag_filename}\n"
            str += "#copy lib,/bin\n"
            if int(tmp_docker["docker_info"]["os"]["version"][:2]) < 19:
                str += "RUN cp -R /lib* {work_dir} && cp -R /usr/lib* {work_dir} && mkdir {work_dir}/dev && mknod {work_dir}/dev/null c 1 3 && mknod {work_dir}/dev/zero c 1 5 && mknod {work_dir}/dev/random c 1 8 && mknod {work_dir}/dev/urandom c 1 9 && chmod 666 {work_dir}/dev/* && cp /bin/sh {work_dir}/bin && cp /bin/ls {work_dir}/bin && cp /bin/cat {work_dir}/bin\n"
            else:
                str += "RUN cp -R /lib* {work_dir} && mkdir {work_dir}/dev && mknod {work_dir}/dev/null c 1 3 && mknod {work_dir}/dev/zero c 1 5 && mknod {work_dir}/dev/random c 1 8 && mknod {work_dir}/dev/urandom c 1 9 && chmod 666 {work_dir}/dev/* && cp /bin/sh {work_dir}/bin && cp /bin/ls {work_dir}/bin && cp /bin/cat {work_dir}/bin\n"
            str += "CMD './{startup_script_name}'\n"
            str=str.format(
                os=tmp_docker["docker_info"]["os"]["release"] + ':' + tmp_docker["docker_info"]["os"]["version"],
                username=tmp_docker["docker_username"],
                xinetd_config_filename=tmp_docker["docker_info"]["xinetd_config"],
                work_dir="/home/" + tmp_docker["docker_username"],
                flag='flag{' + md5(bytes(tmp_docker["docker_info"]["flag"], encoding="utf-8")).hexdigest() + '}',
                filename=tmp_docker["filename"],
                flag_filename=flag_filename,
                startup_script_name=startup_script_name,
                project_path=tmp_docker["project_path"]
            )
            return str

    def set_dockerfile(self, dockerfile_name="Dockerfile"):
        tips("--------GENERATE DOCKERFILE--------")
        for dockerfile in self.docker_list:
            try:
                path = dockerfile["project_path"]
                with open(os.path.join(path, dockerfile_name), "w", encoding="utf-8") as file:
                    file.write(self.dockerfile(dockerfile))
                succed(
                    "{filename} is generated".format(filename=os.path.join(path, dockerfile_name)))
                tips("now copy the basic files")
                
                shutil.copy("./basic/service.sh", path)
                shutil.copy("./basic/catflag", path)
                shutil.copy(dockerfile["filename"], path)
                with open(path+"service.sh","w",encoding='utf-8') as conf:
                    str = '''echo $FLAG > /home/{user}/flag
chown root:{user} /home/{user}/flag
chmod 640 /home/{user}/flag
export FLAG=not_flag
FLAG=not_flag
/etc/init.d/xinetd start;
sleep infinity;'''.format(user=dockerfile["docker_username"])
                    conf.write(str)

                tips("using command below to build and run docker")
                tips("  sudo docker build -f {project_dir}Dockerfile -t {image_name} .".format(
                    project_dir=dockerfile["project_path"],
                    image_name=dockerfile["image_name"]))

                tips("  sudo docker run -p {expose_port}:{docker_port} -d {image_name}".format(
                    docker_port=dockerfile["port"],
                    image_name=dockerfile["image_name"],
                    expose_port=dockerfile["docker_info"]["expose"]))
            except (Exception, BaseException) as e:
                error("{filename} ocurrd ERROR".format(filename=os.path.join(path, dockerfile_name)))
                error(e)
                exit()
        print()

    def docker_composer(self):
        tips("--------GENERATE DOCKER_COMPOSE--------")
        for dockerfile in self.docker_list:
            try:
                self.compose_header += "    " + dockerfile["image_name"] + ":\n"
                self.compose_header += "        image: " + dockerfile["image_name"] + "\n"
                self.compose_header += "        build: " + dockerfile["project_path"] + "\n"
                self.compose_header += "        container_name: " + dockerfile["image_name"] + "\n"
                self.compose_header += "        ports:\n"
                self.compose_header += "            - " + str(dockerfile["docker_info"]["expose"]) + ":" + str(
                    dockerfile["port"]) + "\n"
            except Exception as e:
                error("docker compose file ERROR")
                error(e)
        try:
            with open("docker-compose.yml", "w") as file:
                file.write(self.compose_header)
            succed("docker-compose.yml generate success")
            tips("use command below to build and run docker")
            tips(" sudo docker-compose up --build -d")
            tips("use command below to build dockers")
            tips(" sudo docker-compose build")

        except Exception as e:
            error("docker-compose.yml generate failed")
            error(e)
        print()


class xinetd(object):
    """docstring for xient_info"""

    def __init__(self, ):
        super(xinetd, self).__init__()
        self.xinetd_list = []
        config = read_config()

        for dockerfile in config["pwn_dockers"]:
            self.xinetd_list.append(dockerfile)

        for xinetd_file in self.xinetd_list:
            project_path = xinetd_file["project_path"]
            if not os.path.exists(project_path):
                warn(project_path + "is not exists")
                warn("now automatic create path " + project_path)
                try:
                    os.makedirs(project_path)
                    succed("path is created")
                except Exception as e:
                    error("path in config.json create failed!")
                    error(e)

    def xinetd_file(self, tmp_xinetd):
        xinetd_info = tmp_xinetd["xinetd_info"]
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
                name=xinetd_info["service_name"],
                protocol=xinetd_info["protocol"],
                user=xinetd_info["user"],
                port=tmp_xinetd["port"],
                server_arg=xinetd_info["server_arg"] + " " + "/home/" + tmp_xinetd["docker_username"] + " ./" +
                           tmp_xinetd["filename"]
            )

    def set_xinetd(self, xinetd_filename="xinetd.conf"):
        # tips("--------GENERATE XINETD FILE--------")
        for config in self.xinetd_list:
            try:
                with open(os.path.join(config["project_path"], xinetd_filename), "w") as file:
                    file.write(xinetd().xinetd_file(config))
                succed(config["project_path"] + " xinetd config file is generated")
            except (Exception, BaseException) as e:
                error(config["project_path"] + " xinetd config file ocurrd ERROR")
                error(e)
        print()