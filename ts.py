import time, random, socket

class TS:
    hostname = None
    ip = None 
    flag = None

    def __init__(self, hostname, ip, flag):
        self.hostname = hostname
        self.ip = self.ip
        self.flag = flag

def ts_server():
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

    ss.close()
    exit()


if __name__ == "__main__":
    ts_server()