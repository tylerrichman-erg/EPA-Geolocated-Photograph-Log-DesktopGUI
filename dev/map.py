import folium
import folium.plugins as plugins
import io
from PIL import Image
import os

def mean_center(latitude_list, longitude_list):
    latitude_mean = sum(latitude_list)/len(latitude_list)
    longitude_mean = sum(longitude_list)/len(longitude_list)
    return latitude_mean, longitude_mean

def create_map(center_latitude, center_longitude, zoom, img_width, img_height, map_control_scale, map_zoom_control, map_dragging):
    m = folium.Map(
        location=(center_latitude, center_longitude),
        tiles = "Esri.WorldImagery",
        zoom_start = zoom,
        width = img_width,
        height = img_height,
        control_scale = map_control_scale,
        zoom_control = False, #map_zoom_control,
        dragging = map_dragging
    )
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
    rgb_im = img.convert('RGB')
    rgb_im.save(img_path, format='JPEG')

    #img_data = m._to_png(5)
    #img = Image.open(io.BytesIO(img_data))
    #img.save(img_path)
    return

def generate_individual_maps(df, output_folder, filename_field, latitude_field, longitude_field, bearing_field, zoom, img_width, img_height, map_control_scale, map_zoom_control, map_dragging, 
    icon_name, icon_size, icon_shape, icon_border_color, icon_border_width, icon_background_color, icon_text_color):
    for index, row in df.iterrows(): 
        m = create_map(
            center_latitude = row[latitude_field], 
            center_longitude = row[longitude_field], 
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

    return