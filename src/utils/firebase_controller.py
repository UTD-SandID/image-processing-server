import firebase_admin
from firebase_admin import credentials, storage, db


cred = credentials.Certificate('utils/certificates/utdsand-id-firebase-admins.json')
firebase_admin.initialize_app(cred, {'storageBucket': 'utdsand-id.appspot.com'})


def firebase_image_upload(image_path):
    bucket = storage.bucket()
    blob_name = "SandImages/" + image_path.split("/")[-1]
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(image_path)
    return blob.public_url
