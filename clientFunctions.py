'''
Timothy Queva
CS3130 Lab4
March 10, 2021

This file holds the necessary functions for the client-side operations of
dbcserver.py
'''

import time, socket

#sends message and adds end of message sequence of characters
def transmit(sock,msg):
    msg = msg + " \r\n*!*\r\n"
    msg = msg.encode('utf-8')
    sock.sendall(msg)

#receives messages from server
def receive(sock):
    sock.settimeout(2)
    data = b''
    while (data.decode('utf-8',errors='ignore')).find(" \r\n*!*\r\n") == -1:
        try:
            more = sock.recv(1)
            data += more
        except socket.timeout:
            print("Incomplete response received.")
            print("Here is what we've received so far:")
            data = data.decode('utf-8')
            return data
    data = data.decode('utf-8')
    data = data.strip(" \r\n*!*\r\n")
    return data

#checks for correct input and sends add request to server to add a recrd
def add(host,port):
    again = True
    while again:
        recrd = input("Please enter below employee id, first name, last name, " +
                      "and department in this order separated by one space: ")
        
        #allows exiting if one does not wish to add to database
        if str(recrd) == "exit":
            print("Exiting to main menu...\n")
            time.sleep(1)
            break
        
        #processes input
        recrd = recrd.strip()
        recrd = recrd.split(' ')
        
        #psuedo-exception handling for incorrect inputs
        if len(recrd) < 4 or len(recrd) > 4:
            print("Incorrect input: Please enter all details as specified.")
            print() #for ubuntu
            continue
        try:
            int(recrd[0])
        except:
             print("Employee ID is incorrect. Please enter numbers only.")
             continue
        #Note: non-alphabetic names and numeric departments accepted as valid
        #inputs.
        
        #Sends request to server and waits for reply
        msg = ",".join(recrd)
        msg = "add: " + msg
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        transmit(sock,msg)
        print(receive(sock))
        print()
        sock.close()
        
        #Control for loop/exit to main menu
        while True:
            again = input("Enter another record? (Y/n): ")
            again = again.lower()
            if again == "n":
                print("Exiting to main menu...\n")
                time.sleep(1)
                again = False
                break
            elif again == "y":
                again = True
                break
            else:
                print("Sorry, your response was not recognized.")
                print()

#Checks for correct input and sends display request to server to add a recrd
def display(host,port):
    again = True
    while again:
        recrd = input("Which employee do you wish to find? ID #: ")
        
        #allows exiting if one does not wish to remove record from database
        if recrd == "exit":
            print("Exiting to main menu...\n")
            time.sleep(1)
            break
        
        #checks input to ensure only numbers entered
        if not recrd.isnumeric():
            print("Please enter employee ID numbers only")
            continue
        
        #Sends request to server and waits for reply
        msg = "display: " + recrd
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        transmit(sock,msg)
        print(receive(sock))
        print()
        sock.close()
        
        #Control for loop/exit to main menu
        while True:
            again = input("Search another employee? (Y/n): ")
            again = again.lower()
            if again == "n":
                print("Exiting to main menu...\n")
                print() #for ubuntu
                time.sleep(1)
                again = False
                break
            elif again == "y":
                print() #for ubuntu
                again = True
                break
            else:
                print("Sorry, your response was not recognized.")
                print() #for ubuntu

#Checks for correct input and sends remove request to server to add a recrd
#also sends verification of delete request to server
def rm(host,port):
    again = True
    while again:
        try:
            recrd = input("Which employee do you wish to remove? ID #: ")
            
            #allows exiting if one does not wish to remove record from database
            if recrd == "exit":
                print("Exiting to main menu...\n")
                time.sleep(1)
                break
            
            #checks input to make sure it is an integer
            recrd = int(recrd)
            recrd = str(recrd)
            
            #Sends request to server and waits for reply
            recrd = recrd.strip()
            msg = "rm: " + recrd
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((host, port))
            transmit(sock,msg)
            
            #captures response from server and replies to verification request
            s_response = receive(sock)
            while s_response[:8] == "verify: ":
                print(s_response[8:], end = '')
                msg = input()
                transmit(sock,msg)
                s_response = receive(sock)
            
            #prints servers confirmation of serviced request
            print(s_response)
            print()
            sock.close()
        except ValueError:
            print("Please enter employee ID numbers only")
            print()
            continue
        
        #Control for loop/exit to main menu
        while True:
            again = input("Delete another record? (Y/n): ")
            again = again.lower()
            if again == "n" or again == "exit":
                print("Exiting to main menu...\n")
                time.sleep(1)
                again = False
                break
            elif again == "y":
                again = True
                break
            else:
                print("Sorry, your response was not recognized.")

#Sends displayall request to server to add a recrd
def displayall(host,port):
    msg = "displayall"
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    transmit(sock,msg)
    print(receive(sock))
    print()
    sock.close()