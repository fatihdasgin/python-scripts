#!/usr/bin/python
__author__ = 'fatihdasgin'

import paramiko
import time
import sys

if __name__ == '__main__':

    def nsBackup(ip,username,password,command):

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

        # Execute backup command
        remoteConnection.send(command)
        remoteConnection.send("\n")

        # Wait 
        time.sleep(60)

        ssh.close()


    def getConfigToServer(ip,username,password,localPath,remotePath,itemName):

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            # initiate SSH connection
            ssh.connect(ip, username=username, password=password, look_for_keys=False, allow_agent=False)

        except:
            sys.exit("Connection Error.")

        # Create sftp object
        sftp = ssh.open_sftp()

        remoteFile = remotePath + itemName
        localFile = localPath + itemName

        # fetch remote file
        sftp.get(remoteFile, localFile)

        time.sleep(30)

        sftp.close()
        ssh.close()

    def deleteRemoteBackupFile(ip,username,password,command):

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

        # Open shell
        remoteConnection.send("shell")
        remoteConnection.send("\n")

        time.sleep(5)

        # Remote old backup file
        remoteConnection.send(command)
        remoteConnection.send("\n")

        time.sleep(5)


    # Time
    date = time.strftime("%Y-%m-%d_")

    # NS Config Backup Command
    nsBackupCommand = "create system backup " + date + "netscaler-backup -level full"

    # NS Credentials
    nsIp = ''
    nsUser = ''
    nsPass = ''

    # Files
    itemName = date + "netscaler-backup.tgz"
    remotePath = "/var/ns_sys_backup/"
    localPath = "/home/fwbackup/"

    # NS Remove File Command
    removeBackupCommand = "rm " + remotePath + itemName

    # back up config file on netscaler
    nsBackup(nsIp,nsUser,nsPass,nsBackupCommand)

    # get backup config to local server
    getConfigToServer(nsIp,nsUser,nsPass,localPath,remotePath,itemName)

    # remove the newly created backup file from netscaler
    deleteRemoteBackupFile(nsIp,nsUser,nsPass,removeBackupCommand)
