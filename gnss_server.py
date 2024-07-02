import socket

# Set up a TCP server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('192.168.33.5', 5000))  # Bind to all interfaces on port 5000
server_socket.listen(1)
print("Waiting for connection...")

connection, address = server_socket.accept()
print(f"Connection established with {address}")

while True:
    data = connection.recv(1024).decode('utf-8')
    if not data:
        break
    print(data)

connection.close()