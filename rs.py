import time, random, socket

class RS:
    hostname = None
    ip = None 
    flag = None

    def __init__(self, hostname, ip, flag):
        self.hostname = hostname
        self.ip = self.ip
        self.flag = flag

# creates a 2d array to represent a table type of lookup
def table_to_string(table):
    for i in range(0,len(table)):
        print(table[i].hostname, table[i].ip, table[i].flag)  

# create the rs dns table for the given file
def create_rsdns_table():
    rsdns_table = [None]*6
    index = 0

    file = open("PROJI-DNSRS.txt", "r")
    for info in file:
        tokens = info.split()
        if tokens[0] == '-':
            tokens[0] = 'None'
        elif tokens[1] == '-':
            tokens[1] = 'None'
        elif tokens[2] == '-':
            tokens[2] = 'None'
        rsdns_table[index] = RS(tokens[0], tokens[1], tokens[2])
        index+=1
    
    return rsdns_table

def check_hostname_table(queried_hostname, table):
    for i in range(0, len(table)):
        if table[i].hostname == queried_hostname:
            return '{} {} {}'.format(table[i].hostname, table[i].ip, table[i].flag)
    
    return 'Information not found'


def rs_server():
    # initial setup for the server side
    try:
        ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[S]: Server socket created")
    except socket.error as err:
        print('socket open error: {}\n'.format(err))
        exit()

    server_binding = ('', 1903)
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
    print('[S]: Server recieved {} from the client'.format(queried_hostname))

    # next part is the table lookup to give the client its respective string
    queried_string = check_hostname_table(queried_hostname, table)
    csockid.send(queried_string.encode('utf-8'))

    ss.close()
    exit()


if __name__ == "__main__":
    rs_server()
    