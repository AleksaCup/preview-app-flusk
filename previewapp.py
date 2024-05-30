from flask import Flask, render_template, after_this_request, send_from_directory
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import zipfile
import re
import os
import datafetch
from imagesfetch import *
import pandas as pd
from datetime import datetime


app = Flask(__name__)

app.config['DEBUG'] = True

SECTION_FOLDER_NAMES = {
    'grid': 'Grid',
    'highlights': 'Highlights',
    'highlighted_post': 'Highlighted post',
    'flyers': 'Flyers',
    'must_have': 'Must Have',

}

# Google Drive API credentials
CLIENT_ID = '623345392233-1or5nb79khcdbj4825tnfnva5v8vhdnn.apps.googleusercontent.com'
CLIENT_SECRET = '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'
REDIRECT_URI = 'https://developers.google.com/oauthplayground'
REFRESH_TOKEN = '1//04nG6sxGfiZ3eCgYIARAAGAQSNwF-L9IrCWFoBNWiMFeVH5OWuinkbCGQdNDEAJ4FNEsu2Val85MMo0c4_nEgvEefEIVKu2Lhwxk'

# Load the service account credentials
credentials = Credentials.from_authorized_user_info({

    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "redirect_uris": [REDIRECT_URI],
    "token_uri": "https://accounts.google.com/o/oauth2/token",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_info_uri": "https://oauth2.googleapis.com/tokeninfo",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "refresh_token": REFRESH_TOKEN,
    
})

# Create a Drive API client
drive_service = build('drive', 'v3', credentials=credentials)

ROOT_FOLDER_ID = "1ory7m04Z_WzAaoMZSd4f1wqkOnUcpOMA"



@app.route('/')
def index():
    return render_template('test.html')

@app.route('/<string:user_name>')
def show_user(user_name):

    # Convert the user_name to lowercase and replace spaces/hyphens with spaces
    user_name = re.sub(r'[-\s]+', ' ', user_name.lower())
    
    # Capitalize each word to match the format in the database
    name_parts = user_name.split(" ")
    user_name_capitalized = ' '.join([part.capitalize() for part in name_parts])

    users = datafetch.fetch_client_infos()


    user = None
    for u in users:
        user_fullname = f"{users[u].get('name', '')} {users[u].get('surname', '')}".strip()
        if user_fullname.lower() == user_name_capitalized.lower():
            user = users[u]
            break

    if user:
        start = datetime.now()
        # person_folder_id = fetch_subfolder_id_by_name(drive_service, ROOT_FOLDER_ID, user['name'] + " " + user['surname'])
        person_folder_id = ""

        # if user['grid'] == 'TRUE':
        #     grid_folder_id = fetch_subfolder_id_by_name(drive_service, person_folder_id, SECTION_FOLDER_NAMES['grid'])
        #     folder_ids = fetch_subfolders(drive_service, grid_folder_id)
        
        #     grid_image_ids, grid_mimetypes = fetch_image_ids_from_folder(drive_service, person_folder_id, SECTION_FOLDER_NAMES['grid']) #GRID

        #     sorted_data = dict(sorted(grid_image_ids.items(), key=lambda item: int(item[0]), reverse=True))
        #     sorted_mimetypes = dict(sorted(grid_mimetypes.items(), key=lambda item: int(item[0]), reverse=True))
        #     sorted_folder_ids = sorted(folder_ids, key=lambda x: int(x['name']), reverse=True)

        #     user['grid_image_ids'] = sorted_data
        #     user['grid_mimetypes'] = sorted_mimetypes
        #     user['grid_folders_ids'] = sorted_folder_ids
        #     zip_ids = fetch_zip_files_from_folders(drive_service, sorted_folder_ids)
        #     user['zip_ids'] = zip_ids

        # if user['highlights'] == 'TRUE':
        #     highlights_folder_id = fetch_subfolder_id_by_name(drive_service, person_folder_id, SECTION_FOLDER_NAMES['highlights'])
        #     highlights_image_ids, mimetypes_highlihts = fetch_image_ids_from_specific_folder(drive_service, highlights_folder_id)
        #     highlights_image_ids.reverse()
        #     user['highlights_ids'] = highlights_image_ids

        # if user['highlighted_post'] == 'TRUE':
        #     highlighted_folder_id = fetch_subfolder_id_by_name(drive_service, person_folder_id, SECTION_FOLDER_NAMES['highlighted_post'])
        #     highlighted_image_ids = fetch_image_ids_from_specific_folder(drive_service, highlighted_folder_id)
        #     highlighted_image_zip = fetch_zip_files_from_folders(drive_service, [{'id': highlighted_folder_id, 'name': SECTION_FOLDER_NAMES['highlighted_post']}])
        #     user['highlighted_image_ids'] = highlighted_image_ids
        #     user['highlighted_post_zip'] = list(highlighted_image_zip.values())[0]
        #     print(highlighted_image_zip)

        # if user['must_have'] == 'TRUE':
        #     musthave_folder_id = fetch_subfolder_id_by_name(drive_service, person_folder_id, SECTION_FOLDER_NAMES['must_have'])

        #     presentations_folder_id = fetch_subfolder_id_by_name(drive_service, musthave_folder_id, "Presentations")
        #     presentations = fetch_filename_to_id_mapping(drive_service, presentations_folder_id)
        #     user['presentations'] = presentations

        #     pdf_folder_id = fetch_subfolder_id_by_name(drive_service, musthave_folder_id, "Pdf")
        #     pdfs = fetch_filename_to_id_mapping(drive_service, pdf_folder_id)
        #     user['pdfs'] = pdfs

        #     preprint_folder_id = fetch_subfolder_id_by_name(drive_service, musthave_folder_id, "Preprint")
        #     preprint = fetch_filename_to_id_mapping(drive_service, preprint_folder_id)
        #     user['preprint'] = preprint

        #     logotypes_folder_id = fetch_subfolder_id_by_name(drive_service, musthave_folder_id, "Logotypes")
        #     logotypes = fetch_filename_to_id_mapping(drive_service, logotypes_folder_id)
        #     user['logotypes'] = logotypes

        # if user['flyers'] == 'TRUE':
        #     flyers_folder_id = fetch_subfolder_id_by_name(drive_service, person_folder_id, SECTION_FOLDER_NAMES['flyers'])
        #     flyers_image_ids = fetch_filename_to_id_mapping(drive_service, flyers_folder_id)
        #     user['flyer'] = flyers_image_ids

        

        # all_files = []
        # fetch_files(drive_service, "1oW_LKWRODXs3wyq-2QtYU8gr545He7i9", '', all_files)

        # print(datetime.now()-start)
        # df = pd.DataFrame(all_files)
        # print(df)

        root_folder_id = '1oW_LKWRODXs3wyq-2QtYU8gr545He7i9'
        drive_data = get_drive_data(drive_service, root_folder_id)
        df = pd.DataFrame(drive_data)
        print(df)

    return render_template('user.html', userdata = user)





@app.route('/download_folder/<folder_id>', methods=['GET'])
def download_folder(folder_id):
    files = drive_service.files().list(q=f"'{folder_id}' in parents").execute().get('files', [])
    
    #zip_filename = f"{folder_id}.zip"
    with zipfile.ZipFile(folder_id, 'w') as myzip:
        for file in files:
            file_id = file['id']
            file_name = file['name']

            request = drive_service.files().get_media(fileId=file_id)
            response = request.execute()

            # Add to zip
            myzip.writestr(file_name, response)

    print("ZIP creation complete.")

    response = send_from_directory(os.getcwd(), folder_id, as_attachment=True, mimetype='application/zip')
    response.headers["Content-Disposition"] = f"attachment; filename={folder_id}.zip"

    @after_this_request
    def remove_file(response):
        try:
            os.remove(os.path.join(os.getcwd(), folder_id))
        except Exception as error:
            app.logger.error("Error deleting file [%s]: %s", folder_id, error)
        return response

    return response




if __name__ == '__main__':
    app.run()
