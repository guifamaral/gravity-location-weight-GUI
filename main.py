from tkinter import *
from geopy.geocoders import Nominatim
import numpy as np
import folium
import webbrowser

def calculate_weight():
    # Retrieve the values entered by the user
    mass = float(mass_entry.get())
    ref1 = ref1_entry.get()
    ref2 = ref2_entry.get()

    # Convert reference names to coordinates using geopy
    geolocator = Nominatim(user_agent="loc_translator")
    location1 = geolocator.geocode(ref1)
    location2 = geolocator.geocode(ref2)
    coord1 = (location1.latitude, location1.longitude)
    coord2 = (location2.latitude, location2.longitude)
    
    # WGS84 ellipsoid model - semimajor axis m = a & semiminor axis m = b 
    a = 6378137 
    b = 6356752.3142  
    e2 = 1 - (b ** 2) / (a ** 2)
    # gravity at equator
    gamma = 9.80665  
    sin_lat1 = np.sin(np.deg2rad(coord1[0]))
    sin_lat2 = np.sin(np.deg2rad(coord2[0]))
    g1 = gamma * ((1 + 0.005279 * sin_lat1 ** 2 - 0.000023 * sin_lat1 ** 4) - 0.000003086 * location1.altitude)
    g2 = gamma * ((1 + 0.005279 * sin_lat2 ** 2 - 0.000023 * sin_lat2 ** 4) - 0.000003086 * location2.altitude)

    weight1 = mass * g1
    weight2 = mass * g2
    diff = weight1 - weight2  

    weight1_label.config(text=f"{ref1} > {weight1:.5f}")
    weight2_label.config(text=f"{ref2} > {weight2:.5f}")
    diff_label.config(text=f"The difference is > {diff:.5f}")
    display_map(coord1, coord2, ref1, ref2)

#GUI
root = Tk()
root.title("Weight Difference Calculator")

mass_label = Label(root, text="Mass (kg):")
mass_entry = Entry(root)
ref1_label = Label(root, text="From this place:")
ref1_entry = Entry(root)
ref2_label = Label(root, text="To this place:")
ref2_entry = Entry(root)

calculate_button = Button(root, text="Calculate", command=calculate_weight)

weight1_label = Label(root, text="")
weight2_label = Label(root, text="")
diff_label = Label(root, text="")

# packs
mass_label.pack()
mass_entry.pack()
ref1_label.pack()
ref1_entry.pack()
ref2_label.pack()
ref2_entry.pack()

calculate_button.pack()
weight1_label.pack()
weight2_label.pack()
diff_label.pack()

def display_map(coord1, coord2, ref1, ref2):
    my_map = folium.Map(location=coord1, zoom_start=3)
    folium.Marker(location = coord1, popup=ref1).add_to(my_map)
    folium.Marker(location = coord2, popup=ref2).add_to(my_map)
    my_map.save('map.html')
    webbrowser.open('map.html')

map_button = Button(root, text="Display Map", command=display_map)
map_button.pack()

root.mainloop()
