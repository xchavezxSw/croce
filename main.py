#!/usr/bin/python
#httplib lo uso para hacer las peticiones
import httplib2
#os lo uso para obtener la ruta actual
import os
#sys lo uso para obtener variables de sistema
import sys
#enviowpp lo uso para enviar los wpp por medio de navegar (para no pagar una api)
import EnvioWpp as ew
#apiclient es la api de google para acceder a los clients
import apiclient as ap
#oauth2 es para autentificarme oauth2.(para iniciar session en youtube)
#esto me crea el main.py-oauth2.json y ahi tengo mi cuenta de youtube, donde tengo permisos para el youtube de comunidad cristiana
#borrando este archivo. te vas a podes loguear en cualquier otro
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow
import datetime


def fecha():
  #Proceso que calcula la fecha a levantar
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


########################################################################################################## OAUTH2
# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account.
CLIENT_SECRETS_FILE = "client_secret.json"
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
##########################################################################################################

# Create a liveBroadcast resource and set its title, scheduled start time,
# scheduled end time, and privacy status.
def insert_broadcast(youtube, options):
  #creo el link
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

def upload_thumbnail(youtube, video_id, file):
#subo la imagen del dia
  youtube.thumbnails().set(
    videoId=video_id,
    media_body=file
  ).execute()


if __name__ == "__main__":
  #calculo fecha,titulo,inicio y fin de reunion segn dia a ejecutar
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
  # mme autentifico con youtube
  youtube = get_authenticated_service(args)

  try:
    #creo el link
    broadcast_id = insert_broadcast(youtube, args)
    #actualizo la imagen
    upload_thumbnail(youtube, broadcast_id, file)
    if broadcast_id != '':
      #envio el wpp con selenium
      ew.envioWpp(dia,"https://www.youtube.com/watch?v="+broadcast_id)
  except (ap.http.HttpError):
    print ("An HTTP error %d occurred:\n")
