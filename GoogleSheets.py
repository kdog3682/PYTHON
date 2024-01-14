class GoogleSheets:
    def __init__(self):
        self.service = getService("sheets")

    def create_spreadsheet(self, title):
        spreadsheet = {
            'properties': {'title': title}
        }
        spreadsheet = self.service.spreadsheets().create(body=spreadsheet, fields='spreadsheetId').execute()
        return spreadsheet.get('spreadsheetId')

    def add_data(self, spreadsheet_id, range_, values):
        body = {'values': values}
        request = self.service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id, 
            range=range_, 
            valueInputOption='RAW', 
            body=body
        )
        request.execute()

    def format_headers(self, spreadsheet_id, sheet_id=0):
        requests = [{
            'repeatCell': {
                'range': {'sheetId': sheet_id, 'startRowIndex': 0, 'endRowIndex': 1},
                'cell': {'userEnteredFormat': {'textFormat': {'bold': True}}},
                'fields': 'userEnteredFormat.textFormat.bold'
            }
        }]
        body = {'requests': requests}
        self.service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body=body).execute()

    def clear_sheet(self, spreadsheet_id, sheet_id=0):
        request = {
            'requests': [{
                'updateCells': {'range': {'sheetId': sheet_id}, 'fields': '*'}
            }]
        }
        self.service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body=request).execute()

# Usage example
service_account_file = 'path/to/your/service-account.json'
scopes = ['https://www.googleapis.com/auth/spreadsheets']

# sheets = GoogleSheets(service_account_file, scopes)
# spreadsheet_id = sheets.create_spreadsheet("My New Spreadsheet")
# sheets.add_data(spreadsheet_id, 'Sheet1!A1:B', [['Header1', 'Header2'], ['Data1', 'Data2']])
# sheets.format_headers(spreadsheet_id)
# sheets.clear_sheet(spreadsheet_id)


# Example usage
# data = [['Header1', 'Header2']]
# range_string = generate_range_string(data)
# print(range_string)  # Output: 'Sheet1!A1:B2'

