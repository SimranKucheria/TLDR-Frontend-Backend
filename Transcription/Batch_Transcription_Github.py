import logging
import sys
import requests
import time
import swagger_client as cris_client
import config
from azure.storage.blob.baseblobservice import BaseBlobService
from azure.storage.blob import BlobServiceClient, BlobBlock
import os
import moviepy.editor as mp
from azure.storage.blob.models import BlobPermissions
from datetime import datetime, timedelta
import uuid
from azure.core.exceptions import ResourceNotFoundError
from pydub import AudioSegment

# Configure Logging
logging.basicConfig(stream=sys.stdout, format="%(asctime)s %(message)s", datefmt="%d/%m/%Y %I:%M:%S %p %Z")

container_name = 'forlecture' # for example, `test`
account_name = config.storage_name
account_key = config.storage_key

video_clip = "../VideoSummarization/Data/videos/Lecture 30-20211028 0641-1.mp4"

clip = mp.VideoFileClip(video_clip)
blob_name = video_clip.split("/")[-1][:-3]+'mp3' # for example, `whatstheweatherlike.wav`
# Insert Local Audio File Path

block_list=[]
chunk_size=8192

if not os.path.isfile(blob_name):
    clip.audio.write_audiofile(blob_name)
    sound = AudioSegment.from_mp3(blob_name)
    sound = sound.set_channels(1)
    sound.export(blob_name, format="mp3")
    
blob_service_client = BlobServiceClient.from_connection_string(config.connect_str)
blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

try: 
    blob_client.get_blob_properties()
    print("File exists")
except ResourceNotFoundError:
    print("\nUploading to Azure Storage as blob:\n\t" + blob_name)
    with open(blob_name, "rb") as data:
        while True:
            read_data = data.read(chunk_size)
            if not read_data:
                break
            blk_id = str(uuid.uuid4())
            blob_client.stage_block(block_id=blk_id,data=read_data) 
            block_list.append(BlobBlock(block_id=blk_id))
    blob_client.commit_block_list(block_list)


        
blob_service = BaseBlobService(
    account_name=account_name,
    account_key=account_key
)

sas_token = blob_service.generate_blob_shared_access_signature(container_name, blob_name, permission=BlobPermissions.READ, expiry=datetime.utcnow() + timedelta(hours=1))
url_with_sas = blob_service.make_blob_url(container_name, blob_name, sas_token=sas_token)

# TODO: Paste your keys and URLs into their respective variables

# Your subscription key and region for the speech service
SUBSCRIPTION_KEY = config.api_key
SERVICE_REGION = "centralindia"

NAME = blob_name[:-3]
DESCRIPTION = "Lecture Video"

LOCALE = "en-US"
RECORDINGS_BLOB_URI = url_with_sas

def transcribe_from_single_blob(uri, properties):
    """
    Transcribe a single audio file located at `uri` using the settings specified in `properties`
    using the base model for the specified locale.
    """
    transcription_definition = cris_client.Transcription(
        display_name=NAME,
        description=DESCRIPTION,
        locale=LOCALE,
        content_urls=[uri],
        properties=properties
    )

    return transcription_definition

def _paginate(api, paginated_object):
    """
    The autogenerated client does not support pagination. This function returns a generator over
    all items of the array that the paginated object `paginated_object` is part of.
    """
    yield from paginated_object.values
    typename = type(paginated_object).__name__
    auth_settings = ["apiKeyHeader", "apiKeyQuery"]
    while paginated_object.next_link:
        link = paginated_object.next_link[len(
            api.api_client.configuration.host):]
        paginated_object, status, headers = api.api_client.call_api(link, "GET",
                                                                    response_type=typename, auth_settings=auth_settings)

        if status == 200:
            yield from paginated_object.values
        else:
            raise Exception(
                f"could not receive paginated data: status {status}")

def transcribe():
    logging.info("Starting transcription client...")

    # configure API key authorization: subscription_key
    configuration = cris_client.Configuration()
    configuration.api_key["Ocp-Apim-Subscription-Key"] = SUBSCRIPTION_KEY
    configuration.host = f"https://{SERVICE_REGION}.api.cognitive.microsoft.com/speechtotext/v3.0"

    # create the client object and authenticate
    client = cris_client.ApiClient(configuration)

    # create an instance of the transcription api class
    api = cris_client.DefaultApi(api_client=client)

    # Specify transcription properties by passing a dict to the properties parameter. See
    # https://docs.microsoft.com/azure/cognitive-services/speech-service/batch-transcription#configuration-properties
    # for supported parameters.
    properties = {
        "wordLevelTimestampsEnabled": True,
        "diarizationEnabled": True,
        "destinationContainerUrl": "https://btspeechtotext.blob.core.windows.net/forlecture?sp=rwl&st=2022-01-12T11:37:16Z&se=2022-01-12T19:37:16Z&spr=https&sv=2020-08-04&sr=c&sig=qxaLZcA16sEF5l0P3Y9cHHVQM7CpGLTkI9yxXIiq9uk%3D", # TODO: Supply SAS URI
        "timeToLive": "PT1H"
    }
    
    transcription_definition = transcribe_from_single_blob(RECORDINGS_BLOB_URI, properties)

    created_transcription, status, headers = api.create_transcription_with_http_info(
        transcription=transcription_definition)

    # get the transcription Id from the location URI
    transcription_id = headers["location"].split("/")[-1]

    # Log information about the created transcription. If you should ask for support, please
    # include this information.
    logging.info(
        f"Created new transcription with id '{transcription_id}' in region {SERVICE_REGION}")

    logging.info("Checking status.")

    completed = False

    while not completed:
        # wait for 5 seconds before refreshing the transcription status
        time.sleep(5)

        transcription = api.get_transcription(transcription_id)
        logging.info(f"Transcriptions status: {transcription.status}")

        if transcription.status in ("Failed", "Succeeded"):
            completed = True

        if transcription.status == "Succeeded":
            pag_files = api.get_transcription_files(transcription_id)
            for file_data in _paginate(api, pag_files):
                if file_data.kind != "Transcription":
                    continue

                audiofilename = file_data.name
                results_url = file_data.links.content_url
                results = requests.get(results_url)
                logging.info(
                    f"Results for {audiofilename}:\n{results.content.decode('utf-8')}")
        elif transcription.status == "Failed":
            logging.info(
                f"Transcription failed: {transcription.properties.error.message}")

if __name__ == "__main__":
    transcribe()
