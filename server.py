import socket
import threading

HOST = 'localhost'
PORT = 65000

clients = []

def broadcast(message, sender):
    for client in clients:
        if client != sender:
            try:
                client.send(message)
            except:
                index = clients.index(client)
                clients.remove(client)
                client.close()
                print(f'Клиент {index} отключился.')

def handle(client):
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message:

                broadcast(message.encode('utf-8'), client)
            else:

                index = clients.index(client)
                clients.remove(client)
                client.close()
                print(f'Клиент {index} отключился.')
                break
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            print(f'Клиент {index} отключился.')
            break

def receive():
    while True:
        try:
            client, address = server.accept()
            print(f'Новое соединение от {str(address)}')

            client.send('NICK_OR_REGISTER'.encode('utf-8'))
            response = client.recv(1024).decode('utf-8')

            if response == 'REGISTER':
                client.send('REGISTER_USERNAME'.encode('utf-8'))
                nick = client.recv(1024).decode('utf-8')
                client.send('REGISTER_PASSWORD'.encode('utf-8'))
                password = client.recv(1024).decode('utf-8')

                if True:
                    clients.append(client)
                    print(f'Пользователь {nick} зарегистрировался и присоединился к чату')
                    broadcast(f'{nick} присоединился к чату!'.encode('utf-8'), client)
                    client.send('Вы успешно зарегистрировались и вошли в чат!'.encode('utf-8'))

                    handle_thread = threading.Thread(target=handle, args=(client,))
                    handle_thread.start()

                else:
                    client.close()
                    print(f'Ошибка регистрации пользователя {nick}.')

            else:
                client.send('NICK'.encode('utf-8'))
                nick = client.recv(1024).decode('utf-8')
                client.send('PASSWORD'.encode('utf-8'))
                password = client.recv(1024).decode('utf-8')
                if True:
                    clients.append(client)
                    print(f'Пользователь {nick} присоединился к чату')
                    broadcast(f'{nick} присоединился к чату!'.encode('utf-8'), client)
                    client.send('Вы успешно вошли в чат!'.encode('utf-8'))

                    handle_thread = threading.Thread(target=handle, args=(client,))
                    handle_thread.start()

                else:
                    client.send('AUTH_FAILED'.encode('utf-8'))
                    client.close()
                    print(f'Ошибка авторизации пользователя {nick}.')
        except:
            print('Ошибка при обработке клиента.')

print('Сервер работает...')
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 65000))
server.listen()
receive()