import socket
import threading

HOST = 'localhost'
PORT = 65000

def receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            print(message)
        except:
            print('Произошла ошибка, соединение закрыто')
            client.close()
            break

def write():
    while True:
        try:
            message = input()
            client.sendall(f"MESSAGE:{message}".encode('utf-8'))
        except:
            print('Произошла ошибка, соединение закрыто')
            client.close()
            break

def start_client():

    global client
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    while True:
        action = input("Введите действие (REGISTER/LOGIN): ")
        if action == "REGISTER":
            nickname = input("Введите никнейм: ")
            password = input("Введите пароль: ")
            client.sendall(f"REGISTER:{nickname}:{password}".encode('utf-8'))
            result = client.recv(1024).decode('utf-8')
            if result == "REGISTER_SUCCESS":
                print("Вы успешно зарегистрировались и вошли в чат!")
                break
            else:
                print("Ошибка регистрации. Попробуйте другой никнейм.")
                client.close()
                break
        elif action == "LOGIN":
            nickname = input("Введите никнейм: ")
            password = input("Введите пароль: ")
            client.sendall(f"LOGIN:{nickname}:{password}".encode('utf-8'))
            result = client.recv(1024).decode('utf-8')
            if result == "AUTH_SUCCESS":
                print("Вы успешно вошли в чат!")
                break
            else:
                print("Неверный логин или пароль. Попробуйте еще раз.")
                client.close()
                break
        else:
            print("Неверная команда.")

    receive_thread = threading.Thread(target=receive)
    receive_thread.start()
    write_thread = threading.Thread(target=write)
    write_thread.start()

if __name__ == '__main__':
    start_client()