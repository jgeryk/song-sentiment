import urllib2
import json
import re
import os
import lyricsscraper
import time
import random
# Music genre list for an artist: qr['message']['body']['artist_list'][0]['artist']['primary_genres']['music_genre_list']
# 23731396

class MusixMatch:
    def __init__(self, key):
        self.API_KEY = '&apikey=cc6a81644d36b107b7066a6c78383bda' if key is 1 else ' '
        self.ROOT_URL = 'http://api.musixmatch.com/ws/1.1/'
        self.workingDir = os.getcwd()

    def get_artist_id(self, artist):
        query_string = self.ROOT_URL + 'artist.search?q_artist=' + artist + self.API_KEY
        qr = json.loads(urllib2.urlopen(query_string).read())
        return str(qr['message']['body']['artist_list'][0]['artist']['artist_id'])

    def get_albums(self, artist):
        album_ids = []
        artist_id = self.get_artist_id(artist)
        query_string = self.ROOT_URL + 'artist.albums.get?artist_id=' + artist_id + '&s_release_date=desc&g_album_name=1&page_size=100' + self.API_KEY
        qr = json.loads(urllib2.urlopen(query_string).read())
        album_list = qr['message']['body']['album_list']
        for album in album_list:
            # print album['album']['album_name']
            album_ids.append(str(album['album']['album_id']))
        return album_ids

    def get_album_tracks(self, albumid):
        tracks = []
        query_string =  self.ROOT_URL + 'album.tracks.get?album_id=' + albumid + '&page=1&page_size=50' + self.API_KEY
        qr = json.loads(urllib2.urlopen(query_string).read())
        track_list = qr['message']['body']['track_list']
        for track in track_list:
            trackName = track['track']['track_name']
            tracks.append(trackName)
        return tracks

    def get_lyrics(self, trackid):
        lyrics = []
        query_string = self.ROOT_URL + 'track.lyrics.get?track_id=' + trackid + '&' + self.API_KEY
        qr = json.loads(urllib2.urlopen(query_string).read())
        print qr['message']['body']
        return qr['message']['body']['lyrics']['lyrics_body']

    def save_lyric_discography(self, artist):
        albums = self.get_albums(artist)
        tracks = []
        for album_id in albums:
            trackNames = self.get_album_tracks(album_id)
            for track in trackNames:
                tracks.append(track)
        for trackName in tracks:
            print 'Saving ', trackName, ' to text file.'
            artist_no_punc = "animalcollective"
            track_no_punc = re.sub(r'\W+', '', trackName)
            lyricsscraper.generating(artist_no_punc, track_no_punc, True)
            time.sleep(10 + 10 * random.random())
            if random.random() < .02:
                print "Taking a long break"
                time.sleep(30 + 30 * random.random())

if __name__ == "__main__":
    mm = MusixMatch(1)
    mm.save_lyric_discography("animal_collective")
