import socket
import json
import threading
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Shared data store for processed GNSS data with thread lock
latest_gnss_data = []
data_lock = threading.Lock()

# Define constants and configurations
HOST = '0.0.0.0'  # Bind to all available network interfaces
PORT = 5001

@app.route('/gnss-data', methods=['GET'])
def get_gnss_data():
    global latest_gnss_data
    with data_lock:
        data = latest_gnss_data
    print(f"Serving data: {data}")  # Log the data being served
    return jsonify(data)

@app.route('/gnss-data', methods=['POST'])
def update_gnss_data():
    global latest_gnss_data
    gnss_data = request.json
    print(f"Received data: {gnss_data}")  # Log the received data

    # Update the shared data store with a lock
    with data_lock:
        latest_gnss_data = gnss_data
    return jsonify({"status": "success"}), 200

def start_socket_server():
    global latest_gnss_data

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    print("Waiting for connection...")

    connection, address = server_socket.accept()
    print(f"Connection established with {address}")

    buffer = ''
    while True:
        data = connection.recv(4096).decode('utf-8')
        if not data:
            break

        buffer += data
        print(f"Raw data received: {buffer}")
        try:
            while buffer:
                gnss_data, index = json.JSONDecoder().raw_decode(buffer)
                buffer = buffer[index:].strip()

                if isinstance(gnss_data, dict):
                    gnss_data = [gnss_data]

                print(f"Received data: {gnss_data}")

                # Update the shared data store with a lock
                with data_lock:
                    latest_gnss_data = gnss_data
                print(f"Updated latest_gnss_data: {latest_gnss_data}")

                connection.sendall(json.dumps({"status": "success"}).encode('utf-8'))
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            continue
        except Exception as e:
            print(f"Error processing data: {e}")

    connection.close()
    server_socket.close()

if __name__ == "__main__":
    socket_thread = threading.Thread(target=start_socket_server)
    socket_thread.start()
    app.run(host='192.168.43.53', port=5000)