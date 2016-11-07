import urllib2
import json

# Music genre list for an artist: qr['message']['body']['artist_list'][0]['artist']['primary_genres']['music_genre_list']

class MusixMatch:
    def __init__(self, key):
        self.API_KEY = '&apikey=cc6a81644d36b107b7066a6c78383bda' if key is 1 else ' '
        self.ROOT_URL = 'http://api.musixmatch.com/ws/1.1/'

    def get_artist_id(self, artist):
        query_string = self.ROOT_URL + 'artist.search?q_artist=' + artist + self.API_KEY
        qr = json.loads(urllib2.urlopen(query_string).read())
        return str(qr['message']['body']['artist_list'][0]['artist']['artist_id'])

    def get_albums(self, artist):
        album_ids = []
        artist_id = self.get_artist_id(artist)
        query_string = self.ROOT_URL + 'artist.albums.get?artist_id=' + artist_id + '&s_release_date=desc&g_album_name=1' + self.API_KEY
        qr = json.loads(urllib2.urlopen(query_string).read())
        album_list = qr['message']['body']['album_list']
        for album in album_list:
            album_ids.push(album['album']['album_id'])
        return album_list

    def get_album_tracks(self, album):
        pass

    def get_lyrics(self, trackid):
        pass

    def get_lyric_discography(artist):
        pass
