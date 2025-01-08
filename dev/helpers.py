import folium
import folium.plugins as plugins

def create_map_from_table(
    img_width,
    img_height,
    map_control_scale,
    icon_name,
    icon_size,
    icon_shape,
    icon_border_color,
    icon_border_width,
    icon_background_color,
    icon_text_color
):
    m = folium.Map(
        location=(34.2104, -77.8868), # Alter depending on location.
        width=img_width,
        height=img_height,
        control_scale=map_control_scale,
        zoom_control=map_zoom_control,
        dragging=map_dragging
    )

    icon = plugins.BeautifyIcon(
        icon=icon_name,
        iconSize=[icon_size, icon_size],
        iconAnchor=[icon_size/2, icon_size/2],
        iconShape=icon_shape,
        innerIconAnchor=[0,5], # Alter depending on arrow size.
        innerIconStyle='transform: rotate({0}deg);'.format(bearing),
        borderColor=icon_border_color,
        borderWidth=icon_border_width,
        backgroundColor=icon_background_color,
        textColor=icon_text_color
    )

    return