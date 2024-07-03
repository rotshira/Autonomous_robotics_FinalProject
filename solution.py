import numpy as np
import pyproj
import simplekml
from pykalman import KalmanFilter

WEEKSEC = 604800
LIGHTSPEED = 2.99792458e8


def convert_to_geodetic(x, y, z):
    transformer = pyproj.Transformer.from_crs("EPSG:4978", "EPSG:4326", always_xy=True)
    lon, lat, alt = transformer.transform(x, y, z)
    return lat, lon, alt


def filter_satellites(measurements):
    # Placeholder for satellite filtering logic
    # Filter satellites based on constellation, CN0, etc.
    return measurements


def detect_jamming(measurements):
    # Placeholder for jamming detection logic
    # Implement your algorithm to detect and handle jamming
    return measurements


def trilateration(sat_positions, measured_pr, initial_pos, initial_bias):
    position_corr = 100 * np.ones(3)
    clock_bias = initial_bias

    while np.linalg.norm(position_corr) > 1e-3:
        ranges = np.linalg.norm(sat_positions - initial_pos, axis=1)
        pred_pr = ranges + clock_bias
        residuals = measured_pr - pred_pr

        G = np.ones((measured_pr.size, 4))
        G[:, :3] = -(sat_positions - initial_pos) / ranges[:, None]
        corrections = np.linalg.inv(G.T @ G) @ G.T @ residuals

        position_corr, clock_bias_corr = corrections[:3], corrections[3]
        initial_pos += position_corr
        clock_bias += clock_bias_corr

    lat, lon, alt = convert_to_geodetic(*initial_pos)
    return initial_pos[0], initial_pos[1], initial_pos[2], lat, lon, alt


def calculate_locations_real_time(measurements):
    measurements = filter_satellites(measurements)
    measurements = detect_jamming(measurements)

    result_coords = {}
    for time, group in measurements.groupby('GPS time'):
        sat_pos = group[['Sat.X', 'Sat.Y', 'Sat.Z']].values
        measured_pr = group['Pseudo-Range'].values
        initial_pos = np.array([group['Sat.X'].mean(), group['Sat.Y'].mean(), group['Sat.Z'].mean()])
        initial_bias = 0

        coords = trilateration(sat_pos, measured_pr, initial_pos, initial_bias)
        result_coords[time] = coords

    return result_coords


def export_to_kml(coordinates, output_filepath):
    kml = simplekml.Kml()
    for time, (x, y, z, lat, lon, alt) in coordinates.items():
        pnt = kml.newpoint(name=str(time), coords=[(lon, lat, alt)])
        pnt.timestamp.when = time
    kml.save(output_filepath)
    print(f"KML file saved to: {output_filepath}")
