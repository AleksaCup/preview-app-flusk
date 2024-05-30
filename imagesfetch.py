# def fetch_image_ids_from_folder(drive_service, person_folder_id, subfolder_name):
#     image_ids = {}
#     mimetypes = {}

#     # Get the Grid folder within the person's folder
#     grid_folder_id = fetch_subfolder_id_by_name(drive_service, person_folder_id, subfolder_name)
    
#     if grid_folder_id is None:
#         return {}
    
#     # Fetch all subfolders under the Grid folder
#     subfolders = fetch_subfolders(drive_service, grid_folder_id)

#     for folder in subfolders:
#         numbered_folder_name = folder['name']
#         numbered_folder_id = folder['id']
        
#         ids_in_numbered_folder, mimetypes_in_folder = fetch_image_ids_from_specific_folder(drive_service, numbered_folder_id)
#         image_ids[numbered_folder_name] = ids_in_numbered_folder
#         mimetypes[numbered_folder_name] = mimetypes_in_folder
    
#     return image_ids, mimetypes


# def fetch_subfolder_id_by_name(drive_service, parent_folder_id, subfolder_name):
#     page_token = None
#     while True:
#         response = drive_service.files().list(q=f"'{parent_folder_id}' in parents and mimeType = 'application/vnd.google-apps.folder' and name = '{subfolder_name}'",
#                                               fields='nextPageToken, files(id, name)',
#                                               pageSize=1000,
#                                               pageToken=page_token).execute()
#         for file in response.get('files', []):
#             if file['name'] == subfolder_name:
#                 return file['id']
#         page_token = response.get('nextPageToken', None)
#         if page_token is None:
#             break
#     return None

# def fetch_image_ids_from_specific_folder(drive_service, folder_id):
#     ids = []
#     mimetypes = []
#     page_token = None
#     while True:
#         response = drive_service.files().list(q=f"'{folder_id}' in parents and mimeType != 'application/vnd.google-apps.folder' and mimeType != 'application/x-zip-compressed'",
#                                               fields='nextPageToken, files(id, name, webViewLink, mimeType)',
#                                               pageSize=1000,
#                                               orderBy='createdTime',
#                                               pageToken=page_token).execute()
#         for file in response.get('files', []):
#             if 'webViewLink' in file:
#                 ids.append(file['id'])
#                 mimetypes.append(file['mimeType'])
#         page_token = response.get('nextPageToken', None)
#         if page_token is None:
#             break
#     return ids, mimetypes


# def fetch_subfolders(drive_service, parent_id):
#     """Fetch all subfolders under a parent folder."""
#     query = "'{}' in parents and mimeType='application/vnd.google-apps.folder'".format(parent_id)
#     results = drive_service.files().list(q=query, fields="nextPageToken, files(id, name)").execute()
#     items = results.get('files', [])

#     return items



# def get_mime_type(drive_service, file_id):
#     file = drive_service.files().get(fileId=file_id, fields='mimeType').execute()
#     return file['mimeType']




# def fetch_filename_to_id_mapping(drive_service, folder_id):
#     mapping = {}
#     page_token = None
#     while True:
#         response = drive_service.files().list(
#             q=f"'{folder_id}' in parents and mimeType != 'application/vnd.google-apps.folder'",
#             fields='nextPageToken, files(id, name)',
#             pageSize=1000,
#             orderBy='name',
#             pageToken=page_token
#         ).execute()
        
#         for file in response.get('files', []):
#             file_id = file['id']
#             filename = file['name']
            
#             # Remove the file extension if it exists
#             filename_without_extension = filename.split(".")[0]
            
#             # Check if the file is a PDF or PPTX
#             mime_type = get_mime_type(drive_service, file_id)
#             if mime_type in ['application/pdf', 'application/vnd.openxmlformats-officedocument.presentationml.presentation', 'application/x-zip-compressed']:
#                 mapping[filename_without_extension] = file_id
        
#         page_token = response.get('nextPageToken', None)
#         if page_token is None:
#             break
    
#     return mapping


# def fetch_zip_files_from_folders(drive_service, folder_list):
#     zip_mapping = {}
    
#     for folder in folder_list:
#         folder_id = folder['id']
        
#         page_token = None
#         while True:
#             response = drive_service.files().list(
#                 q=f"'{folder_id}' in parents and mimeType = 'application/x-zip-compressed'",
#                 fields='nextPageToken, files(id)',
#                 pageSize=20,  # This number is larger than the maximum number of files you expect in each folder
#                 pageToken=page_token
#             ).execute()
            
#             zip_files = response.get('files', [])
            
#             if zip_files:
#                 zip_file_id = zip_files[0]['id']  # Assume only one ZIP file exists, take the first one
#                 zip_mapping[folder_id] = zip_file_id
                
#             page_token = response.get('nextPageToken', None)
#             if page_token is None:
#                 break
    
#     return zip_mapping



from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from concurrent.futures import ThreadPoolExecutor, as_completed

def fetch_image_ids_from_folder(drive_service, person_folder_id, subfolder_name):
    image_ids = {}
    mimetypes = {}

    # Get the Grid folder within the person's folder
    grid_folder_id = fetch_subfolder_id_by_name(drive_service, person_folder_id, subfolder_name)
    if grid_folder_id is None:
        return {}

    # Fetch all subfolders under the Grid folder
    subfolders = fetch_subfolders(drive_service, grid_folder_id)
    for folder in subfolders:
        numbered_folder_name = folder['name']
        numbered_folder_id = folder['id']
        ids_in_numbered_folder, mimetypes_in_folder = fetch_image_ids_from_specific_folder(drive_service, numbered_folder_id)
        image_ids[numbered_folder_name] = ids_in_numbered_folder
        mimetypes[numbered_folder_name] = mimetypes_in_folder

    return image_ids, mimetypes

def fetch_subfolder_id_by_name(drive_service, parent_folder_id, subfolder_name):
    try:
        response = drive_service.files().list(
            q=f"'{parent_folder_id}' in parents and mimeType='application/vnd.google-apps.folder' and name='{subfolder_name}'",
            fields='files(id, name)',
            pageSize=10  # Assuming there won't be many folders with the same name
        ).execute()
        for file in response.get('files', []):
            if file['name'] == subfolder_name:
                return file['id']
    except HttpError as error:
        print(f'An error occurred: {error}')
    return None

def fetch_image_ids_from_specific_folder(drive_service, folder_id):
    ids = []
    mimetypes = []
    page_token = None
    while True:
        response = drive_service.files().list(
            q=f"'{folder_id}' in parents and mimeType != 'application/vnd.google-apps.folder'",
            fields='nextPageToken, files(id, mimeType)',
            pageSize=1000,
            orderBy='createdTime',
            pageToken=page_token
        ).execute()
        for file in response.get('files', []):
            ids.append(file['id'])
            mimetypes.append(file['mimeType'])
        page_token = response.get('nextPageToken', None)
        if not page_token:
            break
    return ids, mimetypes

def fetch_subfolders(drive_service, parent_id):
    query = f"'{parent_id}' in parents and mimeType='application/vnd.google-apps.folder'"
    results = drive_service.files().list(q=query, fields="files(id, name)").execute()
    return results.get('files', [])

def fetch_filename_to_id_mapping(drive_service, folder_id):
    mapping = {}
    page_token = None
    fields = 'nextPageToken, files(id, name, mimeType)'
    mime_types = [
        'application/pdf', 
        'application/vnd.openxmlformats-officedocument.presentationml.presentation',
        'application/vnd.ms-powerpoint', 
        'application/x-zip-compressed', 
        'application/zip'
    ]
    while True:
        response = drive_service.files().list(
            q=f"'{folder_id}' in parents and mimeType != 'application/vnd.google-apps.folder'",
            fields=fields,
            pageSize=1000,
            orderBy='name',
            pageToken=page_token
        ).execute()
        for file in response.get('files', []):
            if file['mimeType'] in mime_types:
                filename_without_extension = file['name'].split(".")[0]
                mapping[filename_without_extension] = file['id']
        page_token = response.get('nextPageToken', None)
        if not page_token:
            break
    return mapping

def fetch_zip_files_from_folders(drive_service, folder_list):
    zip_mapping = {}
    for folder in folder_list:
        folder_id = folder['id']
        zip_files = fetch_files_with_mimetype(drive_service, folder_id, ['application/x-zip-compressed', 'application/zip'])
        if zip_files:
            zip_file_id = zip_files[0]['id']  # Assume only one ZIP file exists, take the first one
            zip_mapping[folder_id] = zip_file_id
    return zip_mapping

def fetch_files_with_mimetype(drive_service, folder_id, mime_types):
    """Fetch files from a folder with the specified MIME types."""
    page_token = None
    files = []
    mime_type_query = ' or '.join([f"mimeType = '{mime_type}'" for mime_type in mime_types])
    fields = 'nextPageToken, files(id, name, mimeType)'
    query = f"'{folder_id}' in parents and ({mime_type_query})"
    while True:
        response = drive_service.files().list(
            q=query,
            spaces='drive',
            fields=fields,
            pageToken=page_token
        ).execute()
        files.extend(response.get('files', []))
        page_token = response.get('nextPageToken', None)
        if not page_token:
            break
    return files

# Set up the Drive v3 API
# SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']
# creds = None
# The file token.json stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
# Here you would have the code to handle the credentials, such as:
# if os.path.exists('token.json'):
#    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
# if not creds or not creds.valid:
#    if creds and creds.expired and creds.refresh_token:
#        creds.refresh(Request())
#    else:
#        flow = InstalledAppFlow.from_client_secrets_file(
#            'credentials.json', SCOPES)
#        creds = flow.run_local_server(port=0)
# drive_service = build('drive', 'v3', credentials=creds)

# Example usage:
# person_folder_id = 'your_folder_id_here'
# grid_folder_name = 'Grid'
# image_ids, mime_types = fetch_image_ids_from_folder(drive_service, person_folder_id, grid_folder_name)


def fetch_files(service, folder_id, parent_path, results):
    """
    Fetch files recursively and store in results list.
    """
    query = f"'{folder_id}' in parents"
    fields = 'nextPageToken, files(id, name, mimeType, createdTime, parents)'
    response = service.files().list(q=query, fields=fields).execute()

    for file in response.get('files', []):
        file_path = f"{parent_path}/{file['name']}"
        results.append({
            'id': file['id'],
            'name': file['name'],
            'mimeType': file['mimeType'],
            'createdTime': file['createdTime'],
            'path': file_path
        })

        if file['mimeType'] == 'application/vnd.google-apps.folder':
            fetch_files(service, file['id'], file_path, results)



#NOVAA
def fetch_files_concurrently(service, folder_id, parent_path, results, executor):
    """
    Fetch files recursively and store in results list using concurrent processing.
    """
    query = f"'{folder_id}' in parents"
    fields = 'nextPageToken, files(id, name, mimeType, createdTime, parents)'
    response = service.files().list(q=query, fields=fields).execute()

    futures = []

    for file in response.get('files', []):
        file_path = f"{parent_path}/{file['name']}"
        results.append({
            'id': file['id'],
            'name': file['name'],
            'mimeType': file['mimeType'],
            'createdTime': file['createdTime'],
            'path': file_path
        })

        if file['mimeType'] == 'application/vnd.google-apps.folder':
            # Submit a new task to the executor for each subfolder
            future = executor.submit(fetch_files_concurrently, service, file['id'], file_path, results, executor)
            futures.append(future)

    # Wait for all submitted folder tasks to complete
    for future in as_completed(futures):
        future.result()  # re-raises any exception that occurred in the thread

def get_drive_data(service, root_folder_id):
    results = []
    with ThreadPoolExecutor(max_workers=10) as executor:  # Adjust max_workers as needed
        fetch_files_concurrently(service, root_folder_id, '', results, executor)
    return results