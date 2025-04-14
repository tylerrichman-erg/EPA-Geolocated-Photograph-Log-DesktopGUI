class Config:
    def __init__(self, config):
        ### Map Window Properties ###
        self.main_window_title = config['Main Window Properties']['title']
        self.main_window_geometry = config['Main Window Properties']['geometry']
        self.main_window_resizable_width = config['Main Window Properties']['resizable_width']
        self.main_window_resizable_height = config['Main Window Properties']['resizable_height']
        self.main_window_font_type = config['Main Window Properties']['font_type']

        ### Title Properties ###
        self.title_text = config['Title Properties']['text']
        self.title_font_size = config['Title Properties']['font_size']
        self.title_pady_top = config['Title Properties']['pady_top']
        self.title_pady_bottom = config['Title Properties']['pady_bottom']

        ### Label Properties ###
        self.label_font_size = config['Label Properties']['font_size']
        self.label_font_style = config['Label Properties']['font_style']
        self.label_photographer_text = config['Label Properties']['photographer_text']
        self.label_facility_text = config['Label Properties']['facility_text']
        self.label_inspection_date_text = config['Label Properties']['inspection_date_text']
        self.label_table_text = config['Label Properties']['table_text']
        self.label_output_file_text = config['Label Properties']['output_file_text']
        self.label_pady_top  = config['Label Properties']['pady_top']
        self.label_pady_bottom = config['Label Properties']['pady_bottom']

        ### Entry Properties ###
        self.entry_width = config['Entry Properties']['width']
        self.entry_pady_top = config['Entry Properties']['pady_top']
        self.entry_pady_bottom = config['Entry Properties']['pady_bottom']

        ### Table Properties ###
        self.table_column_width = config['Table Properties']['column_width']
        self.table_row_display_count = config['Table Properties']['row_display_count']
        self.table_selected_cell_bg = config['Table Properties']['selected_cell_bg']
        self.table_pady_top = config['Table Properties']['pady_top']
        self.table_pady_bottom = config['Table Properties']['pady_bottom']

        ### Table Field Names ###
        self.table_field_names_file_name = config['Table Field Names']['file_name']
        self.table_field_names_latitude = config['Table Field Names']['latitude']
        self.table_field_names_longitude = config['Table Field Names']['longitude']
        self.table_field_names_bearing = config['Table Field Names']['bearing']

        ### Select Button Properties ###
        self.select_button_text = config['Select Button Properties']['text']
        self.select_button_width = config['Select Button Properties']['width']
        self.select_button_pady = config['Select Button Properties']['pady']

        ### Generate Report Button Properties ###
        self.generate_report_button_text = config['Generate Report Button Properties']['text']
        self.generate_report_button_width = config['Generate Report Button Properties']['width']
        self.generate_report_button_pady_top = config['Generate Report Button Properties']['pady_top']
        self.generate_report_button_pady_bottom = config['Generate Report Button Properties']['pady_bottom']
        self.generate_report_button_font_size = config['Generate Report Button Properties']['font_size']
        self.generate_report_button_font_style = config['Generate Report Button Properties']['font_style']
        self.generate_report_button_pady_top = config['Generate Report Button Properties']['pady_top']
        self.generate_report_button_pady_bottom = config['Generate Report Button Properties']['pady_bottom']

        ### Image Properties ###
        self.img_width = config['Image Properties']['width']
        self.img_height = config['Image Properties']['height']

        ### Map Properties ###
        self.map_control_scale = config['Map Properties']['control_scale']
        self.map_zoom_control = config['Map Properties']['zoom_control']
        self.map_dragging = config['Map Properties']['dragging']

        ### Overview Map Properties ###
        self.overview_map_zoom = config['Overview Map Properties']['zoom']
        self.overview_map_width = config['Overview Map Properties']['width']
        self.overview_map_height = config['Overview Map Properties']['height']
        self.overview_map_basemap = config['Overview Map Properties']['basemap']

        ### Individual Map Properties ###
        self.individual_map_zoom = config['Individual Map Properties']['zoom']
        self.individual_map_width = config['Individual Map Properties']['width']
        self.individual_map_height = config['Individual Map Properties']['height']
        self.individual_map_imagery_basemap = config['Individual Map Properties']['imagery_basemap']
        self.individual_map_terrain_basemap = config['Individual Map Properties']['terrain_basemap']

        ### Icon Properties ###
        self.icon_name = config['Icon Properties']['name']
        self.icon_size = config['Icon Properties']['size']
        self.icon_shape = config['Icon Properties']['shape']
        self.icon_border_color = config['Icon Properties']['border_color']
        self.icon_border_width = config['Icon Properties']['border_width']
        self.icon_background_color = config['Icon Properties']['background_color']
        self.icon_text_color = config['Icon Properties']['text_color']

        ### Document Properties ###
        self.document_overview_title = config['Document Properties']['overview_title']
        self.document_overview_text_rel_path = config['Document Properties']['overview_text_rel_path']
        self.document_overview_img_width_in = config['Document Properties']['overview_img_width_in']
        self.document_photo_img_width_in = config['Document Properties']['photo_img_width_in']
        self.document_imagery_img_width_in = config['Document Properties']['imagery_img_width_in']
        self.document_terrain_img_width_in = config['Document Properties']['terrain_img_width_in']
        self.document_header_end_text = config['Document Properties']['header_end_text']
        self.document_footer_beginning_text = config['Document Properties']['footer_beginning_text']

        ### Pop-Up Properties ###
        self.popup_title = config['Pop-Up Properties']['title']
        self.popup_geometry = config['Pop-Up Properties']['geometry']
        self.popup_pady = config['Pop-Up Properties']['pady']