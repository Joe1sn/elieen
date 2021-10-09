from setting import *
from elieen_help import *


def set_xient(xient_filename="xient.conf"):
	try:
		with open(xient_filename,"w") as file:
			file.write(xient().xient_file())
		succed("xient config file is generated")
	except:
		error("xient config file ocurrd ERROR")


def set_dockerfile(dockerfile_name = "Dockerfile"):
	try:
		with open(dockerfile_name,"w",encoding="utf-8") as file:
			file.write(docker().dockerfile())
		succed("{filename} is generated".format(filename=dockerfile_name))
	except (Exception,BaseException) as e:
		error("{filename} ocurrd ERROR".format(filename=dockerfile_name))
		error(e)

def set_docker_composer():
	pass


if __name__ == '__main__':
	set_xient()
	set_dockerfile()