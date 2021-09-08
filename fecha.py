#!/usr/bin/python

import httplib2
import os
import sys
import EnvioWpp as ew
import apiclient as ap
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow
import datetime
def fecha():
  today = datetime.date.today()
  miercoles = today + datetime.timedelta( (2-today.weekday()) % 7 )
  domingo = today + datetime.timedelta( (6-today.weekday()) % 7 )
  if today.isoweekday() <=3:
      titulo="Reunión virtual - Miercoles "+str(miercoles.day)+" de Septiembre"
      file="./fotos/"+str(miercoles.day)+".jpg"
      StartscheduleTime='2021-'+str(miercoles.month).zfill(2)+'-'+str(miercoles.day)+'T23:30:00.000Z'
      finishscheduleTime = '2021-' + str(miercoles.month).zfill(2) + '-' + str(int(miercoles.day)+1) + 'T02:30:00.000Z'
      return miercoles,titulo,file,StartscheduleTime,finishscheduleTime,"Miercoles"
  else:
      titulo = "Reunión virtual - Domingo "+str(domingo.day)+" de Septiembre"
      file = "./fotos/"+str(domingo.day) + ".jpg"
      StartscheduleTime='2021-'+str(domingo.month).zfill(2)+'-'+str(domingo.day)+'T13:30:00.000Z'
      finishscheduleTime = '2021-' + str(domingo.month).zfill(2) + '-' + str(domingo.day) + 'T16:30:00.000Z'
      return domingo,titulo,file,StartscheduleTime,finishscheduleTime,"Domingo"
# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret. You can acquire an OAuth 2.0 client ID and client secret from
# the {{ Google Cloud Console }} at
# {{ https://cloud.google.com/console }}.
# Please ensure that you have enabled the YouTube Data API for your project.
# For more information about using OAuth2 to access the YouTube Data API, see:
#   https://developers.google.com/youtube/v3/guides/authentication
# For more information about the client_secrets.json file format, see:
#   https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
CLIENT_SECRETS_FILE = "client_secret.json"

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account.
YOUTUBE_READ_WRITE_SCOPE = "https://www.googleapis.com/auth/youtube"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# This variable defines a message to display if the CLIENT_SECRETS_FILE is
# missing.
MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0
To make this sample run you will need to populate the client_secrets.json file
found at:
   %s
with information from the {{ Cloud Console }}
{{ https://cloud.google.com/console }}
For more information about the client_secrets.json file format, please visit:
https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
""" % os.path.abspath(os.path.join(os.path.dirname(__file__),
                                   CLIENT_SECRETS_FILE))

def get_authenticated_service(args):
  flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE,
    scope=YOUTUBE_READ_WRITE_SCOPE,
    message=MISSING_CLIENT_SECRETS_MESSAGE)

  storage = Storage("%s-oauth2.json" % sys.argv[0])
  credentials = storage.get()

  if credentials is None or credentials.invalid:
    credentials = run_flow(flow, storage, args)

  return ap.discovery.build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    http=credentials.authorize(httplib2.Http()))

# Create a liveBroadcast resource and set its title, scheduled start time,
# scheduled end time, and privacy status.
def insert_broadcast(youtube, options):
  insert_broadcast_response = youtube.liveBroadcasts().insert(
    part="snippet,status",
    body=dict(
      snippet=dict(
        title=options.broadcast_title,
        description="Reunión virtual de la Comunidad Cristiana de la zona sur de Bs. As.",
        categoryId="10",
        scheduledStartTime=options.start_time,
        scheduledEndTime=options.end_time
      ),
      status=dict(
        privacyStatus=options.privacy_status
      )
    )
  ).execute()

  snippet = insert_broadcast_response["snippet"]

  print ("Broadcast '%s' with title '%s' was published at '%s'." % (
    insert_broadcast_response["id"], snippet["title"], snippet["publishedAt"]))
  return insert_broadcast_response["id"]

# Create a liveStream resource and set its title, format, and ingestion type.
# This resource describes the content that you are transmitting to YouTube.

def UPDATECATEGORY(youtube, video_id):
    videos_update_response = youtube.videos().update(
        part='snippet',
        body=dict(
            snippet=dict(
                    categoryId="10"),
            id=video_id
        )).execute()

def insert_stream(youtube, options):
  insert_stream_response = youtube.liveStreams().insert(
    part="snippet,cdn",
    body=dict(
      snippet=dict(
        title=options.stream_title
      ),
      cdn=dict(
        format="1080p",
        ingestionType="rtmp"
      )
    )
  ).execute()

  snippet = insert_stream_response["snippet"]

  print ("Stream '%s' with title '%s' was inserted." % (
    insert_stream_response["id"], snippet["title"]))
  return insert_stream_response["id"]

# Bind the broadcast to the video stream. By doing so, you link the video that
# you will transmit to YouTube to the broadcast that the video is for.
def bind_broadcast(youtube, broadcast_id, stream_id):
  bind_broadcast_response = youtube.liveBroadcasts().bind(
    part="id,contentDetails",
    id=broadcast_id,
    streamId=stream_id
  ).execute()

  print ("Broadcast '%s' was bound to stream '%s'." % (
    bind_broadcast_response["id"],
    bind_broadcast_response["contentDetails"]["boundStreamId"]))

if __name__ == "__main__":
  fecha,titulo,file,StartscheduleTime,finishscheduleTime,dia=fecha()
  argparser.add_argument("--broadcast-title", help="Broadcast title",
    default=titulo)
  argparser.add_argument("--privacy-status", help="Broadcast privacy status",
    default="public")
  argparser.add_argument("--start-time", help="Scheduled start time",
    default=StartscheduleTime)
  argparser.add_argument("--end-time", help="Scheduled end time",
    default=finishscheduleTime)
  argparser.add_argument("--stream-title", help="Stream title",
    default=titulo)
  args = argparser.parse_args()

  youtube = get_authenticated_service(args)

  try:
     UPDATECATEGORY(youtube, "WWRQBsujoLk")
  except (ap.http.HttpError):
    print ("An HTTP error %d occurred:\n")
