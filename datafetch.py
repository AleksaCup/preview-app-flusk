import gspread
from google.oauth2.service_account import Credentials as cd

def fetch_client_infos():

    json_data = {
    "type": "service_account",
    "project_id": "previewapp-393812",
    "private_key_id": "c81a9092346cdcca5344d4216ff00fe46cd0f830",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDODG+UNUcdH3tG\nUkdZhNdK6NS4g0X0W6HsBzSp7xB71sQyZYCfBw3eGndbUGQp4L/QtkVTAggaJNtk\nJeZtymV/01UZmX/X3WdciDCh0tDYp5hWYKfHSfKeckPtvmustz7T23f5bxtNMot5\nW47QltZTWePSGRN5fLcNN0AJbzReIVidc8cMkbc+NBWm35ZqErj+KRn7iWeGC2BZ\nGFZQNNBzkCbUO5LfpgPGwYRFluVhKYcn9Tv5JSQ6bF0MGhuCINgAbEWkDW/kfCXs\n2TmRMyEAsyv9AHe3HfiFKg6OC/YE1DQmTyPDO/IaPfnAbBh7le/Wx5mw7KrxeBXE\nOEA8/lJDAgMBAAECggEAQxL9R4vIaIyU/qFOJK//vZzpkl75aMBjh4gY9rCh9w5E\ns/si0aHkO8b1z73tvUwyZOjQzGK+7HPPD1zfFCJsxB2xeDHl0gl62j5jRmpwHfcA\nui2gsFk8J6QexMfWGVVVmHW7KnGmu4yWppzNcs2HW37JkN0k38lfdWfk6q1OqM0v\n2y/cbwtQoULX9SifsRcptR7IK0aQBIU34bRpuwBEn0rYp6fafkb5ectBYZTnpELG\nWQ9rCRNrDICx0IBL8AafZ42SEaVzZ2CKvki+LxSnbqFrPXIS++HD7EUrQmjEKhrD\nrGzLvb/fbS/Y4vW7+BwSVpwdKInFofIFqn21Zu3VQQKBgQD9x36BTfGQ0N11/rD4\nYpNO31mDUhfXqMw6EgJT5WjP4ioHWcNF1M4W27hZ7+GVbjOFk2CnOnlwtIU0PZcd\nWRA8rJVBn55wKQ3Bg6wic/685c+h0kWajzMYBh3WkaQxYTi2aloU9vWrrVXL0Oe5\nEJkVVzS3cHc0/ZcQQPQbVQxDcQKBgQDP2gRxy+BN07OVBnfaUZ8DEG3xsLsIO0LK\n5sYAsj4fiEL29i4RyWFAi9iTqE9ruejlMPZaUx/ndVi4VPRDlhxZZkJ3AdLMmpOv\nhMHnbgAEvZfxkb4x02g6NH4yYAzHs1b52BQoqZ/NXEjAZLKuHQN+9P8lro5k2DZF\ngznHG/wu8wKBgECDOjF8su/xaJraR/qcdH4UYRj1AYKdMm2Arn7NTrup7q03sGBM\nHKfK6y5RwLLP9OD7+hII115DRalmDsgzH+GMrdSk0w4IIasT4epQOm2irgmg/niv\n9nkg9Oza0TaMVHJqzsONlB40Th8l2AI/qeq25HvNZ0BdRs2m9WcNU7TBAoGBALbr\nm7W6QvC7OvQP+TJ9Wn+L2fY2HqOj46hFaEP8mYeOl8BX7ztgCuKPME7idOLNfhUV\n/fiH5y//qdCvkzhXxyM2R5AMXsQJ1adGIo/V0tZZNHs4VDXtY3C1+cnDlfu57PV8\nIGGYxjYo3S3UcRuiFQ2J93HmKRK+5SRP1G1SR6HZAoGAKskyH3Eua4991pHHPwPg\nS1lOMxlswVSY9rVufcoLzeEmZ+/hQNJSJ0gsZi8B4ZlXnO/8f04gicBTa50jY8Wt\n9/lNKDNt2AQkTq+aGVSVWyKVj61iqVgTtdy5ba6V3b3AWCrSzWYsIftV8rug0lXV\nkVpoQiUrL3Rc67IqePw6dHQ=\n-----END PRIVATE KEY-----\n",
    "client_email": "previewapp-spreadsheet@previewapp-393812.iam.gserviceaccount.com",
    "client_id": "116760683510105440357",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/previewapp-spreadsheet%40previewapp-393812.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
    }

    speadsheet_id = '1TbKXJThTrYu8-gJsMI8Q52Yb9QFAqgAKbmsxXmg_0ec'

    scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

    credentials = cd.from_service_account_info(json_data, scopes=scopes)

    client = gspread.Client(auth=credentials)
    client.session.verify = True  # Enable SSL certificate verification if needed

    # Open the spreadsheet by its title
    spreadsheet = client.open_by_key(speadsheet_id)

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