from bs4 import BeautifulSoup
import urllib2
import os

def generating(artist, title, save):
        artist = artist.lower().replace(" ", "%20")
        title = title.lower().replace(" ", "%20")
        generate_url = 'http://azlyrics.com/lyrics/'+artist+'/'+title +'.html'
        print generate_url
        processing(generate_url, artist, title, save)

def processing(generate_url, artist, title, save):
    # response = urllib2.request.urlopen(generate_url)
    try:
        response = urllib2.urlopen(generate_url)
    except urllib2.HTTPError, urllib2.URLError:
        print 'OOOPS. '
    else:
        read_lyrics = response.read()
        soup = BeautifulSoup(read_lyrics)
        lyrics = soup.find_all("div", attrs={"class": None, "id": None})
        lyrics = [x.getText() for x in lyrics]
        printing(artist, title, save, lyrics)

def printing(artist, title, save, lyrics):
    for x in lyrics:
        print x, "\n\n"
    #     print(x, end="\n\n")
    if save == True:
        saving(artist, title, lyrics)
    elif save == False:
        pass

def saving(artist, title, lyrics):
        f = open(os.getcwd() + '/lyrics/beatles/' + title + '.txt', 'w')
        f.write("\n".join(lyrics).encode('utf-8').strip())
        f.close()
