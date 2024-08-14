import socket
import threading
import struct
import os

app = Flask(__name__)

# Author: Omri Yaakov
# Server Details: A Server that accepts new clients and forwards files from one client to another.

class Server:
    #Initialize the server, configure the TCP socket, and prepare to accept client connections.
    def __init__(self, tcp_port=5011):
        self.tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.tcp_server_socket.bind(("0.0.0.0", tcp_port))
        self.tcp_server_socket.listen(5)

        self.clients = {}  

    #Send a message to all connected clients, optionally excluding one specific client.
    def broadcast(self, message, exclude_client=None):
        encoded_message = message.encode()
        message_length = struct.pack('!I', len(encoded_message))
        for client in self.clients.keys():
            if client != exclude_client:
                try:
                    client.sendall(message_length + encoded_message)
                except:
                    self.remove_client(client)

    #Remove a client from the server's list, notify others of their departure, and update the online users list.
    def remove_client(self, client_socket):
        username = self.clients.pop(client_socket, None)
        if username:
            self.broadcast(f"{username} has left the chat.")
            self.broadcast_online_users()

    #Broadcast the current list of online users to all connected clients.
    def broadcast_online_users(self):
        online_users = ",".join(self.clients.values())
        print(f"Broadcasting online users: {online_users}")
        self.broadcast(f"ONLINE_USERS:{online_users}")

    #Handle the communication with a connected TCP client, including receiving messages and processing file transfers.
    def handle_tcp_client(self, client_socket):
        try:
            username = client_socket.recv(1024).decode()
            if username in self.clients.values():
                error_message = "ERROR: Username already taken. Choose another one."
                client_socket.sendall(struct.pack('!I', len(error_message)) + error_message.encode())
                client_socket.close()
                return
            self.clients[client_socket] = username
            self.broadcast(f"{username} has joined the chat.")
            self.broadcast_online_users()

            while True:
                header = self._recv_exact(client_socket, 4)
                if not header:
                    break
                length = struct.unpack('!I', header)[0]
                data = self._recv_exact(client_socket, length)

                if data.startswith(b"DISCONNECT"):
                    break

                if data.startswith(b"@#@#@#"):
                    print(f"Server received file transfer request from {username}")
                    self.handle_file_transfer(client_socket, data)

        except Exception as e:
            print(f"Error handling client: {e}")
        finally:
            self.remove_client(client_socket)
            client_socket.close()

    #Helper function to receive an exact number of bytes from a client socket.
    def _recv_exact(self, sock, size):
        buffer = b""
        while len(buffer) < size:
            more_data = sock.recv(size - len(buffer))
            if not more_data:
                raise ConnectionError("Connection closed unexpectedly")
            buffer += more_data
        return buffer

    #Process an incoming file transfer request and forward the file to the intended recipient(s).
    def handle_file_transfer(self, client_socket, data):
        try:
            print("Starting file transfer...")
            data_parts = data.split(b'@#@#@')
            recipient_name = data_parts[1].decode().strip().lstrip('#')
            sender_name = data_parts[2].decode().strip()
            file_size = int(data_parts[3].decode().strip())
            file_name = data_parts[4].decode().strip()
            file_data = data.split(b'@#@#@')[5]

            if len(file_data) < file_size:
                file_data += self._recv_exact(client_socket, file_size - len(file_data))

            if len(file_data) == file_size:
                if recipient_name.lower() == 'all':
                    print("Sending file to all clients except sender...")
                    for soc in self.clients.keys():
                        if soc != client_socket:
                            self.send_file(soc, recipient_name, sender_name, file_name, file_data)
                            print(f"File sent to {self.clients[soc]}")
                else:
                    recipient_socket = None
                    for soc in self.clients.keys():
                        stored_name = self.clients[soc].strip()
                        if stored_name.lower() == recipient_name.lower():
                            recipient_socket = soc
                            break
                    if recipient_socket:
                        self.send_file(recipient_socket, recipient_name, sender_name, file_name, file_data)
                        print(f"File successfully sent to {recipient_name}")
                    else:
                        print(f"Recipient {recipient_name} not found!")

        except Exception as e:
            print(f"Error during file transfer: {e}")

    #Send the specified file data to the designated recipient client.
    def send_file(self, recipient_socket, recipient_name, sender_name, file_name, file_data):
        try:
            message = f"@#@#@#{recipient_name}@#@#@{sender_name}@#@#@{len(file_data)}@#@#@{file_name}@#@#@".encode() + file_data
            message_length = struct.pack('!I', len(message))
            recipient_socket.sendall(message_length + message)
            print(f"Sent file '{file_name}' of size {len(file_data)} bytes to {recipient_name}")
        except Exception as e:
            print(f"Error sending file to client: {e}")

    #Continuously accept new client connections and start a new thread to handle each client.
    def run(self):
        while True:
            client_socket, addr = self.tcp_server_socket.accept()
            threading.Thread(target=self.handle_tcp_client, args=(client_socket,)).start()

#Main Function - Run the Server
if __name__ == "__main__":
    server = Server()
    server.run()
