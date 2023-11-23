import socket
import threading

class ChatServer:
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = ('127.0.0.1', 5555)

        self.server_socket.bind(self.server_address)
        self.server_socket.listen(1)

        print('Server listening on {}:{}'.format(*self.server_address))

        self.clients = []
        self.lock = threading.Lock()

        self.accept_connections()

    def accept_connections(self):
        while True:
            client_socket, client_address = self.server_socket.accept()
            print('Accepted connection from {}:{}'.format(*client_address))

            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()

            with self.lock:
                self.clients.append((client_socket, client_thread))

    def handle_client(self, client_socket):
        while True:
            try:
                data = client_socket.recv(1024)
                if not data:
                    break
                message = data.decode('utf-8')
                print('Received message: {}'.format(message))

              
                with self.lock:
                    self.broadcast(message, client_socket)

            except Exception as e:
                print(str(e))
                break

        with self.lock:
            self.clients = [(sock, thread) for sock, thread in self.clients if sock != client_socket]

    def broadcast(self, message, sender_socket):
        for client, _ in self.clients:
            if client != sender_socket:
                try:
                    client.send(message.encode('utf-8'))
                except Exception as e:
                    print(str(e))

    def stop_server(self):
        with self.lock:
            for client_socket, _ in self.clients:
                client_socket.close()

        self.server_socket.close()

if __name__ == "__main__":
    chat_server = ChatServer()
    try:
        input("Press Enter to stop the server.\n")
    except KeyboardInterrupt:
        pass
    finally:
        chat_server.stop_server()
