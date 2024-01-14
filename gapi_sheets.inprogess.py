# custom styling of cells based on a callback


rgb_colors = {
    'red': [1.0, 0.0, 0.0],   # Red
    'green': [0.0, 1.0, 0.0], # Green
    'blue': [0.0, 0.0, 1.0],  # Blue
    'white': [1.0, 1.0, 1.0], # White
    'black': [0.0, 0.0, 0.0], # Black
    'yellow': [1.0, 1.0, 0.0],# Yellow
    'cyan': [0.0, 1.0, 1.0],  # Cyan
    'magenta': [1.0, 0.0, 1.0]# Magenta
}

def rgb(color):
    red, green, blue = rgb_colors[color]
    return {"red": red, "green": green, "blue": blue},  # Yellow background

def style_callback(color = None, background = None, bold = None):
    style = {}
    if background: style["backgroundColor"] = rgb(background)
    if color: style["foregroundColor"] = rgb(color)
    if bold: style["textFormat"] == {"bold": True}
    return style

def get_fields_from_style(style):
    """
    Generates the fields string for the batchUpdate request based on the style.

    :param style: Style dictionary
    :return: A string of fields for the batchUpdate request
    """
    fields = []
    for key in style.keys():
        fields.append(f"userEnteredFormat.{key}")
    return ",".join(fields)

def apply_styles_based_on_content(self, style_callback):
    values = self.get_cell_values()
    requests = []
    for row, row_data in enumerate(values):
        for col, cell_value in enumerate(row_data):
            style = style_callback(cell_value, row, col)
            if style:
                fields = get_fields_from_style(style, row, col)
                # Add a request for each cell that needs styling
                requests.append({
                    "repeatCell": {
                        "range": {
                            "sheetId": sheet_id,  # Adjust as needed
                            "startRowIndex": row,
                            "endRowIndex": row + 1,
                            "startColumnIndex": col,
                            "endColumnIndex": col + 1
                        },
                        "cell": {
                            "userEnteredFormat": style
                        },
                        "fields": fields
                    }
                })

    # Send batch update request to apply the styles
    if requests:
        body = {'requests': requests}
        self.spreadsheets.batchUpdate(spreadsheetId=self.id, body=body).execute()
