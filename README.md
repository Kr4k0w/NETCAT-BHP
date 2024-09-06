# NETCAT-BHP 🐈‍⬛

**NETCAT-BHP** is a versatile networking tool written in Python 3, inspired by the classic Netcat utility and developed based on concepts from the “Black Hat Python” book. This tool aims to provide a powerful and flexible solution for network communication, debugging, and penetration testing.

- Leave your ⭐ to increase the visibility of this project, and if you can, share it! I'm counting with you!


![image](https://github.com/user-attachments/assets/3f4c2a38-db2d-4ced-9aac-6bd26693412c)





## Features 
- File Transfer: Easily transfer files between systems over a network.
- Reverse Shell: Establish a reverse shell connection for remote command execution.
- Bind Shell: Set up a bind shell to listen for incoming connections.

## Install
Clone the repository and navigate to the project directory:

``` shell
git clone https://github.com/Kr4k0w/NETCAT-BHP.git
cd NETCAT-BHP
```

## Usage
Run the tool with the desired options:
``` python
python netcat_bhp.py -t [ip] -p [port] [options]

```
- Press CTRL + D to start the shell

![image](https://github.com/user-attachments/assets/c31dd301-f4dd-40f5-9a98-94010cf072d8)


- Use --help or -h to show this guide


``` shell
usage: netcat_bhp.py [-h] [-c] [-e EXECUTE] [-l] [-p PORT] [-t TARGET] [-u UPLOAD]

BHP Net Tool

options:
  -h, --help            show this help message and exit
  -c, --command         Open a shell command interface
  -e EXECUTE, --execute EXECUTE
                        Execute a specific command on connect
  -l, --listen          Listen for incoming connections
  -p PORT, --port PORT  Port to bind/connect to
  -t TARGET, --target TARGET
                        Target IP to connect to
  -u UPLOAD, --upload UPLOAD
                        File path to upload

Exemple:
        netcat.py -t [ip] -p [port] -l -c #shell command
        netcat.py -t [ip] -p [port] -l -u=file.txt #upload file
        netcat.py -t [ip] -p [port] -l -e="cat /etc/passwd" #execute command

        echo 'ABC' | netcat.py -t [ip] -p [port] #send text to port of server

        netcat.py -t [ip] -p [port] #connect to the server
```


## Contributing
Contributions are welcome!

## Reference

![image](https://github.com/user-attachments/assets/43e4d62c-c7e9-4a15-902b-fe0d5b1ae6df)

- Black Hat Python, 2nd Edition: Python Programming for Hackers and Pentesters
- by Justin Seitz (Autor), Tim Arnold (Autor)
