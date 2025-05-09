from tkinter import *
import ttkthemes
from tkinter import ttk, messagebox
import tkinter as tk
from tkintermapview import TkinterMapView
import random
import math
from PIL import Image, ImageTk



# === Simulated device storage ===
devices = {}

# === Geofencing Settings ===
SAFE_ZONE_LAT = 14.418047877227954
SAFE_ZONE_LON = 121.04582230803875
SAFE_AREA_SQM = 500
SAFE_RADIUS_METERS = math.sqrt(SAFE_AREA_SQM / math.pi)


# === Hardware GPS setup (commented for now) ===
"""
from gps import gps, WATCH_ENABLE
gpsd = gps(mode=WATCH_ENABLE)

def read_gps_coordinates():
    gpsd.next()
    if gpsd.fix.latitude != 0 and gpsd.fix.longitude != 0:
        return gpsd.fix.latitude, gpsd.fix.longitude
    else:
        return None
"""

# === Helper Functions ===
def random_coordinates():
    # Simulate small movement near Alabang safe zone
    lat = random.uniform(14.4178, 14.4182)
    lon = random.uniform(121.0456, 121.0460)
    return lat, lon


def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371000
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = (math.sin(delta_phi/2)**2 +
         math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda/2)**2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c
def register_device():
    global device_counter
    name = petNameEntry.get().strip()
    species = typeSpeciesEntry.get().strip()
    remarks = remarksEntry.get().strip()

    if not name or name in devices:
        messagebox.showwarning("Warning", "Invalid or duplicate Pet Name!")
        return

    # === Demo only
    lat, lon = random_coordinates()

    # === Real hardware
    """
    gps_data = read_gps_coordinates()
    if gps_data:
        lat, lon = gps_data
    else:
        messagebox.showerror("Error", "No GPS Signal!")
        return
    """

    marker = map_widget.set_marker(lat, lon, text=name)
    devices[name] = {'lat': lat, 'lon': lon, 'marker': marker, 'inside': True}

    tree.insert('', 'end', values=(device_counter, name, species, remarks))
    device_counter += 1

    petNameEntry.delete(0, tk.END)
    typeSpeciesEntry.delete(0, tk.END)
    remarksEntry.delete(0, tk.END)

    update_device_list()

def update_device_list():
    device_list.delete(0, tk.END)
    for name in devices:
        lat = devices[name]['lat']
        lon = devices[name]['lon']
        device_list.insert(tk.END, f"{name}: {lat:.4f}, {lon:.4f}")
def update_locations():
    for name, info in devices.items():
        # === Demo only
        lat, lon = random_coordinates()

        # === Real hardware (uncomment below)
        """
        gps_data = read_gps_coordinates()
        if gps_data:
            lat, lon = gps_data
        """

        info['lat'] = lat
        info['lon'] = lon
        info['marker'].set_position(lat, lon)

        distance = haversine_distance(lat, lon, SAFE_ZONE_LAT, SAFE_ZONE_LON)
        is_inside = distance <= SAFE_RADIUS_METERS

        if not is_inside and info['inside']:
            info['marker'].set_text(f"{name} 🚨")
            messagebox.showwarning("Warning", f"{name} has LEFT the safe zone!")
            info['inside'] = False
        elif is_inside and not info['inside']:
            info['marker'].set_text(name)
            info['inside'] = True

    update_device_list()
    root.after(5000, update_locations)

def on_tree_double_click(event):
    region = tree.identify("region", event.x, event.y)
    if region != "cell":
        return

    column = tree.identify_column(event.x)
    row = tree.identify_row(event.y)
    if not row:
        return

    x, y, width, height = tree.bbox(row, column)
    value = tree.set(row, column)

    entry = tk.Entry(tree)
    entry.place(x=x, y=y, width=width, height=height)
    entry.insert(0, value)
    entry.focus()

    def on_entry_confirm(event=None):
        new_value = entry.get()
        tree.set(row, column, new_value)
        entry.destroy()

    entry.bind("<Return>", on_entry_confirm)
    entry.bind("<FocusOut>", on_entry_confirm)



root=ttkthemes.ThemedTk()
root.get_themes()
root.set_theme('breeze')
root.geometry('1300x1000+10+10')
root.resizable(0,0)
root.title("🐾 GPS Tracker")



background_image = Image.open(r'C:\Users\Administrator\Desktop\Codes\GpsTracker\background.jpg')
background_photo = ImageTk.PhotoImage(background_image)

background_label = tk.Label(root, image=background_photo,width=1300,height=1000)
background_label.place(x=0,y=0)





#petinfoFrame = Frame(root,width=300,height=300)
#petinfoFrame.place(x=90,y=250)



# Title
#title=ttk.Label(root, text="Multi-Pet GPS Tracker", font=("Helvetica", 18, "bold"))
#title.place(x=50,y=50)



petName = ttk.Label(root,text='Animal Name      : ', font=('arial',11,'bold'),background='white')
petName.place(x=122,y=375)
petNameEntry = ttk.Entry(root,font=('arial',12,'italic'),width=20)
petNameEntry.place(x=245,y=375)


typeSpecies = ttk.Label(root,text='Type of Species: ', font=('arial',11,'bold'),background='white')
typeSpecies.place(x=122,y=420)
typeSpeciesEntry = ttk.Entry(root,font=('arial',13,'italic'),width=20)
typeSpeciesEntry.place(x=245,y=420)


remarks = ttk.Label(root,text='Remarks           : ', font=('arial',12,'bold'),background='white')
remarks.place(x=122,y=465)
remarksEntry = ttk.Entry(root,font=('arial',13,'italic'),width=20)
remarksEntry.place(x=245,y=465)



submitButton = ttk.Button(root,text='SUBMIT',width=30, command=register_device)
submitButton.place(x=185,y=530 )


# Treeview Area
tree_frame = ttk.Frame(root)
tree_frame.place(x=30,y=680)

columns = ("ID", "Pet Name", "Species", "Remarks")
tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=10)
tree.pack(side="left", fill="x", expand=True)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=120)

scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
scrollbar.pack(side="right", fill="y")
tree.configure(yscrollcommand=scrollbar.set)

#tree.bind("<Double-1>", on_tree_double_click)


# Device list
device_list = tk.Listbox(root, height=8,width=100)
device_list.place(x=550,y=760)


# Map
map_widget = TkinterMapView(root, width=610, height=480, corner_radius=8)
map_widget.place(x=550,y=230)
map_widget.set_position(SAFE_ZONE_LAT, SAFE_ZONE_LON)
map_widget.set_zoom(20)

# === Draw simulated circle ===
def draw_safe_zone_circle(center_lat, center_lon, radius_meters):
    points = []
    steps = 36  # more steps = smoother circle
    for angle in range(0, 360, int(360/steps)):
        bearing = math.radians(angle)
        lat = center_lat + (radius_meters/111320) * math.cos(bearing)
        lon = center_lon + (radius_meters/(111320*math.cos(math.radians(center_lat)))) * math.sin(bearing)
        points.append((lat, lon))
    map_widget.set_path(points, color="green", width=2)

draw_safe_zone_circle(SAFE_ZONE_LAT, SAFE_ZONE_LON, SAFE_RADIUS_METERS)

# Global counter for ID
device_counter = 1







update_locations()
root.mainloop()