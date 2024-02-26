from gapi_setup import *
from gapi_drive import get_file
from utils import *


class GoogleSheets:
    def __init__(self, name=None):
        self.spreadsheets = servicer("sheets")
        self.sheet_index = 0
        if name:
            self.spreadsheet = get_file(
                name=name, mimetype="spreadsheet"
            )
            self.id = resolve_id(self.spreadsheet)

    def resize(self, *args, **kwargs): return resize(self, *args, *kwargs)
    def clear(self, *args, **kwargs): return clear(self, *args, *kwargs)
    def format(self, *args, **kwargs): return format(self, *args, *kwargs)

    @property
    def dimensions(self):
        sheets = self.spreadsheets.get(
            spreadsheetId=self.id
        ).execute()

        pprint(sheets)
        sheet = sheets[self.sheet_index]
        print("sheet", sheet)
        data = sheet["properties"][ "gridProperties" ]
        return (data["rowCount"], data["columnCount"])

    def get_cell_values(self, range="A1:Z10000"):
        result = (
            self.spreadsheets.values()
            .get(spreadsheetId=self.id, range=range)
            .execute()
        )
        values = result.get("values", [])
        return values

    def __repr__(self):
        return pretty_print(self.spreadsheet)

    def create(self, title, data=None, styles=None):

        """
        Creates a new spreadsheet with the specified title.

        :param title: Title of the new spreadsheet.
        :sets: id
        :return: None
        """

        body = {"properties": {"title": title}}
        spreadsheet = self.spreadsheets.create(
            body=body, fields="spreadsheetId"
        ).execute()
        self.id = spreadsheet.get("spreadsheetId")
        self.add(data)

    def add(self, values=None):
        """
        Adds data to the specified range in the spreadsheet.
        :param values: Data to be added, as a list of lists.
        """
        if empty(values):
            return
        body = {"values": values}
        request = self.spreadsheets.values().update(
            spreadsheetId=self.id,
            range=generate_range_string(values),
            valueInputOption="RAW",
            body=body,
        )
        request.execute()

    @property
    def url(self):
        return f"https://docs.google.com/spreadsheets/d/{self.id}"

    @property
    def metadata(self):
        return self.spreadsheets.get(spreadsheetId=self.id).execute()


def generate_range_string(data, sheet_name="Sheet1", start_cell="A1"):
    """
    Generates a Google Sheets range string based on the provided data.
    :param sheet_name: Name of the sheet (e.g., 'Sheet1')
    :param start_cell: Starting cell of the range (e.g., 'A1')
    :param data: List of lists representing the data to be inserted
    :return: Google Sheets range string
    """
    if not data or not data[0]:
        raise ValueError("Data should be a non-empty list of lists.")

    # Get number of rows and columns
    num_rows = len(data)
    num_cols = len(data[0])

    # Calculate ending row number
    start_row = int(start_cell[1:])
    end_row = start_row + num_rows - 1

    # Calculate ending column letter
    start_col = start_cell[0].upper()
    end_col = chr(ord(start_col) + num_cols - 1)

    return f"{sheet_name}!{start_col}{start_row}:{end_col}{end_row}"


def resize(self, rows=100, cols=10):
    current_rows, current_cols = self.dimensions
    sheet_id = self.sheet_id
    requests = []

    # Adjust rows
    if current_rows > rows:
        requests.append(
            {
                "deleteDimension": {
                    "range": {
                        "sheetId": sheet_id,
                        "dimension": "ROWS",
                        "startIndex": rows,
                        "endIndex": current_rows,
                    }
                }
            }
        )
    elif current_rows < rows:
        requests.append(
            {
                "appendDimension": {
                    "sheetId": sheet_id,
                    "dimension": "ROWS",
                    "length": rows - current_rows,
                }
            }
        )

    # Adjust columns
    if current_cols > cols:
        requests.append(
            {
                "deleteDimension": {
                    "range": {
                        "sheetId": sheet_id,
                        "dimension": "COLUMNS",
                        "startIndex": cols,
                        "endIndex": current_cols,
                    }
                }
            }
        )
    elif current_cols < cols:
        requests.append(
            {
                "appendDimension": {
                    "sheetId": sheet_id,
                    "dimension": "COLUMNS",
                    "length": cols - current_cols,
                }
            }
        )

    if requests:
        self.spreadsheets.batchUpdate(
            spreadsheetId=self.id, body={"requests": requests}
        ).execute()

def clear(self):
    request = {
        "requests": [
            {
                "updateCells": {
                    "range": {"sheetId": self.sheet_id},
                    "fields": "*",
                }
            }
        ]
    }
    self.spreadsheets.batchUpdate(
        spreadsheetId=self.id, body=request
    ).execute()



def format(self, sheet_id=0, **kwargs):
    """
    Formats the first row of the sheet as bold.
    :param sheet_id: ID of the sheet (default is 0).
    """
    requests = [
        {
            "repeatCell": {
                "range": {
                    "sheetId": sheet_id,
                    "startRowIndex": 0,
                    "endRowIndex": 1,
                },
                "cell": {
                    "userEnteredFormat": {
                        "textFormat": {"bold": True}
                    }
                },
                "fields": "userEnteredFormat.textFormat.bold",
            }
        }
    ]
    body = {"requests": requests}
    self.spreadsheets.batchUpdate(
        spreadsheetId=self.id, body=body
    ).execute()


finance = GoogleSheets("fina")
pprint(finance)  # gets financial statements
# finance.resize(rows=10, cols=10)
# open(finance)
