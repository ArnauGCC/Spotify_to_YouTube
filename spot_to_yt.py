from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
from googleapiclient.discovery import build
import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors


def create_sp_credentials(client_ID, client_Secret):
    client_ID_sp = client_ID
    client_Secret_sp = client_Secret

    client_credential_manager = SpotifyClientCredentials(client_id=client_ID_sp, client_secret=client_Secret_sp)
    sp = spotipy.Spotify(client_credentials_manager=client_credential_manager)
    return sp


def get_sp_songs(sp, pl_id, offs):
    pl_id = "spotify:playlist:" + pl_id
    response = sp.playlist_items(pl_id,
                                 limit=10,
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


def add_songs_to_yt_playlist(ids, yt, playlist_id, fd):
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
        os.write(fd, (yt_id + "\n").encode('utf-8'))


def main():
    
    """
    The following fields must be filled in as specified in README.md file, 
    some commented examples are attached to help the user to find the correct format.
    Each YouTube key allows to add more or less 50 songs and has to be acitvated opening the URL 
    printed in console and pasting the code given.
    """

    CLIENT_ID_SP = ""           #"5e17746c1f3fa93484c997c71dd4cee8"
    CLIENT_SECRET_SP = ""       #"88c7beb4ea272c1021b585e15949ac4d"
    CLIENT_SECRET_YT = [""]     #["client_secret_49654604654-8d8f9d5543787a23a95f4ba46801d819.apps.googleusercontent.com.json",
                                # "client_secret_54654625346-88da9115afc2d23a6dc2fd8ab1b09f5e.apps.googleusercontent.com.json",
                                #]
    SP_PL_ID = ""               #"3ea3b5abe149c2f39efd79"
    YT_PL_ID = ""               #"6851c72d705366b5896ef-7c9a4c1c7d61"

    
    #Create Spotify credentials 
    sp = create_sp_credentials(CLIENT_ID_SP, CLIENT_SECRET_SP)

    #Create a playlist folder with a file to store YT_IDs
    pl_name = sp.playlist(SP_PL_ID, fields='name')['name']
    os.makedirs(pl_name, exist_ok=True)

    yt_ids_path = pl_name + "/YT_IDs.txt"
    fd = os.open(yt_ids_path, os.O_RDWR|os.O_CREAT)

    size = os.path.getsize(yt_ids_path)     #size == number of songs already added in the YT list
    offset = int(size/13)                   #13 == number of Bytes ID in YT (with next line)
    os.lseek(fd, 0, os.SEEK_END)

    #Create YT credentials
    i = 0
    yt = create_yt_credentials(CLIENT_SECRET_YT[i])

    #Get songs information from SP
    songs_inf = get_sp_songs(sp, SP_PL_ID, offset)
    
    while len(songs_inf['items']) > 0 and i < len(CLIENT_SECRET_YT):
        try:
            #Get new YT IDs (10 songs every iteration)
            new_yt_ids = add_new_yt_ids(songs_inf, yt)
            
            #Insert the new songs found to the YT playlist
            add_songs_to_yt_playlist(new_yt_ids, yt, YT_PL_ID, fd)

        except googleapiclient.errors.HttpError:
            i += 1
            if i < len(CLIENT_SECRET_YT):
                yt = create_yt_credentials(CLIENT_SECRET_YT[i])

            else:
                print("More tokens needed: The request cannot be completed because you have exceeded your Youtube fee")

        #Set new offset and get songs information from SP
        offset = int(os.path.getsize(yt_ids_path)/13)
        songs_inf = get_sp_songs(sp, SP_PL_ID, offset)
        print(offset, "/", songs_inf['total'], "songs added")

    print("NEW SONGS NOT FOUND")


if __name__ == "__main__":
    main()