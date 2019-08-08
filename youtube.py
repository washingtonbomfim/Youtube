#!/usr/bin/python

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
from pytube import YouTube
import moviepy.editor as mp
import os
from flask import Flask, jsonify, request
import socket
import pprint as p

# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = "AIzaSyBETnJnSvZ7Q8AAyJNhFaZUwb09JM7r98Q"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

app = Flask(__name__)

@app.route("/")
def baixa_musica():

    try:
       youtube_search(request.json)
    except HttpError as e:
       print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))

    return jsonify({'teste':'ok'})

def youtube_search(options):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)
    musica = options['musica'] + ' audio'
    #musica = 'kane brown Like a Rodeo audio'
    search_response = youtube.search().list(
        q=musica,
        part="id,snippet",
        maxResults=1
    ).execute()

    videos = []

    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            videos.append("%s - https://www.youtube.com/watch?v=%s" % (search_result["snippet"]["title"],
                                                                     search_result["id"]["videoId"]))

        # elif search_result["id"]["kind"] == "youtube#playlist":
        #   playlists.append("%s (%s)" % (search_result["snippet"]["title"],
        #                                 search_result["id"]["playlistId"]))

    try:
        YouTube('http://youtube.com/watch?v=' + search_result["id"]["videoId"]).streams.first().download()

        pasta = '/home/washington/PycharmProjects/Youtube/'
        caminhos = [os.path.join(pasta, nome) for nome in os.listdir(pasta)]

        arquivos = [arq for arq in caminhos if os.path.isfile(arq)]
        musica_mp4 = [arq for arq in arquivos if arq.lower().endswith(".mp4")]
        print(musica_mp4)
        musica_mp3 = mp.VideoFileClip(musica_mp4[0]).subclip(0, 50)
        print(musica_mp3)
        musica_mp3.audio.write_audiofile(musica_mp4[0][:-1]+'3')
    except HttpError as e:
        print(e)

if __name__ == "__main__":
    #ip_host = socket.gethostbyname(socket.gethostname())
    # argparser.add_argument("--q", help="Search term", default="eminem the real slim shady audio")
    # argparser.add_argument("--max-results", help="Max results", default=1)
    # args = argparser.parse_args()
    app.run(host='192.168.2.75', port=5000)
    # try:
    #    youtube_search(args)
    # except HttpError as e:
    #    print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
