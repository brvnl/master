import socket
import os.path

## STATIC VARIABLES
##----------------------------
AUTHENTICATION_FILES_PATH="../../authentication/"
host = "192.168.1.111"
port = 22004


## AUXILIARY ROUTINES
##----------------------------
def checkCredentials(usr, pwd):
    status = 0
    fname = AUTHENTICATION_FILES_PATH + usr
    if (os.path.isfile(fname)):
        file = open(fname, 'r')
        password = file.read()
        if (password == pwd):
            status =  0
        else:
            status =  3
        file.close()
    else:
        status =  1
    return status

def saveCredentials(usr, pwd):
    fname = AUTHENTICATION_FILES_PATH + usr
    file = open(fname, "w")
    file.write(pwd)
    file.close()
    return 0
    

## MAIN PROGRAM
##----------------------------
soc = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print 'INFO* Socket created.'

try:
    #Bind socket to local host and port
    soc.bind((host, port))
except socket.error as msg:
    print 'ERROR* Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    exit()

soc.listen(10)
print "INFO* Listening on host %s:%d." %(host, port)

while True:
    conn, addr = soc.accept()

    print ("INFO* Got connection from",addr)
    msg = conn.recv(1024)
    print (msg)
    usr, passwd = msg.split(";")
    usr = usr.split(":")[1]
    passwd = passwd.split(":")[1]

    retrn = checkCredentials(usr, passwd)
    if (retrn == 0):
        print("INFO* Authentication request from %s:%s allowed.") %(usr, passwd)
        sent = conn.send("Succeed\r\n")
    elif (retrn == 3):
        print("INFO* Authentication request from %s:%s rejected with wrong pass.") %(usr, passwd)
        sent = conn.send("Wrong Pass\r\n")
    else:
        print("INFO* Authentication request from %s:%s refused.") %(usr, passwd)
        sent = conn.send("Failed\r\n")

soc.close()
exit()