from rich import print as rprint
from datetime import datetime

def title():
	print(
'''
███████╗██╗     ██╗███████╗███████╗███╗   ██╗
██╔════╝██║     ██║██╔════╝██╔════╝████╗  ██║
█████╗  ██║     ██║█████╗  █████╗  ██╔██╗ ██║
██╔══╝  ██║     ██║██╔══╝  ██╔══╝  ██║╚██╗██║
███████╗███████╗██║███████╗███████╗██║ ╚████║
╚══════╝╚══════╝╚═╝╚══════╝╚══════╝╚═╝  ╚═══╝
'''
	)

def error(*body):
    print("\033[0;31;40m│\033[0m",end="")
    msg = ""
    for i in body:
        msg += str(i) + " "
    rprint("[[bold green]" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "[/bold green]] [bold red]ELIEEN[/bold red] [[bold red]error[/bold red]] > [bold yellow]" + msg + "[/bold yellow]")

def success(*body):
    print("\033[0;31;40m│\033[0m",end="")
    msg = ""
    for i in body:
        msg += str(i) + " "
    rprint("[[bold green]" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "[/bold green]] [bold red]ELIEEN[/bold red] [[bold green]success[/bold green]] > " + msg)

def info(*body):
    print("\033[0;31;40m│\033[0m",end="")
    msg = ""
    for i in body:
        msg += str(i) + " "    
    rprint("[[bold green]" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "[/bold green]] [bold red]ELIEEN[/bold red] [[bold blue]info[/bold blue]] > " + msg)

def warn(*body):
    print("\033[0;31;40m│\033[0m",end="")
    msg = ""
    for i in body:
        msg += str(i) + " "    
    rprint("[[bold green]" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "[/bold green]] [bold red]ELIEEN[/bold red] [[bold yellow]warn[/bold yellow]] > " + msg)