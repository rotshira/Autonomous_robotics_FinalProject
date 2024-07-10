import socket
import json
import time

HOST = '10.0.0.2'  # Your server IP
PORT = 5001


def send_gnss_data(latitude, longitude, altitude):
    data = {
        "latitude": latitude,
        "longitude": longitude,
        "altitude": altitude,
        "satellites": [
            {
                "svid": 1,
                "constellationType": 1,
                "cn0": 45.5,
                "doppler": 123.4,
                "pseudorangeRate": -0.5
            }
        ]
    }
    json_data = json.dumps(data)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(json_data.encode('utf-8'))


if __name__ == "__main__":
    # Send normal GNSS data
    send_gnss_data(31.86001198, 35.1710988, 763.7783203125)
    time.sleep(2)

    # Send spoofed GNSS data
    send_gnss_data(40.73061, -73.935242, 10.0)  # New York coordinates for spoofing
    time.sleep(2)

    # Send normal GNSS data again
    send_gnss_data(31.86001198, 35.1710988, 763.7783203125)
