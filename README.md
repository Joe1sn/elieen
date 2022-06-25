# ELIEEN：使用JSON配置CTF-Pwn中的Docker容器

![](https://img.shields.io/badge/joe1sn-ELIEEN-green)![](https://img.shields.io/badge/python-3.7-yellow)

> 该项目构建的docker能够直接在ctfd-whale中启用

之前大家都爱用的：pwn_deploy_chroot要修改版本或者libc很麻烦，要到处找配置修改，所以我想的就是让所有配置信息都在`config.json`中，这样就可以简化配置流程了

将要部署的二进制文件放在该项目目录下

可以在`config.json`中修改

```json
{
  "pwn_dockers": [
    {
      "project_path": "./pwn1/",
      "filename": "babyheap",
      "image_name": "babyheap",
      "docker_username": "pwn1",
      "port": 9999,
      "docker_info": {
        "os": {
          "release": "ubuntu",
          "version": "16.04"
        },
        "flag": "test1",
        "expose": 8000,
        "xinetd_config": "xinetd.conf"
      },
      "xinetd_info": {
        "service_name": "ctf",
        "user": "root",
        "protocol": "tcp",
        "server_arg": "--userspec=1000:1000 "
      }
    },
    {
      "project_path": "./pwn2/",
      "filename": "babyheap",
      "docker_username": "pwn2",
      "image_name": "babyheap2",
      "port": 8000,
      "docker_info": {
        "os": {
          "release": "ubuntu",
          "version": "18.04"
        },
        "flag": "test2",
        "expose": 8001,
        "xinetd_config": "xinetd.conf"
      },
      "xinetd_info": {
        "service_name": "ctf",
        "user": "root",
        "protocol": "tcp",
        "server_arg": "--userspec=1000:1000 "
      }
    }
  ]
}
```

除了 **加粗的** 大多数使用默认参数就行

- pwn_dockers：pwn类配置
- **project_path**：docker相关资源的文件夹，也是最后Dockerfile生成的文件夹
- **filename**：二进制文件名字
- docker_username：docker中运行程序的用户名
- **port**：docker向外暴露的内部的端口
- **docker_info**：docker相关信息
  - os：docker操作系统相关，一般为发行版
    - release：操作系统发布版本
    - version：版本号
  - **flag**：原始flag字符串，在`setting.py`中会自动计算md5值
  - **expose**：外界连接的端口
  - xinetd_config：xinetd的配置文件名字
- xinetd_info
  - service_name：xinetd服务名称
  - user：用户
  - port：xinetd作用的端口
  - protocol：通讯协议
  - server_arg：服务参数

一般配置过程变量使用json中的参数 `-p expose:port`

运行

```shell
python3 initial.py
```

得到`docker-compose.yml`

```shell
sudo docker-compose build
```

然后使用`sudo docker images`就能看到构建好的docker了