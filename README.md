
"""
# File Transfer Application

## Overview

This project implements a client-server file transfer application in Python. The server manages connections and facilitates file transfers between clients, while the client provides a GUI for selecting and sending files to other connected users.

## Prerequisites

- Python 3.x
- `socket` (Python standard library)
- `struct` (Python standard library)
- `tkinter` (Python standard library)

## Installation

1. **Clone the repository or download the source code.**

2. **the server is running:**

    ```
    code: server.py
    ```

3. **Run the client:**

    ```bash
    launch FileTransfer.exe
    ```

## Usage

### Server

- **Run the server:** The server listens for incoming client connections and handles file transfers.
- **User Management:** The server keeps track of connected users and broadcasts this information.

### Client

- **Connect to Server:** Enter a username to connect to the server.
- **Send Files:** Select a user from the list of online users and choose a file to send.
- **Receive Files:** The client automatically handles incoming files and saves them locally.

## File Structure

- **server.py**: Contains the server code for managing client connections and file transfers.
- **client.py**: Contains the client code for connecting to the server, sending files, and receiving files.
- **README.md**: This file, providing an overview and instructions.

## Author

- **Omri Yaakov**

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
"""
