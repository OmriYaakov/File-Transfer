
# File Transfer Application

This project is a Python-based client-server application that allows users to transfer files between connected clients in a network. It uses TCP sockets for communication and is designed with a graphical user interface (GUI) for ease of use.

## Features

- **Client-Server Architecture**: Clients connect to a central server to send and receive files.
- **File Transfer**: Send various types of files to other connected users.
- **User Management**: The server keeps track of connected users and broadcasts this information to all clients.
- **Graphical User Interface**: The client application is equipped with a GUI built using Tkinter, making it user-friendly.
- **Multi-threading**: Both the server and client handle multiple connections simultaneously using threading.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
   ```

2. Install the required dependencies (if any):

   ```bash
   pip install -r requirements.txt
   ```

3. Run the server:

   ```bash
   python server.py
   ```

4. Run the client:

   ```bash
   python client.py
   ```

## Usage

### Server

- **Run the server**: The server will start listening for incoming client connections on the default port `5011`.
- **Handling Clients**: As clients connect, the server assigns them a username and manages file transfers between them.
- **Broadcasting Online Users**: The server continuously updates and broadcasts the list of online users.

### Client

- **Connect to Server**: Enter a username and connect to the server.
- **Send Files**: Select a user from the online list and choose a file to send.
- **Receive Files**: The client automatically handles incoming files and saves them to the local machine.

## File Structure

- **server.py**: Contains the server code which manages client connections and file transfers.
- **client.py**: Contains the client code which connects to the server, allows file sending, and handles file reception.
- **README.md**: This file, providing an overview and instructions.

## Author

- **Omri Yaakov**

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
