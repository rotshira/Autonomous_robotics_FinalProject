# GNSS Data Visualization Server

This project sets up a server to receive GNSS data, process it, and visualize it on a map using OpenStreetMap and Leaflet.js. The server listens for incoming GNSS data over a TCP connection, processes the data, and updates an HTML file to display the location on a map.

## Features

- Receives GNSS data over a TCP connection.
- Processes the received data to extract latitude and longitude.
- Updates an HTML file to visualize the location on a map using OpenStreetMap and Leaflet.js.
- Displays the received GNSS data in a formatted manner within the HTML file.


<img width="1379" alt="image" src="https://github.com/user-attachments/assets/c1d6abfc-884f-42d2-965f-889441f8313c">

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
    python webserver.py
    ```

2. Send GNSS data to the server:
    - Use our application from : https://github.com/rotshira/RealTimeGNSS
      it will send GNSS data from you phone to the server!
      Install it in your phone and give it location permission, set your network ip and your desired port and start to send data.
      <img width="200" height ="400" alt = "image" src = "https://github.com/user-attachments/assets/6a552ce4-5f0e-4b47-b5c4-5bb0babfd126">


## Example GNSS Data Format

The GNSS data should be sent in the following JSON format:
```json
[
{'satellites': [{'cn0': 20.3, 'constellationType': 1, 'carrierCycles': -9223372036854775808, 'svid': 5, 'accumulatedDeltaRangeState': 16, 'receivedSvTimeNanos': 416019336245364, 'pseudorangeRateUncertaintyMetersPerSecond': 5.930500030517578, 'accumulatedDeltaRangeMeters': 0.0, 'accumulatedDeltaRangeUncertaintyMeters': 0.0, 'snrInDb': 0.0, 'carrierFrequencyHz': 1575420030.0, 'receivedSvTimeUncertaintyNanos': 922, 'carrierPhaseUncertainty': 0.0, 'automaticGainControlLevelDb': -52.0, 'doppler': -96.6311264038086, 'multipathIndicator': 0, 'timeOffsetNanos': 0.0, 'carrierPhase': 0.0, 'state': 16399, 'pseudorangeRate': -96.6311264038086}, {'cn0': 33.4, 'constellationType': 1, 'carrierCycles': -9223372036854775808, 'svid': 13, 'accumulatedDeltaRangeState': 16, 'receivedSvTimeNanos': 416019335883656, 'pseudorangeRateUncertaintyMetersPerSecond': 0.20000000298023224, 'accumulatedDeltaRangeMeters': -0.0, 'accumulatedDeltaRangeUncertaintyMeters': 1902.917772949835, 'snrInDb': 0.0, 'carrierFrequencyHz': 1575420030.0, 'receivedSvTimeUncertaintyNanos': 16, 'carrierPhaseUncertainty': 0.0, 'automaticGainControlLevelDb': -52.0, 'doppler': -536.3464965820312, 'multipathIndicator': 0, 'timeOffsetNanos': 0.0, 'carrierPhase': 0.0, 'state': 16399, 'pseudorangeRate': -536.3464965820312}, {'cn0': 20.0, 'constellationType': 1, 'carrierCycles': -9223372036854775808, 'svid': 30, 'accumulatedDeltaRangeState': 16, 'receivedSvTimeNanos': 416019340754013, 'pseudorangeRateUncertaintyMetersPerSecond': 5.906500339508057, 'accumulatedDeltaRangeMeters': 0.0, 'accumulatedDeltaRangeUncertaintyMeters': 0.0, 'snrInDb': 0.0, 'carrierFrequencyHz': 1575420030.0, 'receivedSvTimeUncertaintyNanos': 922, 'carrierPhaseUncertainty': 0.0, 'automaticGainControlLevelDb': -52.0, 'doppler': 69.17174530029297, 'multipathIndicator': 0, 'timeOffsetNanos': 0.0, 'carrierPhase': 0.0, 'state': 16399, 'pseudorangeRate': 69.17174530029297}, {'cn0': 22.8, 'constellationType': 6, 'carrierCycles': -9223372036854775808, 'svid': 7, 'accumulatedDeltaRangeState': 16, 'receivedSvTimeNanos': 416019326258819, 'pseudorangeRateUncertaintyMetersPerSecond': 4.878500461578369, 'accumulatedDeltaRangeMeters': 0.0, 'accumulatedDeltaRangeUncertaintyMeters': 0.0, 'snrInDb': 0.0, 'carrierFrequencyHz': 1575420030.0, 'receivedSvTimeUncertaintyNanos': 61, 'carrierPhaseUncertainty': 0.0, 'automaticGainControlLevelDb': -55.0, 'doppler': -397.7803955078125, 'multipathIndicator': 0, 'timeOffsetNanos': 0.0, 'carrierPhase': 0.0, 'state': 23567, 'pseudorangeRate': -397.7803955078125}], 'altitude': 243.59999084472656, 'latitude': 32.2871894, 'longitude': 35.0780821}
]



