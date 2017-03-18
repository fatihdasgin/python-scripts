#!/usr/bin/python
__author__ = 'fatihdasgin'

import paramiko
import time
import sys

if __name__ == '__main__':

    def backup(ip,username,password,command,scppass):

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

	try:
        	# initiate SSH connection
        	ssh.connect(ip, username=username, password=password, look_for_keys=False, allow_agent=False)

	except:
		sys.exit("Connection Error")

        # Use invoke_shell to establish an 'interactive session'
        remoteConnection = ssh.invoke_shell()
        remoteConnection.send("\n")
        remoteConnection.send(command)

        # Wait 
        time.sleep(5)
        remoteConnection.send(scppass)
        remoteConnection.send("\n")

        # Wait 
        time.sleep(7)

        ssh.close()


    # Firewall Credentials
    username = 'fwuser'
    password = 'fwpass'

    # Time
    date = time.strftime("%Y-%m-%d_%H.%M")

    # Backup Server User Credentials
    scpuser = 'backupuser'
    scppass = "password"
    scppath = '/home/backupuser/'
    scphost = '192.168.x.x'

    # Firewall Ip Adresses
    fwIp = '192.168.x.x'

    # Backup Commands
    fwCommand = "scp export configuration from running-config.xml to " + scpuser + "@" + scphost + ":" + scppath + "paloAlto" + date + ".xml\n"

    backup(fwIp,username,password,fwCommand,scppass)
