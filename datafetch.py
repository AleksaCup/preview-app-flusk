import gspread
import data as data
from google.oauth2.service_account import Credentials as cd

def fetch_client_infos():

    

    credentials = cd.from_service_account_info(data.json_data, scopes=data.scopes)

    client = gspread.Client(auth=credentials)
    client.session.verify = True  # Enable SSL certificate verification if needed

    # Open the spreadsheet by its title
    spreadsheet = client.open_by_key(data.speadsheet_id)

    # Select the worksheet you want to fetch data from
    worksheet_preview = spreadsheet.worksheet("preview")
    worksheet_ads = spreadsheet.worksheet("ads")

    all_values_preview = worksheet_preview.get_all_values()
    all_values_ads = worksheet_ads.get_all_values()
    # Extract header and data
    header_preview = all_values_preview[0]
    data_preview = all_values_preview[1:]

    header_ads = all_values_ads[0]
    data_ads = all_values_ads[1:]

    # Filter out rows without an ID
    filtered_data_preview = [row for row in data_preview if row[0]]
    filtered_data_ads = [row for row in data_ads if row[0]]

    # Convert the filtered data into dictionary format
    users = {}
    for row in filtered_data_preview:
        user_dict = dict(zip(header_preview, row))
        user_id = user_dict.pop('id')  # Removes the 'id' key from user_dict and gets its value
        user_dict['events'] = []
        users[user_id] = user_dict

    for row in filtered_data_ads:
        id = row[0]
        master = row[1]
        event = row[2]
        instagram_links = row[3].strip().split(" ")
        facebook_links = row[4].strip().split(" ")

        if id in users:
            # If the user exists, add the event information to their existing data
            users[id]['events'].append({'master': master, 'event': event, 'instagram_link': instagram_links, 'facebook_link': facebook_links})

    return  users