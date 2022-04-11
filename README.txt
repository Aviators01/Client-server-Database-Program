Timothy Queva
CS3130 Lab4
March 10, 2021

Description: This program is a client-server program that utilizes TCP protocol for serving database requests
made by a client. Both server and client operation are included within the same file.

Limitations:
1. Only works over the local area network due to NAT (Network Address Translation) preventing
communication beyond a subnet.
2. Server doesn't check body message syntax (no time to implement)-only header and end of message termination
string. Therefore, results unknown if substitute client used to send incorrect syntatic body message.
3. Some coding changes needed for console output text and formatting, if different .csv file is used. Especially
if different .csv file has different schema or number of attributes.

Security issues:
1. communication is unencrypted.
2. Database not secured.

Instructions:
	1. Navigate to the correct folder:
	2. Start the server by typing: python3 dbcserver.py server 127.0.0.1
	3. (In a different window) start client by typing: python3 dbcserver.py client 127.0.0.1

Additional tips:
-for help, type: python3 dbcserver.py -h
-127.0.0.1 is just the loopback address. It can be replaced with any valid-according-to-subnet-rules ip address
-To stop the client, one can just type: exit
-to stop the server, press ctrl + c