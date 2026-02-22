# Export playlists

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
5. Copy `Client ID` to [.env](.env) `CLIENT_ID_SP`.
6. Copy `Client Secret` to [.env](.env) `CLIENT_SECRET_SP`.

---

#### Connecting to Spotify's Web API

`Spotify_to_YouTube` needs to connect to YouTube Data API in order to function.

1. Enable the [YouTube Data API](https://console.cloud.google.com/apis/library/youtube.googleapis.com?hl=es-419) in a project.
2. Click `Create credentials`.
    - Select `OAuth client ID`.
3. Choose `Desktop app` and name.
5. Copy `Customer Secret` to [.env](.env) `CLIENT_SECRET_YT`.
6. Click `Download JSON` and copy the file with the credentials into the project directory.
