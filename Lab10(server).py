import socket
import threading

class ChatServer:
    def __init__(self):
        #Створення сокету для взаємодії з клієнтами.
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #Визначення адреси та порту сервера.
        self.server_address = ('127.0.0.1', 5555)
        #Прив'язка сокету до визначеної адреси та порту.
        self.server_socket.bind(self.server_address)
        #Прослуховування вхідних з'єднань, обмеження на одне з'єднання одночасно.
        self.server_socket.listen(1)
        print('Server listening on {}:{}'.format(*self.server_address))
        #Ініціалізація списку підключених клієнтів.
        self.clients = []
        #Створення об'єкта блокування для безпечного доступу до ресурсів з різних потоків.
        self.lock = threading.Lock()
        # Виклик методу для прийому з'єднань від клієнтів.
        self.accept_connections()
    #Метод для прийому з'єднань від клієнтів.Безкінечний цикл, який очікує та приймає нові з'єднання від клієнтів.
    def accept_connections(self):
        while True:
            #Блокування до отримання нового з'єднання та отримання сокету та адреси клієнта.
            client_socket, client_address = self.server_socket.accept()
            print('Accepted connection from {}:{}'.format(*client_address))
            #Створення окремого потоку для обробки клієнта.
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            #Запуск потоку обробки клієнта.
            client_thread.start()
            #Додавання інформації про клієнта до списку, забезпечуючи безпеку в многопоточному середовищі.
            with self.lock:
                self.clients.append((client_socket, client_thread))

    #Метод для обробки повідомлень від конкретного клієнта.
    def handle_client(self, client_socket):
        while True:
            try:
                #Блокування до отримання даних від клієнта (до 1024 байт).
                data = client_socket.recv(1024)
                if not data:
                    break
                #Декодування отриманого повідомлення з байтового представлення у рядок.
                message = data.decode('utf-8')
                print('Received message: {}'.format(message))

                #Виклик методу для розсилки повідомлення усім іншим клієнтам.
                with self.lock:
                    self.broadcast(message, client_socket)

            except Exception as e:
                print(str(e))
                break

        with self.lock:
            self.clients = [(sock, thread) for sock, thread in self.clients if sock != client_socket]
    #Метод для розсилки повідомлення усім іншим клієнтам.
    def broadcast(self, message, sender_socket):
        #Проходження усіх клієнтів у списку.
        for client, _ in self.clients:
            #Якщо клієнт не є тим, хто відправив повідомлення:
            if client != sender_socket:
                try:
                    #Надсилання повідомлення клієнту (кодування у байти перед надсиланням).
                    client.send(message.encode('utf-8'))
                    #Обробка можливих помилок при надсиланні.
                except Exception as e:
                    print(str(e))

    #Метод для закриття всіх з'єднань та завершення роботи сервера.
    def stop_server(self):
        #Захоплення блокування для забезпечення безпеки при доступі до ресурсів з різних потоків.
        with self.lock:
            # Проходження усіх клієнтів та їхніх потоків.
            for client_socket, _ in self.clients:
                client_socket.close()

        self.server_socket.close()
#Перевірка, чи код виконується як основна програма (а не імпортований як модуль).
if __name__ == "__main__":
    #Створення об'єкта ChatServer.
    chat_server = ChatServer()
    try:
        #Чекання введення користувача для зупинки сервера.
        input("Press Enter to stop the server.\n")
        #Обробка винятку, який виникає при натисканні Ctrl+C для зупинки сервера.
    except KeyboardInterrupt:
        pass
    #Завершення роботи сервера в будь-якому випадку, навіть якщо виникає виняток.
    finally:
        chat_server.stop_server()
