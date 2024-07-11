import socket
import json
from collections import deque
from datetime import datetime

# Define constants and configurations
HOST = '10.0.0.2'  # Your server's IP address
PORT = 5001
HTML_FILE = 'gnss_location.html'  # Use a constant file name for updating

# GNSS data sliding window size
WINDOW_SIZE = 5
gnss_data_window = deque(maxlen=WINDOW_SIZE)

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
        <meta http-equiv="refresh" content="5">
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

# Function to detect spoofing
def detect_spoofing(gnss_data_window):
    cn0_threshold = 30.0  # CN0 threshold for valid signals
    doppler_change_threshold = 1000  # Doppler change threshold
    max_distance_change = 100.0  # Maximum allowed change in distance in meters

    # Aggregate data from the sliding window
    all_satellites = [sat for data in gnss_data_window for sat in data['satellites']]
    last_location = gnss_data_window[-1]
    first_location = gnss_data_window[0]

    # Track the average CN0 and sudden Doppler changes
    cn0_values = [sat['cn0'] for sat in all_satellites if 'cn0' in sat]
    doppler_values = [sat['doppler'] for sat in all_satellites if 'doppler' in sat]

    if not cn0_values or not doppler_values:
        return False  # Not enough data to detect spoofing

    average_cn0 = sum(cn0_values) / len(cn0_values)
    max_doppler_change = max(doppler_values) - min(doppler_values)

    # Calculate distance change
    distance_change = haversine(first_location['latitude'], first_location['longitude'],
                                last_location['latitude'], last_location['longitude'])

    if average_cn0 < cn0_threshold or max_doppler_change > doppler_change_threshold or distance_change > max_distance_change:
        return True

    return False

# Function to filter satellites by constellation and signal strength
def filter_satellites(data, constellation=None, cn0_threshold=None):
    if constellation:
        data = [d for d in data if d.get('constellationType') == constellation]
    if cn0_threshold:
        data = [d for d in data if d.get('cn0', 0) >= cn0_threshold]
    return data

# Function to process incoming GNSS data
def process_gnss_data(data):
    if isinstance(data, dict):
        data = [data]

    # Filter satellites (example: only GPS constellation and CN0 > 30)
    for entry in data:
        entry['satellites'] = filter_satellites(entry['satellites'], constellation=1, cn0_threshold=30)

    return data

# Calculate the Haversine distance between two points in meters
def haversine(lat1, lon1, lat2, lon2):
    from math import radians, sin, cos, sqrt, atan2

    R = 6371000  # Radius of the Earth in meters
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

# Start the server
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    print(f"Server started and listening on {HOST}:{PORT}")

    while True:
        print("Waiting for connection...")
        connection, address = server_socket.accept()
        print(f"Connection established with {address}")

        buffer = ''
        while True:
            try:
                data = connection.recv(4096)
                if not data:
                    break

                data = data.decode('utf-8')
                print(f"Received data: {data}")
                buffer += data

                # Attempt to process complete JSON objects from the buffer
                while True:
                    try:
                        gnss_data, index = json.JSONDecoder().raw_decode(buffer)
                        buffer = buffer[index:].strip()

                        if isinstance(gnss_data, dict):
                            gnss_data = [gnss_data]

                        print(f"Parsed GNSS data: {gnss_data}")

                        # Process the data and update the sliding window
                        processed_data = process_gnss_data(gnss_data)
                        for location in processed_data:
                            gnss_data_window.append(location)

                        # Focus on the first valid data point for simplicity
                        for location in gnss_data:
                            print(f"Processing location data: {location}")
                            latitude = location.get('latitude', None)
                            longitude = location.get('longitude', None)
                            print(f"Extracted coordinates: Latitude={latitude}, Longitude={longitude}")

                            if latitude is not None and longitude is not None and latitude != 0.0 and longitude != 0.0:
                                generate_or_update_html(latitude, longitude, location)
                                break  # Only process the first valid location for now

                        # Check for spoofing
                        if len(gnss_data_window) == WINDOW_SIZE:
                            if detect_spoofing(gnss_data_window):
                                print("Spoofing detected! Data might be unreliable.")
                            else:
                                print("No spoofing detected.")
                        break  # Stop after processing the first set of data for now

                    except json.JSONDecodeError:
                        # If JSONDecodeError occurs, break the loop and wait for more data
                        break

            except Exception as e:
                print(f"Error receiving data: {e}")
                break

        connection.close()
        print("Connection closed.")
        break

if __name__ == "__main__":
    start_server()
