import streamlit as st
import folium
from streamlit_folium import folium_static
import pandas as pd

background_image = "https://raw.githubusercontent.com/lamberlin/Southshore/main/pic.jpg"

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

house_data = pd.read_csv("./data.csv")
house_data['X'] = house_data['X'].astype(float)
house_data['Y'] = house_data['Y'].astype(float)
house_data.dropna(subset=['X', 'Y'], inplace=True)

# Initialize the map
m = folium.Map(location=[house_data['X'].mean(), house_data['Y'].mean()], zoom_start=10)

# Display the legend directly using Streamlit outside of the map


# Iterate through the rows to create the CircleMarkers
for _, row in house_data.iterrows():
    if row['HAS WIFI INTERNET'] == 'YES' and row['CONNECTED TO OPTICAL FIBRE(YES/NO)'] == 'YES':
        color = "green"
    elif row['HAS WIFI INTERNET'] == 'YES':
        color = "blue"
    elif row['CONNECTED TO OPTICAL FIBRE(YES/NO)'] == 'YES':
        color = "yellow"
    else:
        color = "red"

    # Generate the popup content with other variables and a link to Google Maps search
    popup_content = f"""
    Address: {row['PHYSICAL LOCATION']}<br>
    Wi-Fi: {row['HAS WIFI INTERNET']}<br>
    Fiber: {row['CONNECTED TO OPTICAL FIBRE(YES/NO)']}<br>
    Service provider: {row['SERVICE PROVIDER']}<br>
    <a href="{row['URL GOOGLE MAPS']}" target="_blank">View on Google Maps</a>
    """

    folium.CircleMarker(
        location=[row['X'], row['Y']],
        radius=5,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.6,
        popup=folium.Popup(popup_content, max_width=300)
    ).add_to(m)

legend_html = """
<div style="position: fixed; bottom: 10px; right: 10px; z-index: 9999; background-color: rgba(255, 255, 255, 0.8); padding: 10px; border-radius: 5px;">
<p><span style="color:red; font-size:25px; margin-right:10px;">●</span>None</p>
<p><span style="color:blue; font-size:25px; margin-right:10px;">●</span>Wi-Fi Only</p>
<p><span style="color:yellow; font-size:25px; margin-right:10px;">●</span>Fiber Only</p>
<p><span style="color:green; font-size:25px; margin-right:10px;">●</span>Wi-Fi + Fiber</p>
</div>
"""

# Attach the legend to the map
legend = folium.Element(legend_html)
m.get_root().html.add_child(legend)
st.title("Student Houses Internet Status in Kampala")
st.subheader("Based on Wi-Fi and Optical Fiber Connectivity")
st.subheader("created by Martin,Ole, Lambert")
col1, col2 = st.columns(2)

# Display the map in the first column
with col1:
    folium_static(m)

# Display the legend in the second column
with col2:
    st.markdown(legend_html, unsafe_allow_html=True)
