# Export Spotify playlists to YouTube

This Python program allows users to seamlessly replicate a Spotify playlist to YouTube. By retrieving song data from a given Spotify playlist, it automatically searches for and creates a matching playlist on YouTube.

### 🤔 Why?
For users who enjoy playlists on Spotify but prefer to listen on YouTube, this tool provides an easy way to transfer music between platforms, saving time and hassle.

## 🚀 Getting Started

### Installation

#### Download or Clone the Project

```shell
git clone https://github.com/ArnauGCC/Spotify_to_YouTube.git
```

Now `cd` into the project directory.
      
---

### Configuration

#### .env

```shell
cp .env.dist .env
```
---

#### Connecting to Spotify's Web API

`Spotify_to_YouTube` needs to connect to Spotify's Web API in order to function.

1. Log in to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard).
2. Click [Create app](https://developer.spotify.com/dashboard/create).
    - Choose name, description, website.
    - Check `Web API`.
3. Click `Save`.
4. Click `Settings`.
5. Copy `Client ID` to [.env](.env.dist) `CLIENT_ID_SP`.
6. Copy `Client Secret` to [.env](.env.dist) `CLIENT_SECRET_SP`.

---

#### Connecting to Spotify's Web API

`Spotify_to_YouTube` also needs to connect to YouTube Data API in order to function.

1. Enable the [YouTube Data API](https://console.cloud.google.com/apis/library/youtube.googleapis.com?hl=es-419) in a project.
2. Click `Create credentials`.
    - Select `OAuth client ID`.
3. Choose `Desktop app` and name.
5. Copy `Customer Secret` to [.env](.env) `CLIENT_SECRET_YT`.
6. Click `Download JSON` and copy the file with the credentials into the project directory.

---

#### Define Spofify and YouTube playlists
You must indicate both playlists, which must already be created.

##### Spotify playlist
1. Go to [Spotify](https://open.spotify.com/) and `Log in`.
2. Search the playlist and click on it.
3. The URL should be something like:
````
https://open.spotify.com/playlist/7klwPuuuSCLIwDDX9JNEiA
````
4. Copy the last fragment of the URL (in the example: `7klwPuuuSCLIwDDX9JNEiA`) to [.env](.env.dist) `SP_PL_ID`.


##### YouTube playlist
1. Go to [YouTube](https://www.youtube.com/) and `Log in`.
2. Search the playlist (or create it if it's necessary) and click on it. (**The playlist must be _empty_**).
3. The URL should be something like:
````
https://www.youtube.com/playlist?list=PLwI6L22yAes6C_aKwgAsWyafCUuLGyIM0
````
4. Copy the last fragment of the URL (in the example: `PLwI6L22yAes6C_aKwgAsWyafCUuLGyIM0`) to [.env](.env.dist) `YT_PL_ID`.

---

It should look like this (but with your own values):

````
CLIENT_ID_SP="5e17746c1f3fa93484c997c71dd4cee8"
CLIENT_SECRET_SP="88c7beb4ea272c1021b585e15949ac4d"
CLIENT_SECRET_YT=client_secret_49654604654-8d8f9d5543787a23a95f4ba46801d819.apps.googleusercontent.com.json,client_secret_54654625346-88da9115afc2d23a6dc2fd8ab1b09f5e.apps.googleusercontent.com.json
SP_PL_ID="3ea3b5abe149c2f39efd79"
YT_PL_ID="6851c72d705366b5896ef-7c9a4c1c7d61"
````
