from setting import *
import elieen_help

if __name__ == '__main__':
    elieen_help.title()
    xinetd().set_xinetd()
    pwn_docker().set_dockerfile()
    pwn_docker().docker_composer()
