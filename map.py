import streamlit as st
import folium
from streamlit_folium import folium_static
import pandas as pd
import geopandas as gpd

# Setup
background_image = "https://drive.google.com/uc?export=view&id=1ULOlggWoTgSd6EQfhAMoK1m9NdrD6PLJ"

st.markdown(
    f"""
    <style>
        .stApp {{
            background-image: url({background_image});
            background-repeat: no-repeat;
            background-size: cover;
        }}
        .map-frame {{
            border: 25px solid #8B4513;
            border-radius: 15px;
            overflow: hidden;
        }}
        .leaflet-container {{
            box-shadow: 0 0 20px 20px white;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

# Load data
house_data = pd.read_csv("./data.csv")

# Load the saved boundary
kampala_gdf = gpd.read_file("kampala_boundary.geojson")

# Convert the boundary to coordinates
kampala_coords = kampala_gdf.geometry[0].exterior.coords.xy
kampala_coords = list(zip(kampala_coords[1], kampala_coords[0]))  # lat, lon format

# Function to generate map based on selected status
def generate_map(status):
    m = folium.Map(location=[0.3476, 32.5825], zoom_start=11)  # Centered on Kampala
    
    # Highlight Kampala
    folium.Polygon(
        locations=kampala_coords,
        fill=True,
        color='green',
        fill_opacity=0.1,
        weight=2
    ).add_to(m)
    
    for _, row in house_data.iterrows():
        color = None
        if row['HAS WIFI INTERNET'] == 'YES' and row['CONNECTED TO OPTICAL FIBRE(YES/NO)'] == 'YES':
            color = "green"
        elif row['HAS WIFI INTERNET'] == 'YES':
            color = "blue"
        elif row['CONNECTED TO OPTICAL FIBRE(YES/NO)'] == 'YES':
            color = "yellow"
        else:
            color = "red"
        
        if status == "All" or \
           (status == "Wi-Fi Only" and color == "blue") or \
           (status == "Optical Fiber Only" and color == "yellow") or \
           (status == "Both Wi-Fi and Optical Fiber" and color == "green") or \
           (status == "Neither" and color == "red"):
            folium.CircleMarker(
                location=[row['X'], row['Y']],
                radius=5,
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.6,
            ).add_to(m)
    return m

# User interface
st.title("Student Houses Internet Status in Uganda")
st.subheader("Based on Wi-Fi and Optical Fiber Connectivity")

selected_status = st.selectbox(
    "Select Internet Status",
    ["All", "Wi-Fi Only", "Optical Fiber Only", "Both Wi-Fi and Optical Fiber", "Neither"]
)

m = generate_map(selected_status)
folium_static(m)
