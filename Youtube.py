import json
import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import google.oauth2.credentials

from googleapiclient.http import MediaFileUpload

scopes = ["https://www.googleapis.com/auth/youtube.upload"]


# Code to generate the required token.json, in order to run this you need client_secrets.json from youtubes api
# client_secrets_file = "client_secrets.json"
# flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
#     client_secrets_file, scopes)
# credentials = flow.run_console()

# creds_data = {
#   'token': credentials.token,
#   'refresh_token': credentials.refresh_token,
#   'token_uri': credentials.token_uri,
#   'client_id': credentials.client_id,
#   'client_secret': credentials.client_secret,
#   'scopes': credentials.scopes
# }
# del creds_data['token']
# with open('token.json', 'w') as outfile:
#     json.dump(creds_data, outfile)


def getCreds():
  with open('token.json') as json_file:
    credentials = json.load(json_file)
  credentials = google.oauth2.credentials.Credentials.from_authorized_user_file('./token.json')
  return credentials


def upload(path, options):
    if not os.path.exists("token.json"):
      print("token.json does not exist, not uploading to youtube")
      return
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"

    credentials = getCreds()
    youtube = googleapiclient.discovery.build(
      api_service_name,
      api_version,
      credentials=credentials
    )

    request = youtube.videos().insert(
      part="snippet,status",
      body=options,
      media_body=MediaFileUpload(path)
    )
    response = request.execute()
    return response
