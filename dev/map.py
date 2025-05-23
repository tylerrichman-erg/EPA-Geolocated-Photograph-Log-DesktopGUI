import folium
import folium.plugins as plugins
import io
import math
from PIL import Image, ImageOps
import os
import shutil

def mean_center(latitude_list, longitude_list):
    latitude_list = [x for x in latitude_list if x != 0]
    longitude_list = [x for x in longitude_list if x != 0]
    latitude_mean = sum(latitude_list)/len(latitude_list)
    longitude_mean = sum(longitude_list)/len(longitude_list)
    return latitude_mean, longitude_mean

def folium_bounds(center_lat, center_lon, zoom, width_px, height_px):
    EARTH_CIRCUMFERENCE = 40075016.686  # meters
    TILE_SIZE = 256
    lat_rad = math.radians(center_lat)

    # Meters per pixel at current zoom
    initial_resolution = EARTH_CIRCUMFERENCE / TILE_SIZE
    resolution = initial_resolution / (2 ** zoom)

    # Map size in meters
    half_width_m = (width_px / 2) * resolution
    half_height_m = (height_px / 2) * resolution

    # Convert meters to degrees
    lat_deg_per_meter = 1 / 111320  # constant
    lon_deg_per_meter = 1 / (111320 * math.cos(lat_rad))

    delta_lat = half_height_m * lat_deg_per_meter
    delta_lon = half_width_m * lon_deg_per_meter

    min_lat = center_lat - delta_lat
    max_lat = center_lat + delta_lat
    min_lon = center_lon - delta_lon
    max_lon = center_lon + delta_lon

    return {
        "min_lat": min_lat,
        "max_lat": max_lat,
        "min_lon": min_lon,
        "max_lon": max_lon
    }

def create_map(center_latitude, center_longitude, tiles, zoom, img_width, img_height, map_control_scale, map_zoom_control, map_dragging):
    m = folium.Map(
        location = (center_latitude, center_longitude),
        tiles = tiles,
        attr = "",
        zoom_start = zoom,
        width = img_width,
        height = img_height,
        control_scale = map_control_scale,
        zoom_control = False, #map_zoom_control,
        dragging = map_dragging
    )

    hide_attribution = """
    <style>
    .leaflet-control-attribution {
        display: none !important;
    }
    </style>
    """
    
    m.get_root().html.add_child(folium.Element(hide_attribution))
    return m

def create_icon(icon_name, icon_size, icon_shape, icon_border_color, icon_border_width, icon_background_color, icon_text_color, bearing):
    icon = plugins.BeautifyIcon(
        icon = icon_name,
        iconSize = [float(icon_size), float(icon_size)],
        iconAnchor = [float(icon_size)/2, float(icon_size)/2],
        iconShape = icon_shape,
        innerIconAnchor = [0,5], # Alter depending on arrow size.
        innerIconStyle ='transform: rotate({0}deg);'.format(bearing),
        borderColor = icon_border_color,
        borderWidth = int(icon_border_width),
        backgroundColor = icon_background_color,
        textColor = icon_text_color
    )
    return icon

def add_icons_to_map(m, icon, latitude, longitude):
    folium.Marker(
        location = [latitude, longitude],
        icon = icon
        ).add_to(m)
    return

def save_map_to_image(m, img_path):
    img_data = m._to_png(5)
    img = Image.open(io.BytesIO(img_data))
    img = ImageOps.expand(img, border=5, fill='black') # Move to config file.
    rgb_im = img.convert('RGB') # Move to config file.
    rgb_im.save(img_path, format='JPEG') # Move to config file.

    #img_data = m._to_png(5)
    #img = Image.open(io.BytesIO(img_data))
    #img.save(img_path)
    return

def generate_overview_map(df, output_folder, filename_field, latitude_field, longitude_field, bearing_field, tiles, zoom, img_width, img_height, map_control_scale, map_zoom_control, map_dragging, 
    icon_name, icon_size, icon_shape, icon_border_color, icon_border_width, icon_background_color, icon_text_color):

    mean_latitude, mean_longitude = mean_center(
        [float(s) for s in df[latitude_field].tolist()],
        [float(s) for s in df[longitude_field].tolist()]
        )

    latitude_list = [float(s) for s in df[latitude_field].tolist()]
    longitude_list = [float(s) for s in df[longitude_field].tolist()]

    zoom_found = False

    zoom = int(zoom)

    while not zoom_found:
        bounds = folium_bounds(float(mean_latitude), float(mean_longitude), int(zoom), int(img_width), int(img_height))
        if (bounds["min_lat"] < min(latitude_list) and bounds["max_lat"] > max(latitude_list)) and (bounds["min_lon"] < min(longitude_list) and bounds["max_lon"] > max(longitude_list)):
            zoom_found = True
        else:
            zoom -= 1

    m = create_map(
        center_latitude = mean_latitude, 
        center_longitude = mean_longitude, 
        tiles = tiles,
        zoom = zoom, 
        img_width = int(img_width),
        img_height = int(img_height),
        map_control_scale = map_control_scale, 
        map_zoom_control = map_zoom_control, 
        map_dragging = map_dragging
        )

    for index, row in df.iterrows():
        icon = create_icon(
            icon_name = icon_name, 
            icon_size = icon_size, 
            icon_shape = icon_shape, 
            icon_border_color = icon_border_color, 
            icon_border_width = icon_border_width, 
            icon_background_color = icon_background_color, 
            icon_text_color = icon_text_color, 
            bearing = row[bearing_field]
            )

        add_icons_to_map(
            m = m,
            icon = icon,
            latitude = row[latitude_field],
            longitude = row[longitude_field]
            )

    save_map_to_image(
        m = m, 
        img_path = os.path.join(output_folder, "overview.jpg")
        )
    return

def generate_individual_map(df, output_folder, no_img_path, filename_field, latitude_field, longitude_field, bearing_field, tiles, zoom, img_width, img_height, map_control_scale, map_zoom_control, 
    map_dragging, icon_name, icon_size, icon_shape, icon_border_color, icon_border_width, icon_background_color, icon_text_color):
    for index, row in df.iterrows(): 
        if float(row[latitude_field]) != 0 or float(row[longitude_field]) != 0:
            m = create_map(
                center_latitude = row[latitude_field], 
                center_longitude = row[longitude_field], 
                tiles = tiles,
                zoom = zoom, 
                img_width = int(img_width),
                img_height = int(img_height),
                map_control_scale = map_control_scale, 
                map_zoom_control = map_zoom_control, 
                map_dragging = map_dragging
                )

            icon = create_icon(
                icon_name = icon_name, 
                icon_size = icon_size, 
                icon_shape = icon_shape, 
                icon_border_color = icon_border_color, 
                icon_border_width = icon_border_width, 
                icon_background_color = icon_background_color, 
                icon_text_color = icon_text_color, 
                bearing = row[bearing_field]
                )

            add_icons_to_map(
                m = m,
                icon = icon,
                latitude = row[latitude_field],
                longitude = row[longitude_field]
                )

            save_map_to_image(
                m = m, 
                img_path = os.path.join(output_folder, row[filename_field])
                )

        else:
            shutil.copy2(
                no_img_path, 
                os.path.join(output_folder, row[filename_field])
                )

    return