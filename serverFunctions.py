"""
Timothy Queva
CS3130 Lab4
March 10, 2021

This file holds the necessary functions for the server-side operations of
dbcserver.py
"""

import socket

def recvall(sock,disableTOut = False):
    if disableTOut:
        sock.settimeout(None)
    else:
        sock.settimeout(2)
    
    data = b''
    while (data.decode('utf-8')).find(" \r\n*!*\r\n") == -1:
        try:
            more = sock.recv(1)
            data += more
        except socket.timeout:
            msg = "Request (" + data.decode('utf-8') + ") was not understood.\n\n"
            msg = msg.encode('utf-8')
            sock.sendall(msg)
            return ""
    data = data.decode('utf-8')
    data = data.strip(" \r\n*!*\r\n")
    return data

#checks database if record already exists and adds if not
def addDB(sc,db,recrd):
    nfound = True
    for key in db.keys():
        if key == recrd[0]:
            nfound = False
            break
    if nfound:
        db[recrd[0]] = ":".join(recrd[1:])
        reply =("\nRecord (" + recrd[0] + ":" + db[recrd[0]] + 
                ") added to database")
        reply = reply + " \r\n*!*\r\n"
        reply = reply.encode('utf-8')
        sc.sendall(reply)
    else:
        reply = "Sorry: A record already exists for this employee."
        reply = reply.encode('utf-8')
        sc.sendall(reply)

#searches for record. If found, confirm? deletion:abort
def rmDB(sc,db,recrd):
    found = False
    for key in db.keys():
        if recrd == key:
            reply = "verify: "
            reply = reply + "The following record will be deleted:\n"
            tmp = db[recrd].split(':')
            reply = reply + "Employee ID: " + recrd + "\n"
            reply = reply + "First name : " + tmp[0] + "\n"
            reply = reply + "Last name  : " + tmp[1] + "\n"
            reply = reply + "Department : " + tmp[2] + "\n"
            
            #this part confirms deletion
            while True:
                reply = reply + "PROCEED? (Y/n): "
                
                #send to client and ask if client is sure
                reply = reply + " \r\n*!*\r\n"
                reply = reply.encode('utf-8')
                sc.sendall(reply)
                
                response = recvall(sc,True).lower()
                response = response.strip()
                if response == "y":
                    del db[recrd]
                    reply = "\nRecord has been deleted. \r\n*!*\r\n"
                    reply = reply.encode('utf-8')
                    sc.sendall(reply)
                    break
                elif response == "n":
                    reply = "\nDeletion operation aborted. \r\n*!*\r\n"
                    reply = reply.encode('utf-8')
                    sc.sendall(reply)
                    break
                else:
                    reply = ("verify: Sorry, your response was not " +
                            "recognized.\n")
            found = True
            break
    if not found:
        reply = ("Sorry, requested employee could not be found "
                 "in the database.")
        reply = reply + " \r\n*!*\r\n"
        reply = reply.encode('utf-8')
        sc.sendall(reply)

#searches database for record and responds to client accordingly
def displayDB(sc,db,recrd):
    found = False
    for key in db.keys():
        if recrd == key:
            tmp = db[recrd].split(':')
            reply = "Employee ID: " + recrd + "\n"
            reply = reply + "First name : " + tmp[0] + "\n"
            reply = reply + "Last name  : " + tmp[1] + "\n"
            reply = reply + "Department : " + tmp[2] + "\n"
            found = True
            break
    if not found:
        reply = ("Sorry, requested employee could not be found "
                 "in the database.")
    
    reply = reply + " \r\n*!*\r\n"
    reply = reply.encode('utf-8')
    sc.sendall(reply)


def displayallDB(sc,db,recrd):
    reply ="Employee ID     First Name     Last Name     Department\n"
    for recrd in db:
        tmp = db[recrd].split(':')
        reply = reply + ('{:<16}'.format(recrd) +
                         '{:<15}'.format(tmp[0]) +
                         '{:<14}'.format(tmp[1]) + tmp[2] + "\n")
    reply = reply + " \r\n*!*\r\n"
    reply = reply.encode('utf-8')
    sc.sendall(reply)