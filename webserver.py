import socket
import json
import time
from datetime import datetime, timedelta

# Define constants and configurations
HOST = '10.0.0.2'  # Your server IP
PORT = 5002
HTML_FILE = 'gnss_location.html'  # Use a constant file name for updating


# Function to generate or update HTML using OpenStreetMap and Leaflet.js
def generate_or_update_html(latitude, longitude, location_data):
    print(f"Updating HTML for coordinates: Latitude={latitude}, Longitude={longitude}")
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>GNSS Location</title>
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css" />
        <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script>
        <style>
            #map {{
                height: 500px;
                width: 100%;
            }}
        </style>
    </head>
    <body>
        <h1>GNSS Location</h1>
        <div id="map"></div>
        <script>
            var map = L.map('map').setView([{latitude}, {longitude}], 15);
            L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
                maxZoom: 19,
                attribution: '© OpenStreetMap contributors'
            }}).addTo(map);
            var marker = L.marker([{latitude}, {longitude}]).addTo(map);
        </script>
        <h2>Received GNSS Data</h2>
        <pre>{json.dumps(location_data, indent=4)}</pre>
    </body>
    </html>
    """

    with open(HTML_FILE, 'w') as file:
        file.write(html_content)
    print(f"HTML file updated with the location data at {HTML_FILE}.")


# Function to detect spoofing based on location data
def detect_spoofing(data):
    known_good_location = (31.86001198, 35.1710988)  # Replace with your actual coordinates
    latitude = data.get('latitude', None)
    longitude = data.get('longitude', None)

    if latitude is not None and longitude is not None:
        distance = ((latitude - known_good_location[0]) ** 2 + (longitude - known_good_location[1]) ** 2) ** 0.5
        if distance > 0.001:  # Threshold distance for spoofing detection
            print("Spoofing detected! Data might be unreliable.")
        else:
            print("No spoofing detected.")
    else:
        print("Insufficient data for spoofing detection.")


# Start the server
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    print("Waiting for connection...")

    connection, address = server_socket.accept()
    print(f"Connection established with {address}")

    start_time = datetime.now()
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
                    gnss_data = [gnss_data]

                print(f"Received data: {gnss_data}")

                # Focus on the first valid data point for simplicity
                for location in gnss_data:
                    print(f"Processing location data: {location}")
                    latitude = location.get('latitude', None)
                    longitude = location.get('longitude', None)
                    print(f"Extracted coordinates: Latitude={latitude}, Longitude={longitude}")

                    if latitude is not None and longitude is not None and latitude != 0.0 and longitude != 0.0:
                        generate_or_update_html(latitude, longitude, location)
                        break  # Only process the first valid location for now

                # Check for spoofing only after 30 seconds
                if datetime.now() - start_time > timedelta(seconds=30):
                    detect_spoofing(gnss_data[0])

        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            continue
        except Exception as e:
            print(f"Error processing data: {e}")

    connection.close()
    server_socket.close()


if __name__ == "__main__":
    start_server()
