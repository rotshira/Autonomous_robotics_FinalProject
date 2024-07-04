import socket
import json

# Define constants and configurations
HOST = '192.168.43.53'  # Your server IP
PORT = 5000


# Function to filter satellites by constellation and Otzena
def filter_satellites(data, constellation=None, otzena_threshold=None):
    if constellation:
        data = [d for d in data if d.get('constellation') == constellation]
    if otzena_threshold:
        data = [d for d in data if d.get('otzena', 0) > otzena_threshold]
    return data


# Function to identify false satellites
def identify_false_satellites(data):
    # Placeholder: Add your logic to identify false satellites
    # Example: Filter out satellites with unlikely Doppler shift values
    return [d for d in data if abs(d.get('doppler', 0)) < 1000]


# Function to detect interference ("Cairo + Beirut")
def detect_interference(data):
    # Placeholder: Add your logic to detect interference
    # Example: Identify interference based on CN0 value patterns
    interference_detected = any(d.get('cn0', 0) < 20 for d in data)
    return interference_detected


# Function to handle interference
def handle_interference(data):
    # Placeholder: Add your logic to handle interference
    # Example: Remove data points affected by interference
    return [d for d in data if d.get('cn0', 0) >= 20]


# Main function to process incoming GNSS data
def process_gnss_data(data):
    # Ensure data is a list of dictionaries
    if isinstance(data, dict):
        data = [data]

    # Step 1: Filter satellites
    filtered_data = filter_satellites(data, constellation='GPS', otzena_threshold=30)

    # Step 2: Identify and filter false satellites
    filtered_data = identify_false_satellites(filtered_data)

    # Step 3: Detect and handle interference
    if detect_interference(filtered_data):
        filtered_data = handle_interference(filtered_data)

    return filtered_data


# Start the server
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))  # Bind to the specified IP and port
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
        try:
            while buffer:
                gnss_data, index = json.JSONDecoder().raw_decode(buffer)
                buffer = buffer[index:].strip()

                if isinstance(gnss_data, dict):
                    gnss_data = [gnss_data]  # Ensure it is a list of dictionaries

                print(f"Received data: {gnss_data}")

                # Process the GNSS data
                processed_data = process_gnss_data(gnss_data)

                # Send back the processed data (for example purposes)
                connection.sendall(json.dumps(processed_data).encode('utf-8'))
        except json.JSONDecodeError:
            # Wait for more data
            continue
        except Exception as e:
            print(f"Error processing data: {e}")

    connection.close()
    server_socket.close()


if __name__ == "__main__":
    start_server()
