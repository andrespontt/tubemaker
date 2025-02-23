import os

import google_auth_httplib2
import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"

def upload_video(file, title, description, category, keywords, privacyStatus):
    """
    Uploads a video to YouTube.
    """
    # Disable OAuthlib verification.
    # (https://github.com/googleapis/google-api-python-client/issues/890)
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    client_secrets_file = "client_secret.json"

    # Get credentials and create an API client
    flow = google_auth_httplib2.flow_from_clientsecrets(
        client_secrets_file, SCOPES)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        API_SERVICE_NAME, API_VERSION, credentials=credentials)

    body = {
        "snippet": {
            "categoryId": category,
            "description": description,
            "title": title
        },
        "status": {
            "privacyStatus": privacyStatus
        }
    }

    # Call the API's videos.insert method to create and upload the video.
    media = MediaFileUpload(file, mimetype='video/*', resumable=True)
    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media=media
    )

    response = None
    try:
        response = request.execute()
        print(response)
    except googleapiclient.errors.HttpError as e:
        print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))

    return response

if __name__ == '__main__':
    # Set arguments
    file = "video.mp4"
    title = "My Video"
    description = "This is my video"
    category = "22"
    keywords = "video, fun"
    privacyStatus = "private"

    upload_video(file, title, description, category, keywords, privacyStatus)
