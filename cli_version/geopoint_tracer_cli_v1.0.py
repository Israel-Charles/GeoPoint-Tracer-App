import sys
import json
import folium
import argparse

class GeoPointCLI:
    def __init__(self, points=None):
        self.points = points if points is not None else []

        # Map view options
        self.map_views = {
            "1": ("OpenStreetMap", "openstreetmap"),
            "2": ("Google Satellite", "https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}")
        }

    def add_point(self, lat, lon):
        """Add a geographical point to the list."""
        try:
            lat = float(lat)
            lon = float(lon)
            self.points.append((lat, lon))
            print(f"Added point: Lat: {lat}, Lon: {lon}")
        except ValueError:
            print("Invalid input. Please enter valid latitude and longitude values.")

    def load_points_from_file(self, file_path):
        """Load geographical points from a JSON file."""
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                self.extract_points(data)
            print(f"Loaded points from {file_path}")
        except Exception as e:
            print(f"Failed to load points: {e}")

    def extract_points(self, data):
        """Extract geographical points from JSON data."""
        if isinstance(data, dict):
            if "lat" in data and "lon" in data:
                try:
                    lat = float(data["lat"])
                    lon = float(data["lon"])
                    self.points.append((lat, lon))
                    print(f"Added point from file: Lat: {lat}, Lon: {lon}")
                except ValueError:
                    pass
            else:
                for key, value in data.items():
                    self.extract_points(value)
        elif isinstance(data, list):
            for item in data:
                self.extract_points(item)

    def save_map(self, map_view):
        """Save the map with the traced points to an HTML file."""
        if not self.points:
            print("No points to save.")
            return

        file_path = input("Enter the file name to save the map (e.g., map.html): ")
        map_view_name, map_view_url = self.map_views[map_view]

        m = folium.Map()
        folium.TileLayer(tiles=map_view_url, attr='Google' if "google" in map_view_url else '', name=map_view_name, overlay=True, control=True).add_to(m)

        for point in self.points:
            folium.Marker(location=point).add_to(m)

        folium.PolyLine(self.points, color="blue", weight=2.5, opacity=1).add_to(m)
        m.fit_bounds(self.points)
        m.save(file_path)
        print(f"Map saved to {file_path}")

    def export_points_as_json(self):
        """Export geographical points to a JSON file."""
        if not self.points:
            print("No points to export.")
            return

        file_path = input("Enter the file name to save points (e.g., points.json): ")
        points_dict = [{"lat": lat, "lon": lon} for lat, lon in self.points]
        with open(file_path, 'w') as file:
            json.dump(points_dict, file, indent=4)

        print(f"Points exported to {file_path}")

def main():
    parser = argparse.ArgumentParser(description="GeoPoint CLI")
    parser.add_argument("inputfile", nargs="?", help="Input file with geographical points")

    args = parser.parse_args()

    geo_app = GeoPointCLI()

    if args.inputfile:
        geo_app.load_points_from_file(args.inputfile)
    else:
        print("Enter geographical points (latitude and longitude). Type 'x' to stop.")
        while True:
            lat = input("Enter latitude (or 'x' to stop): ")
            if lat.lower() == 'x':
                break
            lon = input("Enter longitude: ")
            geo_app.add_point(lat, lon)

    while True:
        print("\nOptions:")
        print("1. OpenStreetMap")
        print("2. Google Satellite")
        print("e. Export points as JSON")
        print("q. Quit")
        option = input("Select an option: ")

        if option == 'q':
            break
        elif option == 'e':
            geo_app.export_points_as_json()
        elif option in geo_app.map_views:
            geo_app.save_map(option)
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
