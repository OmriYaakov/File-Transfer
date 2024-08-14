import sys
import os
import socket
import threading
import struct
import tkinter as tk
from tkinter import filedialog, ttk

# Author: Omri Yaakov
# Client Details: An application that connects to the server and can transfer all kinds of files to other clients that are connected to the server as well.

class Client:
    #Initialize the client, set up the socket connection, and start the UI.
    def __init__(self, host="127.0.0.1", tcp_port=5011):
        self.host = host
        self.tcp_port = tcp_port

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False
        try:
            self.client_socket.connect((host, tcp_port))
            print(f"Connected to server at {host}:{tcp_port}")
            self.connected = True
        except Exception as e:
            print(f"Error connecting to server: {e}")
            self.client_socket.close()
            return

        self.username = None
        self.online_users = []

        self.root = tk.Tk()
        self.root.title("FileTransfer")
        self.root.geometry("740x380")
        self.root.configure(bg="#a6a6ed")

        self.setup_ui()

        threading.Thread(target=self.receive_data, daemon=True).start()
        self.root.mainloop()

    #Configure the main UI elements and layout for the client application.
    def setup_ui(self):
        self.main_frame = tk.Frame(self.root, bg="#a6a6ed")
        self.main_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

        self.username_frame = tk.Frame(self.main_frame, bg="#a6a6ed")
        self.username_frame.grid(row=0, column=0, pady=10, sticky="w")

        self.username_label = tk.Label(self.username_frame, text="Enter Username:", bg="#a6a6ed", font=("Arial", 14))
        self.username_label.pack(side=tk.LEFT, padx=5)

        self.username_entry = tk.Entry(self.username_frame, font=("Arial", 14))
        self.username_entry.pack(side=tk.LEFT, padx=5)

        self.connect_button = tk.Button(self.username_frame, text="Connect", command=self.connect_to_server, bg="#FFFFFF", font=("Arial", 14))
        self.connect_button.pack(side=tk.LEFT, padx=5)

        self.status_label = tk.Label(self.main_frame, text="", bg="#a6a6ed", font=("Arial", 14))
        self.status_label.grid(row=1, column=0, pady=5)

        self.progress_label = tk.Label(self.main_frame, text="", bg="#a6a6ed", font=("Arial", 14))
        self.progress_label.grid(row=2, column=0, pady=5)

        self.actions_frame = tk.Frame(self.main_frame, bg="#a6a6ed")
        self.actions_frame.grid(row=3, column=0, pady=20)

        self.send_button = tk.Button(self.actions_frame, text="Send File", command=self.initiate_file_send, bg="#FFFFFF", font=("Arial", 14))
        self.send_button.pack(side=tk.LEFT, padx=10)

        self.disconnect_button = tk.Button(self.actions_frame, text="Disconnect", command=self.disconnect, bg="#FFFFFF", font=("Arial", 14))
        self.disconnect_button.pack(side=tk.LEFT, padx=10)

        self.users_frame = tk.Frame(self.main_frame, bg="#a6a6ed")
        self.users_frame.grid(row=0, column=1, rowspan=4, padx=20, pady=20, sticky="n")

        self.users_label = tk.Label(self.users_frame, text="Online Users", bg="#a6a6ed", font=("Arial", 14))
        self.users_label.pack()

        self.users_listbox = tk.Listbox(self.users_frame, font=("Arial", 12), selectmode=tk.SINGLE, bg="#a6a6ed", height=15)
        self.users_listbox.pack(fill=tk.Y, expand=True)

    #Send the username to the server and disable the input fields upon successful connection.
    def connect_to_server(self):
        if not self.connected:
            try:
                self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.client_socket.connect((self.host, self.tcp_port))
                self.connected = True
                threading.Thread(target=self.receive_data, daemon=True).start()
            except Exception as e:
                self.update_status_label(f"Error: {e}")
                return

        self.username = self.username_entry.get()
        if self.username:
            try:
                self.client_socket.sendall(self.username.encode())

            except Exception as e:
                print(f"Error during username verification: {e}")
                self.root.after(0, self.update_status_label, f"Error: {e}")
                self.client_socket.close()
                self.connected = False

    #If the username is taken so it will let the client pick another one
    def reenable_username_entry(self):
        self.username_entry.config(state=tk.NORMAL)
        self.connect_button.config(state=tk.NORMAL)

    #Continuously listen for incoming data from the server and handle it appropriately.
    def receive_data(self):
        while self.connected:
            try:
                header = self.client_socket.recv(4)
                if not header:
                    self.connected = False
                    break

                length = struct.unpack('!I', header)[0]
                data = self._recv_exact(length)
                if data:
                    threading.Thread(target=self.handle_raw_data, args=(data,), daemon=True).start()

            except Exception as e:
                self.connected = False
                break

    #Helper function to receive an exact number of bytes from the server.
    def _recv_exact(self, length):
        buffer = b''
        while len(buffer) < length:
            more_data = self.client_socket.recv(length - len(buffer))
            if not more_data:
                raise ConnectionError("Connection lost while receiving data.")
            buffer += more_data
        return buffer

    #Process the raw data received from the server, determining its type and handling it accordingly.
    def handle_raw_data(self, data):
        try:
            if data.startswith(b"ERROR"):
                error_message = data.decode()
                self.root.after(0, self.update_status_label, error_message)
                self.root.after(0, self.reenable_username_entry)
                self.client_socket.close()
                self.connected = False
            elif data.startswith(b"ONLINE_USERS:"):
                users = data[len(b"ONLINE_USERS:"):].decode().strip()
                self.root.after(0, self.update_status_label, "")
                self.root.after(0, self.update_users_listbox, users.split(','))
                self.username_entry.config(state=tk.DISABLED)
                self.connect_button.config(state=tk.DISABLED)
            elif data.startswith(b"@#@#@#"):
                self.root.after(0, self.update_status_label, "Receiving...")
                threading.Thread(target=self.handle_file_data, args=(data,), daemon=True).start()
        except Exception as e:
            print(f"Error handling raw data: {e}")

    #Handle the file transfer data, manage file reception, and update the UI with progress.
    def handle_file_data(self, data):
        try:
            data_parts = data.split(b'@#@#@')
            recipient_name = data_parts[1].decode()
            sender_name = data_parts[2].decode()
            file_size = int(data_parts[3].decode())
            file_name = data_parts[4].decode()
            file_data = data.split(b'@#@#@')[5]

            received_file_data = file_data

            while len(received_file_data) < file_size:
                more_data = self._recv_exact(min(4096, file_size - len(received_file_data)))
                received_file_data += more_data
                progress = (len(received_file_data) / file_size) * 100
                self.root.after(0, self.update_progress_label, f"Receiving: {progress:.2f}%")

            self.save_file(file_name, received_file_data)
            self.root.after(0, self.update_status_label, "File received successfully.")
            self.root.after(0, self.update_progress_label, "") 

        except Exception as e:
            self.root.after(0, self.update_status_label, "Error during receiving.")
            self.root.after(0, self.update_progress_label, "")

    #Save the received file to the local system, ensuring a unique filename if needed.
    def save_file(self, file_name, file_data):
        try:
            counter = 1
            base_filename, file_extension = os.path.splitext(file_name)
            save_filename = file_name

            while os.path.exists(save_filename):
                save_filename = f"{base_filename}_{counter}{file_extension}"
                counter += 1

            with open(save_filename, 'wb') as file:
                file.write(file_data)

            print(f"File saved as '{save_filename}'.")
            self.root.after(0, self.update_status_label, f"File '{save_filename}' saved.")

        except Exception as e:
            print(f"Error saving file: {e}")
            self.root.after(0, self.update_status_label, "Error saving file.")

    #Start a new thread to handle the process of selecting and sending a file to another user.
    def initiate_file_send(self):
        threading.Thread(target=self.send_file, daemon=True).start()

    #Send the selected file to the specified recipient, updating the UI with the sending progress.
    def send_file(self):
        self.root.after(0, self.update_status_label, "")
        selected_user_index = self.users_listbox.curselection()
        if not selected_user_index:
            self.root.after(0, self.update_status_label, "No user selected.")
            return

        recipient = self.online_users[selected_user_index[0]]
        self.root.after(0, self.update_status_label, "")
        self.root.after(0, self.update_progress_label, "")
        file_path = filedialog.askopenfilename()

        if file_path:
            try:
                self.root.after(0, self.update_status_label, "Sending...")
                with open(file_path, 'rb') as f:
                    file_data = f.read()
                    file_name = os.path.basename(file_path)
                    total_size = len(file_data)
                    message = f"@#@#@#{recipient}@#@#@{self.username}@#@#@{total_size}@#@#@{file_name}@#@#@".encode()
                    message_length = struct.pack('!I', len(message) + total_size)
                    self.client_socket.sendall(message_length + message)
                    sent_size = 0

                    while sent_size < total_size:
                        chunk_size = min(4096, total_size - sent_size)
                        chunk_data = file_data[sent_size:sent_size + chunk_size]
                        self.client_socket.sendall(chunk_data)
                        sent_size += chunk_size
                        progress = (sent_size / total_size) * 100
                        self.root.after(0, self.update_progress_label, f"Sending: {progress:.2f}%")
                        self.root.update_idletasks() 

                    self.root.after(0, self.update_status_label, "File sent.")
                    self.root.after(0, self.update_progress_label, "") 
            except Exception as e:
                self.root.after(0, self.update_status_label, "Error during sending.")
                self.root.after(0, self.update_progress_label, "")

    #Send a disconnect message to the server, close the socket, and exit the application.
    def disconnect(self):
        try:
            self.client_socket.sendall("DISCONNECT".encode())
        except Exception as e:
            print(f"Error sending disconnect: {e}")
        finally:
            self.client_socket.close()
            self.root.quit()
            self.restart()

    # Restart the client application by re-executing the current script.
    def restart(self):
        os.execv(sys.executable, [sys.executable] + sys.argv)

    #Update the list of online users in the UI, applying different background colors for each user.
    def update_users_listbox(self, users):
        self.online_users = users
        self.users_listbox.delete(0, tk.END)
        colors = ["#FF6347", "#40E0D0", "#FF69B4", "#FFD700", "#98FB98", "#FF4500", "#87CEFA", "#DA70D6"]

        if self.username in users:
            users.remove(self.username)

        for index, user in enumerate(users):
            color = colors[index % len(colors)]
            self.users_listbox.insert(tk.END, user)
            self.users_listbox.itemconfig(index, {'bg': color})

    #Update the status label in the UI with the provided message.
    def update_status_label(self, message):
        self.status_label.config(text=message)

    #Update the progress label in the UI with the provided message.
    def update_progress_label(self, message):
        self.progress_label.config(text=message)

#Main Function - Run the Client
if __name__ == "__main__":
    Client()
