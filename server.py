import socket
import sys
import threading


class User:

    def __init__(self, n, c, a):
        self.username = n
        self.connection = c
        self.address = a
        self.prefix = '[{}] '.format(self.username).encode('utf-8')

    def sendMsg(self, data):
        self.connection.send(data)


users = []


def listenUser(user):
    global users

    flag = True

    while flag:
        data = user.connection.recv(1024)

        if not data:
            text = '[SERVER] ' + user.username + ' disconnected'

            data = text.encode('utf-8')
            users.remove(user)
            user.connection.close()
            flag = False
        else:
            data = user.prefix + data
        print(data.decode('utf-8'))

        for u in users:
            if u is not user:
                u.sendMsg(data)


if len(sys.argv) is not 3:
    print("[ERROR] Usage: \"server.py <host> <port>\"")
else:
    host = sys.argv[1]
    port = int(sys.argv[2])
    try:
        s = socket.socket()
        s.bind((host, port))
        s.listen(1)
        print('Server running...')

        while True:
            c, a = s.accept()

            # Create User
            name = c.recv(1024).decode('utf-8')
            newUser = User(name, c, a)
            users.append(newUser)

            # Notify Users
            text = '[SERVER] ' + name + ' connected'
            print(text)
            newUser.sendMsg(
                '[SERVER] Welcome, {}!'.format(name).encode('utf-8'))
            for u in users:
                if u is not newUser:
                    u.sendMsg(text.encode('utf-8'))

            # Listen User
            thread = threading.Thread(target=listenUser, args=(newUser,))
            thread.daemon = True
            thread.start()

    except KeyboardInterrupt:
        sys.exit(0)
    except:
        print('[ERROR] Server closed.')
