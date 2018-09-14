import socket
import sys
import threading


def thread_sendMsg(s, u):

    while True:
        s.send(input().encode('utf-8'))


if len(sys.argv) is not 4:
    print("[ERROR] Usage: \"client.py <user> <host> <port>\"")
else:
    username = sys.argv[1]
    host = sys.argv[2]
    port = int(sys.argv[3])

    try:
        print("Trying to connect...")
        s = socket.socket()
        s.connect((host, port))

        # Send UserName
        s.send(username.encode('utf-8'))

        # Send Msgs
        thread = threading.Thread(target=thread_sendMsg, args=(s, username))
        thread.daemon = True
        thread.start()

        # Recive Msgs
        while True:
            data = s.recv(1024)
            if not data:
                raise
            print(data.decode('utf-8'))

    except KeyboardInterrupt:
        sys.exit(0)
    except:
        print('[ERROR] Client disconnected.')
