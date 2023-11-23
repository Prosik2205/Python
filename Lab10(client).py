import tkinter as tk
from tkinter import scrolledtext
import socket
import threading

class ChatClient:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat Client")

        self.chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=10)
        self.chat_area.pack(padx=10, pady=10)

        self.message_entry = tk.Entry(root, width=30)
        self.message_entry.pack(padx=10, pady=10)

        self.send_button = tk.Button(root, text="Send", command=self.send_message)
        self.send_button.pack(pady=10)

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = ('127.0.0.1', 5555)

        try:
            self.client_socket.connect(self.server_address)
        except socket.error as e:
            print(str(e))

        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.start()

    def send_message(self):
        message = self.message_entry.get()
        if message:
            self.update_chat_area(f"You: {message}")

            self.client_socket.send(message.encode('utf-8'))
            
            self.message_entry.delete(0, tk.END)

    def receive_messages(self):
        while True:
            try:
                data = self.client_socket.recv(1024)
                if not data:
                    break
                message = data.decode('utf-8')
                
                self.update_chat_area(message)
                
            except Exception as e:
                print(str(e))
                break

    def update_chat_area(self, message):
        self.chat_area.insert(tk.END, message + '\n')
        self.chat_area.yview(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    chat_client = ChatClient(root)
    root.mainloop()
