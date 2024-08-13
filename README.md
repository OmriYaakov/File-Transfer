# File Transfer Application

## Overview

This project implements a client-server file transfer application in Python. The client, packaged as `fileTransfer.exe`, provides a GUI for selecting and sending files to other connected users. The server is hosted on GitHub Pages and manages connections and facilitates file transfers between clients.

## Prerequisites

- `fileTransfer.exe` (The client executable)
- Internet access (to connect to the server hosted on GitHub Pages)

## Installation

1. **Download the `fileTransfer.exe` executable.**

2. **Run the executable:**

    Simply double-click `fileTransfer.exe` to start the client application.

## Usage

### Server

- **Hosted on GitHub Pages:** The server is automatically managed and does not require any local setup.
- **User Management:** The server keeps track of connected users and broadcasts this information.

### Client (fileTransfer.exe)

- **Connect to Server:** Enter a username to connect to the server.
- **Send Files:** Select a user from the list of online users and choose a file to send.
- **Receive Files:** The client automatically handles incoming files and saves them locally.

## File Structure

- **fileTransfer.exe**: The client executable for connecting to the server, sending files, and receiving files.
- **README.md**: This file, providing an overview and instructions.

## Author

- **Omri Yaakov**

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
