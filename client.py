import time, random, socket

# goal of this function is to eventually send all the hosts on here to the rs server for a look up
# but to start we'll just use the very first one
def query_hostname_table():
    queried_hostname = None
    file = open("PROJI-HNS.txt", "r")
    for host in file:
        return host.replace('\r\n', '')
    f.close()

def client():
    # initial setup for the client side
    try:
        cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[C]: Client socket created")
    except socket.error as err:
        print('socket open error: {} \n'.format(err))
        exit()
        
    port = 1903
    localhost_addr = socket.gethostbyname(socket.gethostname())

    server_binding = (localhost_addr, port)
    cs.connect(server_binding)

    '''
    Use send instead of sendall
    '''

    # first task of client is to query the table and send the queried hostname to rs server
    queried_hostname = query_hostname_table()
    cs.send(queried_hostname.encode('utf-8'))

    # recieve the queried string from the client 
    server_string = cs.recv(1024)
    print('Returned {} from the server'.format(server_string.decode('utf-8')))

    # tokenize the string to check the flag portion which should be at token[2]
    tokens = server_string.split()
    if tokens[2] == 'A':
        print(server_string)
        cs.close()
        exit()

    cs.close()
    exit()

if __name__ == "__main__":
    client()