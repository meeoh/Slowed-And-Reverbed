import json
import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import google.oauth2.credentials

from googleapiclient.http import MediaFileUpload

scopes = ["https://www.googleapis.com/auth/youtube.upload"]

def getCreds():
    # Get credentials and create an API client
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

  with open('token.json') as json_file:
    credentials = json.load(json_file)
  credentials = google.oauth2.credentials.Credentials.from_authorized_user_file('./token.json')
  return credentials


def upload(path, options):
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secrets.json"

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

    print(response)
