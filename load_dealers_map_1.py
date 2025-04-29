
# dealer_map_loader.py
import pandas as pd
import geopandas as gpd
import folium
import random
from folium.features import GeoJsonTooltip


def load_dealer_data(file_path):
    df_raw = pd.read_excel(file_path)
    df = df_raw.rename(columns={
        "Distrcit": "District",
        "Pin code": "Pincode",
        "Dealer Name": "DealerName",
        "Number tag for dealer": "DealerID"
    })
    df = df.dropna(subset=["District", "Pincode"], how='all')
    df["Pincode"] = df["Pincode"].dropna().astype(int).astype(str).str.zfill(6)
    return df


def load_pincode_geojson(geojson_path):
    return gpd.read_file(geojson_path)


def assign_colors(dealer_names):
    random.seed(42)
    return {dealer: f"#{random.randint(0, 0xFFFFFF):06x}" for dealer in dealer_names}


def merge_dealers_with_geo(dealers_df, geo_df):
    dealers_df = dealers_df.dropna(subset=["District"])
    dealers_df["District"] = dealers_df["District"].str.strip().str.title()
    geo_df["Name"] = geo_df["Name"].str.strip().str.title()
    return geo_df.merge(dealers_df, left_on='Name', right_on='District')


def generate_interactive_map(merged_gdf, color_map):
    m = folium.Map(location=[26.85, 80.95], zoom_start=7, tiles='CartoDB positron')

    for dealer in merged_gdf["DealerName"].unique():
        dealer_gdf = merged_gdf[merged_gdf["DealerName"] == dealer]
        color = color_map.get(dealer, "#000000")
        folium.GeoJson(
            dealer_gdf,
            style_function=lambda x, clr=color: {
                "fillColor": clr,
                "color": clr,
                "weight": 1,
                "fillOpacity": 0.4
            },
            tooltip=GeoJsonTooltip(fields=["DealerName", "Pincode"])
        ).add_to(m)

    return m

from folium import FeatureGroup, LayerControl

def generate_interactive_map_v2(merged_gdf, color_map):
    m = folium.Map(location=[26.85, 80.95], zoom_start=7, tiles='CartoDB positron')

    for dealer in merged_gdf["DealerName"].unique():
        dealer_gdf = merged_gdf[merged_gdf["DealerName"] == dealer]
        color = color_map.get(dealer, "#000000")

        dealer_group = FeatureGroup(name=f"Dealer: {dealer}", show=True)

        for _, row in dealer_gdf.iterrows():
            folium.GeoJson(
                row["geometry"],
                style_function=lambda x, clr=color: {
                    "fillColor": clr,
                    "color": clr,
                    "weight": 1,
                    "fillOpacity": 0.5,
                },
                tooltip=folium.GeoJsonTooltip(fields=["DealerName", "Pincode", "District"])
            ).add_to(dealer_group)

        dealer_group.add_to(m)

    LayerControl(collapsed=False).add_to(m)
    return m

from folium import FeatureGroup, LayerControl
from folium.features import GeoJsonTooltip

def generate_interactive_map_v3(merged_gdf, color_map):
    m = folium.Map(location=[26.85, 80.95], zoom_start=7, tiles='CartoDB positron')

    for dealer in merged_gdf["DealerName"].unique():
        dealer_gdf = merged_gdf[merged_gdf["DealerName"] == dealer]
        color = color_map.get(dealer, "#000000")

        dealer_group = FeatureGroup(name=f"Dealer: {dealer}", show=True)

        folium.GeoJson(
            dealer_gdf,
            style_function=lambda x, clr=color: {
                "fillColor": clr,
                "color": clr,
                "weight": 1,
                "fillOpacity": 0.5,
            },
            tooltip=GeoJsonTooltip(fields=["DealerName", "Pincode", "District"])
        ).add_to(dealer_group)

        dealer_group.add_to(m)

    LayerControl(collapsed=False).add_to(m)
    return m

# In[]
# Example usage:
# df_dealers = load_dealer_data("dealers.xlsx")
# gdf_pincodes = load_pincode_geojson("up_pincodes.geojson")

# # gdf_pincodes_map = load_pincode_geojson("map_2.geojson")
# color_map = assign_colors(df_dealers["DealerName"].unique())
# merged_gdf = merge_dealers_with_geo(df_dealers, gdf_pincodes)
# map_object = generate_interactive_map(merged_gdf, color_map)
# map_object.save("dealer_coverage_map.html")

# map_object = generate_interactive_map_v2(merged_gdf, color_map)
# map_object.save("dealer_coverage_map_v2.html")











