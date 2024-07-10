import socket
import json
from datetime import datetime, timedelta
from collections import deque

# Define constants and configurations
HOST = '0.0.0.0'  # Listen on all available interfaces
PORT = 5002
HTML_FILE = 'gnss_location.html'  # Use a constant file name for updating
SPOOFING_DETECTION_DELAY = timedelta(seconds=30)  # Delay spoofing detection for 30 seconds
WINDOW_SIZE = 5  # Number of data points to consider for spoofing detection

# Variables to track time and data
start_time = datetime.now()
gnss_data_window = deque(maxlen=WINDOW_SIZE)  # Sliding window to store GNSS data points

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

# Function to detect GNSS spoofing based on sliding window data
def detect_spoofing(gnss_data_window):
    cn0_threshold = 30.0  # CN0 threshold for valid signals
    doppler_change_threshold = 1000  # Doppler change threshold

    # Aggregate data from the sliding window
    all_satellites = [sat for data in gnss_data_window for sat in data['satellites']]

    # Track the average CN0 and sudden Doppler changes
    cn0_values = [sat['cn0'] for sat in all_satellites if 'cn0' in sat]
    doppler_values = [sat['doppler'] for sat in all_satellites if 'doppler' in sat]

    if not cn0_values or not doppler_values:
        return False  # Not enough data to detect spoofing

    average_cn0 = sum(cn0_values) / len(cn0_values)
    max_doppler_change = max(doppler_values) - min(doppler_values)

    if average_cn0 < cn0_threshold or max_doppler_change > doppler_change_threshold:
        return True

    return False

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

                for location in gnss_data:
                    print(f"Processing location data: {location}")
                    latitude = location.get('latitude', None)
                    longitude = location.get('longitude', None)
                    satellites = location.get('satellites', [])

                    print(f"Extracted coordinates: Latitude={latitude}, Longitude={longitude}")

                    if latitude is not None and longitude is not None:
                        generate_or_update_html(latitude, longitude, location)
                        gnss_data_window.append(location)  # Add data to sliding window

                        if datetime.now() - start_time > SPOOFING_DETECTION_DELAY:
                            if detect_spoofing(gnss_data_window):
                                print("Spoofing detected! Data might be unreliable.")
                            else:
                                print("No spoofing detected.")
                        break  # Only process the first valid location for now

        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            continue
        except Exception as e:
            print(f"Error processing data: {e}")

    connection.close()
    server_socket.close()

if __name__ == "__main__":
    start_server()
