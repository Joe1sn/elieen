# ELIEEN：使用JSON配置CTF-Pwn中的Docker容器

之前大家都爱用的：pwn_deploy_chroot要修改版本或者libc很麻烦，要到处找配置修改，所以我想的就是让所有配置信息都在`config.json`中，这样就可以简化配置流程了

- **目前只能实现Dockerfile的单独pwn题部署**

将要部署的二进制文件放在该项目目录下

可以在`config.json`中修改

```json
{
    "project_path": "./pwn/",
    "filename":"babyheap",
    "work_path": "/home/pwn",
    "docker_info":
    {
        "os":
        {
            "release":"ubuntu",
            "version":"16.04"
        },
        "flag":"testtestest",
        "port":9999,
        "expose": "8000",
        "xinetd_config":"xinetd.conf"
    },
    "xinetd_info":{
        "service_name":"ctf",
        "user":"root",
        "port":9999,
        "protocol":"tcp",
        "server_arg":"--userspec=1000:1000 "
    }
}
```

- project_path：docker相关资源的文件夹，也是最后Dockerfile生成的文件夹
- filename：二进制文件名字
- work_path：docker中的文件夹
- docker_info：docker相关信息
  - os：docker操作系统相关，一般为发行版
    - release：操作系统发布版本
    - version：版本号
  - flag：原始flag字符串，在`setting.py`中会自动计算md5值
  - port：docker向外暴露的端口
  - expose：外界连接的端口
  - xinetd_config：xinetd的配置文件名字
- xinetd_info
  - service_name：xinetd服务名称
  - user：用户
  - port：xinetd作用的端口
  - protocol：通讯协议
  - server_arg：服务参数

运行

```shell
python3 initial.py
```

得到Dockerfile并运行

创建image

```shell
sudo docker build -f <project dir>/Dockerfile -t <image_name> .
```

创建container

```shell
sudo docker run -p <expose_port>:<docker_port> -d <image_name>
```



