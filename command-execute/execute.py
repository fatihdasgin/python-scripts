#!/usr/bin/python
import paramiko
import time

username=''
password=''
server_list='servers'
command_file='commands'


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


f  = open(server_list,"r")
fc = open(command_file,"r")

def executeCommand(command):
	cmd = command
	stdin, stdout, ssh_stderr = ssh.exec_command(cmd)
	out = stdout.read()
	err = ssh_stderr.read()
	print bcolors.OKBLUE + cmd.rstrip("\n") + bcolors.ENDC
	if out: print bcolors.OKGREEN + out.rstrip("\n") + bcolors.ENDC
	if err: print bcolors.FAIL + err.rstrip("\n") + bcolors.ENDC

for host in f.readlines():
	hostname = host.strip("\n").split("|")[0]
	ip = host.strip("\n").split("|")[1]


	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

	try:
		ssh.connect(ip, username=username, password=password, look_for_keys=False, allow_agent=False, timeout=5)
		print bcolors.OKGREEN + "==========================================================================" + bcolors.ENDC
		print bcolors.OKGREEN +"[+]\tConnected to \t%s\t\t%s"%(hostname,ip)+ bcolors.ENDC

		fc.seek(0)
		for command in fc.readlines():
			executeCommand(command)

		ssh.close()

	except:
		print bcolors.FAIL + "==========================================================================" + bcolors.ENDC
		print bcolors.FAIL +"[-]\tAccess Denied\t%s\t\t%s"%(hostname,ip) + bcolors.ENDC


	time.sleep(2)

f.close()
fc.close()
