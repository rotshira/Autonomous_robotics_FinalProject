# GNSS Data Visualization Server

This project sets up a server to receive GNSS data, process it, and visualize it on a map using OpenStreetMap and Leaflet.js. The server listens for incoming GNSS data over a TCP connection, processes the data, and updates an HTML file to display the location on a map.

## Features

- Receives GNSS data over a TCP connection.
- Processes the received data to extract latitude and longitude.
- Updates an HTML file to visualize the location on a map using OpenStreetMap and Leaflet.js.
- Displays the received GNSS data in a formatted manner within the HTML file.

![image](https://github.com/rotshira/Autonomous_robotics_FinalProject/assets/92684730/02c5c61a-2d6b-473b-8728-86067c55adab)


## Requirements

- Python 3.x
- `socket` library (comes with the Python standard library)
- `json` library (comes with the Python standard library)
- Internet connection (for fetching map tiles from OpenStreetMap)

## Installation

1. Clone this repository to your local machine.
2. Navigate to the project directory.

## Usage

1. Start the server:
    ```sh
    python gnss_server.py
    ```

2. Send GNSS data to the server:
    - Use our application from : https://github.com/rotshira/RealTimeGNSS
      it will send GNSS data from you phone to the server!

## Example GNSS Data Format

The GNSS data should be sent in the following JSON format:
```json
[
    {
        "altitude": 763.7783203125,
        "cn0": 32.8,
        "latitude": 31.86001198,
        "x": 4432884.854755868,
        "doppler": 78.43905639648438,
        "y": 3123708.727690281,
        "z": 3347660.598760714,
        "pseudorangeRate": 78.43905639648438,
        "longitude": 35.1710988
    }
]




Enjoy🙂
