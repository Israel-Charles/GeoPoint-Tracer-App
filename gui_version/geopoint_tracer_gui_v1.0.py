import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import folium
import json
import csv

class GeoPointApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GeoPoint Tracer App")

        self.points = []  # List to store geographical points

        self.map_views = {
            "OpenStreetMap": "openstreetmap",
            "Google Satellite": "https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}"
        }

        self.init_gui()

    def init_gui(self):
        """Initialize the GUI layout."""
        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=10)

        self.lat_label = tk.Label(self.frame, text="Latitude:")
        self.lat_label.grid(row=0, column=0)
        self.lat_entry = tk.Entry(self.frame)
        self.lat_entry.grid(row=0, column=1)

        self.lon_label = tk.Label(self.frame, text="Longitude:")
        self.lon_label.grid(row=1, column=0)
        self.lon_entry = tk.Entry(self.frame)
        self.lon_entry.grid(row=1, column=1)

        self.add_button = tk.Button(self.frame, text="Add Point", command=lambda: self.add_point())
        self.add_button.grid(row=2, column=0, columnspan=2, pady=5)

        self.load_button = tk.Button(self.frame, text="Load Points from File", command=self.load_points_from_file)
        self.load_button.grid(row=3, column=0, columnspan=2, pady=5)

        self.points_listbox = tk.Listbox(self.root, width=50, selectmode=tk.SINGLE)
        self.points_listbox.pack(pady=10)
        self.points_listbox.bind('<Double-1>', self.edit_point)

        self.actions_frame = tk.Frame(self.root)
        self.actions_frame.pack(pady=10)

        self.edit_button = tk.Button(self.actions_frame, text="Edit Point", command=self.edit_point)
        self.edit_button.grid(row=0, column=0, padx=5)

        self.delete_button = tk.Button(self.actions_frame, text="Delete Point", command=self.delete_point)
        self.delete_button.grid(row=0, column=1, padx=5)

        self.clear_button = tk.Button(self.actions_frame, text="Clear All Points", command=self.clear_points)
        self.clear_button.grid(row=0, column=2, padx=5)

        self.export_json_button = tk.Button(self.root, text="Export Points as JSON", command=self.export_points_as_json)
        self.export_json_button.pack(pady=5)

        self.export_txt_button = tk.Button(self.root, text="Export Points as Text", command=self.export_points_as_txt)
        self.export_txt_button.pack(pady=5)

        self.map_view_label = tk.Label(self.root, text="Select Map View:")
        self.map_view_label.pack()

        self.map_view_var = tk.StringVar(value="OpenStreetMap")
        self.map_view_menu = tk.OptionMenu(self.root, self.map_view_var, *self.map_views.keys())
        self.map_view_menu.pack(pady=5)

        self.save_button = tk.Button(self.root, text="Save Map", command=self.save_map)
        self.save_button.pack(pady=5)

    def add_point(self, lat=None, lon=None):
        try:
            lat = float(lat) if lat is not None else float(self.lat_entry.get())
            lon = float(lon) if lon is not None else float(self.lon_entry.get())
            self.points.append((lat, lon))
            self.points_listbox.insert(tk.END, f"{lat}, {lon}")
            self.lat_entry.delete(0, tk.END)
            self.lon_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter valid latitude and longitude values")

    def load_points_from_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("All Files", "*.*"), ("JSON Files", "*.json"), ("Text Files", "*.txt")])
        if file_path:
            if file_path.lower().endswith('.json'):
                try:
                    with open(file_path, 'r') as file:
                        data = json.load(file)
                        self.extract_points(data)
                    print(f"Loaded points from {file_path}")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to load points: {e}")
            elif file_path.lower().endswith('.txt'):
                try:
                    with open(file_path, 'r') as file:
                        reader = csv.reader(file)
                        for row in reader:
                            if len(row) == 2:
                                self.add_point(row[0].strip(), row[1].strip())
                    print(f"Loaded points from {file_path}")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to load points: {e}")

    def extract_points(self, data):
        if isinstance(data, dict):
            if "lat" in data and "lon" in data:
                self.add_point(data["lat"], data["lon"])
            else:
                for value in data.values():
                    self.extract_points(value)
        elif isinstance(data, list):
            for item in data:
                self.extract_points(item)

    def save_map(self):
        """Save the map with the traced points to an HTML file."""
        if not self.points:
            messagebox.showwarning("No points", "Please add some points before saving the map")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".html", filetypes=[("HTML files", "*.html")])
        if not file_path:
            return

        map_view = self.map_views[self.map_view_var.get()]
        m = folium.Map()
        folium.TileLayer(tiles=map_view, attr='Google' if "google" in map_view else '', name=self.map_view_var.get(), overlay=True, control=True).add_to(m)

        for point in self.points:
            folium.Marker(location=point).add_to(m)
        
        folium.PolyLine(self.points, color="blue", weight=2.5, opacity=1).add_to(m)
        m.fit_bounds(self.points)
        m.save(file_path)
        messagebox.showinfo("Map saved", f"Map has been saved to {file_path}")

    def edit_point(self):
        selected_index = self.points_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("No selection", "Please select a point to edit")
            return
        selected_index = selected_index[0]
        lat, lon = self.points[selected_index]
        new_lat = simpledialog.askfloat("Edit Latitude", "Enter new latitude:", initialvalue=lat)
        new_lon = simpledialog.askfloat("Edit Longitude", "Enter new longitude:", initialvalue=lon)
        if new_lat is not None and new_lon is not None:
            self.points[selected_index] = (new_lat, new_lon)
            self.points_listbox.delete(selected_index)
            self.points_listbox.insert(selected_index, f"{new_lat}, {new_lon}")

    def delete_point(self):
        selected_index = self.points_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("No selection", "Please select a point to delete")
            return
        selected_index = selected_index[0]
        self.points.pop(selected_index)
        self.points_listbox.delete(selected_index)

    def clear_points(self):
        self.points.clear()
        self.points_listbox.delete(0, tk.END)

    def export_points_as_json(self):
        if not self.points:
            messagebox.showerror("No points", "Please add some points before exporting")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
        if not file_path:
            return
        with open(file_path, 'w') as file:
            json.dump([{"lat": lat, "lon": lon} for lat, lon in self.points], file, indent=4)
        messagebox.showinfo("Export Successful", f"Points have been exported to {file_path}")

    def export_points_as_txt(self):
        if not self.points:
            messagebox.showerror("No points", "Please add some points before exporting")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if not file_path:
            return
        with open(file_path, 'w') as file:
            for lat, lon in self.points:
                file.write(f"{lat}, {lon}\n")
        messagebox.showinfo("Export Successful", f"Points have been exported to {file_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = GeoPointApp(root)
    root.mainloop()
