import socket
import json
import time

# Define constants and configurations
HOST = '10.0.0.2'  # Your server's IP address
PORT = 5001

def send_gnss_data(sock, latitude, longitude, altitude):
    gnss_data = {
        "latitude": latitude,
        "longitude": longitude,
        "altitude": altitude,
        "satellites": [
            {"svid": 5, "constellationType": 1, "cn0": 33.1, "doppler": -646.5695190429688, "pseudorangeRate": -646.5695190429688},
            {"svid": 16, "constellationType": 1, "cn0": 17.3, "doppler": 655.7139282226562, "pseudorangeRate": 655.7139282226562},
            {"svid": 10, "constellationType": 6, "cn0": 27.4, "doppler": -82.25444030761719, "pseudorangeRate": -82.25444030761719}
        ]
    }
    try:
        sock.sendall(json.dumps(gnss_data).encode('utf-8'))
        print("GNSS data sent")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            print("Connection established")
            # Send data points every second
            for _ in range(10):
                send_gnss_data(s, 32.2871859, 35.0780891, 243.59999084472656)
                time.sleep(1)

            # Send spoofed data points
            for _ in range(10):
                send_gnss_data(s, 40.730610, -73.935242, 10.0)  # New York coordinates for spoofing
                time.sleep(1)

    except ConnectionRefusedError:
        print("Connection refused. Please ensure the server is running.")
    except Exception as e:
        print(f"Error: {e}")
