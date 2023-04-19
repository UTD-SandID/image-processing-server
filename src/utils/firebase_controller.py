import firebase_admin
from firebase_admin import credentials, storage, db


cred = credentials.Certificate('utils/certificates/utdsand-id-firebase-admins.json')
firebase_admin.initialize_app(cred, {'storageBucket': 'utdsand-id.appspot.com'})


def firebase_image_upload(image_path):
    bucket = storage.bucket()
    blob = bucket.blob(image_path)
    blob.upload_from_filename(image_path)

#def store_firebase_image_url(image_url):
#    ref = db.reference('images')
#    ref.push({
#        'url': image_url
#    })