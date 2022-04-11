"""
Timothy Queva
CS3130 Lab4
March 10, 2021

This program is a client-server program that allows access/manipulation
of server's database through formulated requests. Database is a .csv
file. This only works over the local area network due to NAT (Network
Address Translation)

Issues:
need to deal with ConnectionRefusedError in client

Optimization:
Server rewrites database every time there is a request from a client.
Need to fix this so it only writes changes or at least when there is
an actual change in the database
"""

import argparse, socket, time
import serverFunctions
import clientFunctions

def server(interface,port):
    #inports .csv file into in-program database
    db={}
    with open('Test.csv',encoding = "ISO-8859-1") as data:
            for elemnt in data:
                elemnt  = elemnt.strip()    #This by itself strips '\n' from line
                elemnt = elemnt.split(',')
                db[elemnt[0]] = ":".join(elemnt[1:])
    
    #This strips 'schema' from the csv file if it has one
    if 'ID' in db:
        del db['ID']
    
    #setups the server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((interface, port))
    sock.listen(1)
    print('Listening at', sock.getsockname())
    
    msg=''
    while True:
        sc, sockname = sock.accept()
        msg = serverFunctions.recvall(sc)
        
        msg = msg.split(' ')
        
        #services user request
        if msg[0].lower() == "add:":
            recrd = msg[1].split(',')
            serverFunctions.addDB(sc,db,recrd)
        elif msg[0].lower() == "rm:":
            recrd = msg[1]
            serverFunctions.rmDB(sc,db,recrd)
        elif msg[0].lower() == "display:":
            recrd = msg[1]
            serverFunctions.displayDB(sc,db,recrd)
        elif msg[0].lower() == "displayall":
            recrd = msg[0]
            serverFunctions.displayallDB(sc,db,recrd)
        else:
            reply = "Sorry. Your request was not understood."
            reply = reply + " \r\n*!*\r\n"
            reply = reply.encode('utf-8')
            sc.sendall(reply)
        
        sc.close()
        
        #Update database: uploads internal database back into csv file
        with open('Test.csv','w',encoding = "ISO-8859-1") as data:
            data.write("ID,FNAME,LNAME,DEPT\n")
            for elemnt in db:
                #Writes the key
                data.write(str(elemnt) + ",")
                
                #transforms stored attributes back into csv file storage format
                tmp = str(db[elemnt])
                tmp = tmp.split(":")
                tmp = ",".join(tmp)
                data.write(tmp)
                data.write('\n')
        

def client(host,port):
    #client interface
    opt = 0
    print("Note: if a back/exit option is unavailable, " +
          "you can exit any submenu by typing: exit\n")
    print("Welcome to Employee FMS\n")
    while opt != 5:
        print("Please select one of the following options:")
        print("    1) Add new employee")
        print("    2) Search for an employee")
        print("    3) Remove an employee from FMS")
        print("    4) Display entire employee FMS")
        print("    5) Exit")
        print()
        
        #This dals with user input and associated exception handling
        try:
            opt = int(input("Choice #? : "))
            if(opt < 1 or opt > 5):
                print("\nERROR: Please enter a valid option\n")
                time.sleep(2)
                continue
        except ValueError:
            print("\nERROR: Please enter a valid number")
            time.sleep(2)
            continue
    
        #This will deals with user selected options
        if opt == 1:
            clientFunctions.add(host,port)
        elif opt == 2:
            clientFunctions.display(host,port)
        elif opt == 3:
            clientFunctions.rm(host,port)
        elif opt == 4:
            clientFunctions.displayall(host,port)

if __name__ == '__main__':
    choices = {'client': client, 'server': server}
    parser = argparse.ArgumentParser(description='Computer Science chat'+
                                     'program')
    parser.add_argument('role', choices=choices, help='which role to take')
    parser.add_argument('host', help='interface the server listens at;'
                        ' host the client sends to')
    parser.add_argument('-p', metavar='PORT', type=int, default=1123,
                        help='UDP port (default 1123)')
    args = parser.parse_args()
    function = choices[args.role]
    function(args.host, args.p)