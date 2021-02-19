'''
@author: Karun Kanda (kk951)
@author: Shila Basu (sb1825)
'''

import time
import random
import socket, sys

'''
query_hostname_table takes in no arguments and returns a dictionary containing all the hostnames to be
queried held in PROJI-HNS.txt.

The purpose of this method is to store everything in a dictionary so that when it comes to requesting information
it can pop one element at a time to check with either the RS server or the TS server to check if either server
contains the information that its looking for.
'''
def query_hostname_table():
    queried_hostname = None
    file = open("PROJI-HNS.txt", "r")
    hostnames_queries = []
    for host in file:
        hostnames_queries.append(host.replace('\r\n', ''))
    file.close()
    return hostnames_queries

'''
client takes in no arguments and does not return anything because this is where the main logic of the program
is going to be held. Upon start it will create a dictionary containing all the hostnames that need to be queried.
Then looping through all the names it will pop one at a time and send it to the RS server and see where its information lies.

The purpose of this method is to host the knowledge of the client application. One hostname at a time will be popped from the 
dictionary of hostnames and first sent to the RS server. If the RS server found the requested information it will provide the 
client a A flag and all the client will do is stop and print what it recieved. Otherwise it will take the hostname found before the NS flag 
and ask the TS server for its requested information. It will do the same process once it asks the TS server and if the TS server 
did not find its information it will output:
    Hostname - Error:Host not found
Then close the client after all the hostnames have been popped.
'''
def client():
    hostnames = query_hostname_table()
    while len(hostnames) != 0:
        # initial setup for the client side
        try:
            cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as err:
            print('socket open error: {} \n'.format(err))
            exit()

        port = int(sys.argv[2])
        localhost_addr = socket.gethostbyname(sys.argv[1])

        server_binding = (localhost_addr, port)
        cs.connect(server_binding)

        # first task of client is to query the table and send the queried hostname to rs server
        queried_hostname = hostnames.pop(0)
        cs.send(queried_hostname.encode('utf-8'))

        # recieve the queried string from the client
        server_string = cs.recv(1024)

        # tokenize the string to check the flag portion which should be at token[2]
        tokens = server_string.split()
        if tokens[2] == 'A':
            print(server_string)
            f = open("RESOLVED.txt", "a")
            f.write(server_string + "\n")
        elif tokens[2] == 'NS':
            # if the second token isn't an A and if its an "NS" then the client should go to "ask" the TS server
            try:
                cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            except socket.error as err:
                print('socket open error: {} \n'.format(err))

            port = int(sys.argv[3])
            if tokens[0] == "localhost":
                localhost_addr = socket.gethostbyname(socket.gethostname())
            else:
                localhost_addr = socket.gethostbyname(tokens[0])

            server_binding = (localhost_addr, port)
            cs.connect(server_binding)

            cs.send(queried_hostname.encode('utf-8'))

            server_string = cs.recv(1024)

            tokens = server_string.split()
            if tokens[2] == 'A':
                print(server_string)
                f = open("RESOLVED.txt", "a")
                f.write(server_string + "\n")
            else:
                print(server_string)
                f = open("RESOLVED.txt", "a")
                f.write(server_string + "\n")

    cs.close()
    exit()

'''
This is the main method that will expect four arguments from the user to start the application
otherwise it will return an error.
'''
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Incorrect Usage: python client.py <hostname> <RS server port number> <TS server port number>")
        sys.exit(1)

    f = open("RESOLVED.txt","w")
    f.close()
    client()
