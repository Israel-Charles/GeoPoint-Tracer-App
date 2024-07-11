# GeoPoint-Tracer-App
GeoPoint Tracer is a versatile application designed to handle geographical points, allowing users to add, edit, delete, and visualize these points on a map. The application supports both a graphical user interface (GUI) and a command-line interface (CLI), providing flexibility for different user preferences and scenarios.

### Features
- Add Points: Add geographical points by specifying latitude and longitude.
- Edit Points: Modify existing points.
- Delete Points: Remove points from the list.
- Clear Points: Clear all points from the list.
- Load Points: Load points from a JSON file.
- Save Map: Visualize the points on a map and save it as an HTML file.
- Export Points: Export the points to a JSON file.
- Map Views: Choose between different map views, such as OpenStreetMap and Google Satellite.

# How to Use
## Command-Line Interface (CLI)
### Requirements
- Python 3.x
- folium library

### Installation
Install the required library using pip:
`pip install folium`

### Running the CLI Version
#### With Input File:
```
python geo_point_cli.py inputfile.json
```
This command loads points from inputfile.json and then prompts you to select a map view or export the points as a JSON file.

#### Without Input File:
```
python geo_point_cli.py
```

This command allows you to manually enter geographical points. Enter latitude and longitude values, typing 'x' to stop entering points. Afterward, you can select a map view or export the points.

Options:

- 1: OpenStreetMap
- 2: Google Satellite
- e: Export points as JSON file
- q: Quit the program

## Graphical User Interface (GUI)
### Requirements
- Python 3.x
- tkinter (comes pre-installed with Python)
- folium library

### Installation
Install the required library using pip:
```
pip install folium
```

### Running the Application:
```
python geo_point_gui.py
```
This command opens the graphical user interface.

### Using the GUI:

Add Point: Enter latitude and longitude in the respective fields and click "Add Point".
Load Points: Click "Load Points from File" to select and load points from a JSON file.
Edit Point: Select a point from the list and click "Edit Point" or double-click a point to modify it.
Delete Point: Select a point from the list and click "Delete Point" to remove it.
Clear Points: Click "Clear All Points" to remove all points from the list.
Select Map View: Choose the desired map view from the dropdown menu.
Save Map: Click "Save Map" to save the map with the points to an HTML file.
Export Points: Click "Export Points as JSON" to save the points to a JSON file.

# Main Files
- geo_point_cli.py: Contains the CLI version of the GeoPoint Tracer application.
- geo_point_gui.py: Contains the GUI version of the GeoPoint Tracer application.

This dual-interface approach ensures that GeoPoint Tracer can be used efficiently in both graphical and terminal environments, making it a powerful tool for managing and visualizing geographical data.