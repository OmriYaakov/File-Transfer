
# File Transfer Client-Server Application

## Prerequisites

Before running the application, ensure you have Python 3.x installed on your system. You will also need to install the following Python packages:

### Required Packages

- `socket`: Built-in Python module for networking.
- `threading`: Built-in Python module for threading.
- `struct`: Built-in Python module for handling binary data.
- `os`: Built-in Python module for interacting with the operating system.
- `tkinter`: Python's standard GUI package.

### Installation

To install the required packages, run the following commands:

```bash
pip install tkinter
```

(Note: The `socket`, `threading`, `struct`, and `os` modules are part of the Python standard library and do not require separate installation.)

## Overview

This project is a client-server application written in Python that allows clients to send files to each other via a central server. The server manages client connections, handles file transfers, and broadcasts online users to all connected clients.

## Features

### Server
- Accepts multiple client connections via TCP.
- Manages a list of online users.
- Facilitates file transfers between clients.
- Broadcasts messages to all clients.
- Handles errors during file transfer and client disconnections.

### Client
- Connects to the server via TCP.
- Allows users to select a username and join the server.
- Displays a list of online users.
- Enables file selection and transfer to specific users.
- Updates UI with progress and status messages during file transfer.
- Handles file reception and saving to the local system.
- Allows disconnection from the server.

## Requirements

- Python 3.x
- Tkinter (for GUI)
- A working internet connection for client-server communication

## Usage

### Server

1. **Run the Server:**
   - Start the server by running the `server.py` script.
   - The server will listen for client connections on port `5011`.

   ```bash
   python server.py
   ```

2. **Server Functionalities:**
   - **Broadcast Messages:** The server sends a message to all connected clients.
   - **Manage Online Users:** The server keeps track of connected clients and their usernames, broadcasting the current list of online users.
   - **Handle File Transfers:** The server receives files from one client and forwards them to the intended recipient(s).

### Client

1. **Run the Client:**
   - Start the client by running the `FileTransfer.py` script.

   ```bash
   python FileTransfer.py
   ```

2. **Client Functionalities:**
   - **Connect to the Server:** Enter a username and click "Connect" to join the server.
   - **View Online Users:** The client UI displays a list of users currently online.
   - **Send Files:** Select a user from the list and choose a file to send.
   - **Receive Files:** Files sent to the client are automatically saved to the local system.
   - **Disconnect:** Click "Disconnect" to leave the server.

### GUI Overview

The client application features a simple graphical interface created with Tkinter:

- **Username Entry:** Field to input your desired username before connecting to the server.
- **Connect Button:** Connects to the server with the entered username.
- **Status Label:** Displays the current status, including errors and connection status.
- **Online Users List:** Shows the list of currently connected users.
- **Send File Button:** Opens a dialog to select a file to send to the selected user.
- **Disconnect Button:** Disconnects from the server and closes the client application.

## Author

- Omri Yaakov

## License

This project is open-source and available under the MIT License.
