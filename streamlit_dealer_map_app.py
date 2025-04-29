import streamlit as st
import pandas as pd
import geopandas as gpd
from streamlit_folium import st_folium
from load_dealers_map_1 import (
    load_dealer_data,
    assign_colors,
    merge_dealers_with_geo,
    generate_interactive_map_v3,
)

# Set page layout
st.set_page_config(layout="wide")
st.title("🗺️ Dealer Coverage Map – Uttar Pradesh")

# --- Hardcoded file paths ---
DEALER_EXCEL_PATH = "dealers.xlsx"
SHAPEFILE_PATH = "up_pincodes.geojson"  # Or .geojson if you have that

# --- Load data ---
try:
    df_dealers = load_dealer_data(DEALER_EXCEL_PATH)
    gdf_geo = gpd.read_file(SHAPEFILE_PATH)

    merged_gdf = merge_dealers_with_geo(df_dealers, gdf_geo)
    color_map = assign_colors(merged_gdf["DealerName"].unique())

    # Sidebar filters
    st.sidebar.header("🔍 Filters")
    district_filter = st.sidebar.multiselect("Select District(s)", sorted(merged_gdf["District"].unique()), default=None)
    dealer_filter = st.sidebar.multiselect("Select Dealer(s)", sorted(merged_gdf["DealerName"].unique()), default=None)

    filtered_gdf = merged_gdf.copy()
    if district_filter:
        filtered_gdf = filtered_gdf[filtered_gdf["District"].isin(district_filter)]
    if dealer_filter:
        filtered_gdf = filtered_gdf[filtered_gdf["DealerName"].isin(dealer_filter)]

    if filtered_gdf.empty:
        st.warning("⚠️ No data found for selected filters.")
    else:
        m = generate_interactive_map_v3(filtered_gdf, color_map)
        st_folium(m, width=1000, height=600)

except Exception as e:
    st.error(f"❌ Error: {e}")
