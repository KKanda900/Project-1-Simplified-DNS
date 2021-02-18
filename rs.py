'''
@author: Karun Kanda (kk951)
@author: Shila Basu (sb1825)
'''

import time, random, socket, sys

class RSTable:
    rsdns_table = []
    localhost_line = None

    def __init__(self):
        rsdns_table = []
        localhost_line = None
 
'''
create_rsdns_table does not take any arguments and returns a dictionary of the DNS table found 
in PROJI-DNSRS.txt.

The purpose of this method is for when the client requests a corresponding IP address for the given Hostname 
that the RS server can iterate this table and give the client the corresponding column in the table that
matches with the domain name given or the TS server that might have information on the domain name. 
'''
def create_rsdns_table():
    table = RSTable()
    index = 0

    file = open("PROJI-DNSRS.txt", "r")
    for info in file:
        tokens = info.split()
        table.rsdns_table.append((tokens[0], tokens[1], tokens[2]))
        if tokens[2] == 'NS':
            table.localhost_line = tokens[0] + " " + tokens[1] + " " + tokens[2]
        index+=1
    
    return table

'''
check_hostname_table takes in two arguments, the queried hostname from the client and the RS server table
and returns a column from the table or the last column according to if the hostname is found in the table.

The purpose of this method is to check if given hostname is found in the RS server and if it is not found in 
this table give it the corresponding TS server that might have information on it. It iterates the table and if 
a match is found it returns:
    Hostname IP Address A
However if a match isn't found it returns the last column of the table which is:
    localhost - NS
Where the A should tell the client just to output the results and NS should tell the client that the RS server 
didn't have the information that it needed so pass the domain name to the corresponding TS server.
'''
def check_hostname_table(queried_hostname, table):
    for i in range(0, len(table.rsdns_table)):
        if table.rsdns_table[i][0].lower() == queried_hostname.lower():
            return '{} {} {}'.format(table.rsdns_table[i][0], table.rsdns_table[i][1], table.rsdns_table[i][2])
    
    return table.localhost_line

'''
rs_server takes in no arguments and doesn't return anything because this is where the RS server is going to 
start from. Upon start the RS server will create its respective table which will be used when the client connects
and provides the server a hostname to start with.

The purpose of this method is to hold the main logic behind the RS server upon connection. First creating its RS
table. Then waiting for a response from the client to give it a match or a given TS server to connect to next. 
The socket used to create the RS server will contain a reusable address so that the client can query everything in
its table.
'''
def rs_server():
    # initial setup for the server side
    while True:
        try:
            ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ss.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            print("[S]: Server socket created")
        except socket.error as err:
            print('socket open error: {}\n'.format(err))
            exit()

        server_binding = ('', int(sys.argv[1]))
        ss.bind(server_binding)
        ss.listen(1)
        host = socket.gethostname()
        localhost_ip = (socket.gethostbyname(host))
        csockid, addr = ss.accept()
        print ("[S]: Got a connection request from a client at {}".format(addr)) # check if we recieved a connection or not

        # create the rs dns table for lookup
        table = create_rsdns_table()

        # for testing, let's see what we get back
        queried_hostname = csockid.recv(1024)

        # next part is the table lookup to give the client its respective string
        queried_string = check_hostname_table(queried_hostname, table)
        csockid.send(queried_string.encode('utf-8'))

    ss.close()
    exit()


'''
This is the main method where the program will start. rs.py is expecting two arguments one being 
python rs.py and the port number so it can start successfully.
'''
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Incorrect Usage: python rs.py <port number>")
        sys.exit(1)
    rs_server()
    
