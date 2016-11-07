import socket
import os.path
import logging
import re

## STATIC VARIABLES
##----------------------------
logging.basicConfig(format='%(asctime)s %(levelname)s* %(message)s', level=logging.INFO)
AUTHENTICATION_FILES_PATH="../../authentication/"
KEYWORDS_FILES_PATH="../../keywords/"
#host = socket.gethostbyname(socket.gethostname())
stmp = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
stmp.connect(("gmail.com",80))
host = stmp.getsockname()[0]
stmp.close
port = 22004


## AUXILIARY ROUTINES
##----------------------------
def checkCredentials(usr, pwd):
    status = 0
    fname = AUTHENTICATION_FILES_PATH + usr
    if (os.path.isfile(fname)):
        file = open(fname, 'r')
        password = file.read()
        password = password.rstrip("\r\n")
        password = password.rstrip("\n")
        password = password.rstrip("^\s")
        password = password.rstrip("\s$")
        if (password == pwd):
            status =  0
        else:
            status =  3
        file.close()
    else:
        status =  1
    return status

def saveCredentials(usr, pwd, keywrds):
    # Saves a file with the password
    fname = AUTHENTICATION_FILES_PATH + usr
    file = open(fname, "w")
    file.write(pwd)
    file.close()

    # Saves the keywords on a different file
    fname = KEYWORDS_FILES_PATH + usr
    file = open(fname, "w")
    file.write(keywrds)
    file.close()

    return 0


## MAIN PROGRAM
##----------------------------
logging.info('Starting authentication service...')
soc = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
logging.info('Socket created.')

try:
    #Bind socket to local host and port
    soc.bind((host, port))
except socket.error as msg:
    logging.error('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
    exit()

soc.listen(10)
logging.info("Listening on host %s:%d." %(host, port))

while True:
    conn, addr = soc.accept()

    logging.info("Got connection from %s." %(str(addr)))
    msg = conn.recv(1024)
    
    # Remove first bytes added by Java
    msg = re.sub('^[^@]*@', '@', msg)

    logging.info("Request:" + msg)
    parameters = msg.split(";")

    if (len(parameters) != 4):
        continue

    operation, usr, passwd, keywrds = parameters
    usr = usr.split(":")[1]
    passwd = passwd.split(":")[1]
    operation = '@' + operation.split('@')[1]

    if (operation == "@authenticate"):
        retrn = checkCredentials(usr, passwd)
        if (retrn == 0):
            logging.info("Authentication request from %s:%s allowed." %(usr, passwd))
            sent = conn.send("Succeed\r\n")
        elif (retrn == 3):
            logging.info("Authentication request from %s:%s rejected with wrong pass." %(usr, passwd))
            sent = conn.send("Wrong Pass\r\n")
        else:
            logging.info("Authentication request from %s:%s refused." %(usr, passwd))
            sent = conn.send("Failed\r\n")

    elif (operation == "@register"):
        retrn = checkCredentials(usr, passwd)

        if ((retrn == 0) or (retrn == 3)):
            sent = conn.send("Already exists\r\n")
            logging.info("Registration refused for %s:%s. User already exists." %(usr, passwd))
        else:
            saveCredentials(usr, passwd, keywrds)
            sent = conn.send("Succeed\r\n")
            logging.info("Registration succeed for %s:%s." %(usr, passwd))

    conn.close()

soc.close()

exit()
