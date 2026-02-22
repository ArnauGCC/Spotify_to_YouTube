from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
from googleapiclient.discovery import build
import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from dotenv import find_dotenv, load_dotenv


def create_sp_credentials(client_ID, client_Secret):
    client_ID_sp = client_ID
    client_Secret_sp = client_Secret

    client_credential_manager = SpotifyClientCredentials(client_id=client_ID_sp, client_secret=client_Secret_sp)
    sp = spotipy.Spotify(client_credentials_manager=client_credential_manager)
    return sp


def get_sp_songs(sp, pl_id, offs, lim):
    pl_id = "spotify:playlist:" + pl_id
    response = sp.playlist_items(pl_id,
                                 limit=lim,
                                 offset=offs,
                                 fields='items.track.name,items.track.artists.name,total',
                                 #additional_types=['episode']
                                 )
    return response


def create_yt_credentials(client_secret):
    scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = os.path.dirname(os.path.abspath(__file__)) + "\\" + client_secret

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()
    yt = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)
    
    return yt


def add_new_yt_ids(songs, yt):
    #For each song (name + artists) get the ID of a matching YT video
    new_yt_ids = []
    for song in songs['items']:
        search_yt = song['track']['name'] + " "
        for artist in song['track']['artists']:
            search_yt += artist['name'] + " "
        #print(search_yt)            #Uncomment this line to print the new songs added

        request = yt.search().list(q=search_yt,
                                    part="id",
                                    type="video",
                                    maxResults=1,
                                    order="relevance")
        response_yt = request.execute()
        new_yt_ids.append(response_yt["items"][0]["id"]["videoId"])
    return new_yt_ids


def add_songs_to_yt_playlist(ids, yt, playlist_id):
    for yt_id in ids:
        request = yt.playlistItems().insert(
            part="snippet",
            body={
                "snippet": {
                    "playlistId": playlist_id,
                    "resourceId": {
                        "videoId": yt_id,
                        "kind": "youtube#video"
                    }
                }
            }
        )
        response = request.execute()

def get_offset(yt, pl_id):
    return int(yt.playlists().list(
        part="contentDetails",
        id=pl_id
    ).execute()['items'][0]['contentDetails']['itemCount'])

def main():
    dotenv_path = find_dotenv()
    load_dotenv(dotenv_path)

    CLIENT_ID_SP = os.getenv("CLIENT_ID_SP")
    CLIENT_SECRET_SP = os.getenv("CLIENT_SECRET_SP")
    CLIENT_SECRET_YT = os.getenv("CLIENT_SECRET_YT").split(",")
    SP_PL_ID = os.getenv("SP_PL_ID")
    YT_PL_ID = os.getenv("YT_PL_ID")
    LIM = 10
    
    #Create Spotify credentials 
    sp = create_sp_credentials(CLIENT_ID_SP, CLIENT_SECRET_SP)

    #Create YT credentials and set offset
    i = 0
    yt = create_yt_credentials(CLIENT_SECRET_YT[i])    
    offset = get_offset(yt, YT_PL_ID)

    #Get songs information from SP
    songs_inf = get_sp_songs(sp, SP_PL_ID, offset, LIM)
    
    while len(songs_inf['items']) > 0 and i < len(CLIENT_SECRET_YT):
        try:
            #Get new YT IDs (10 songs every iteration)
            new_yt_ids = add_new_yt_ids(songs_inf, yt)
            
            #Insert the new songs found to the YT playlist
            add_songs_to_yt_playlist(new_yt_ids, yt, YT_PL_ID)

            #Set new offset
            offset += LIM

        except googleapiclient.errors.HttpError:
            i += 1
            if i < len(CLIENT_SECRET_YT):
                yt = create_yt_credentials(CLIENT_SECRET_YT[i])
                offset = get_offset(yt, YT_PL_ID)

            else:
                print("More tokens needed: The request cannot be completed because you have exceeded your Youtube fee")

        #Get songs information from SP
        songs_inf = get_sp_songs(sp, SP_PL_ID, offset, LIM)
        print(offset, "/", songs_inf['total'], "songs added")

    print("NEW SONGS NOT FOUND")


if __name__ == "__main__":
    main()