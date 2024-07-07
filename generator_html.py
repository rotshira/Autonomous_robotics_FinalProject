import socket
import json
from datetime import datetime

# Define constants and configurations
HOST = '192.168.43.53'  # Your server IP
PORT = 5001
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

# Start the server
def start_server():
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
                break  # Stop after processing the first set of data for now

        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            continue
        except Exception as e:
            print(f"Error processing data: {e}")

    connection.close()
    server_socket.close()

if __name__ == "__main__":
    start_server()
