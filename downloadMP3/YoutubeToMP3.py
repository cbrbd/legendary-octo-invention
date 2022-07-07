#build app with pyinstaller --onefile --windowed YoutubeToMP3.py
#or run with python YoutubeToMP3.py
import os
import eyed3
from eyed3.core import Date 
from tkinter import filedialog
from tkinter import *

import urllib.request

#temporary add ffmpeg to bath
binPath = os.getcwd() + '\libav' + "\\" + "usr" + '\\bin' #bin folder location of libav
PATH = os.environ.get('PATH') #curent PATH
os.environ['PATH'] = PATH + ";" + binPath #update PATH

#this is imported after path was defined, otherwise yt_dlp will not find ffmpeg and program will crash
import yt_dlp

#list of the fields in the tkinter form
fields = ('Youtube URL', 'Titre', "Interprète de l'album", 'Album', "Année", "Piste n°", 'Autre artistes (ex: artiste1;artiste2)', 'Genre','n° Disque (Nombre entier)', 'Pochette')

#folder where the music will be placed, default is ./musique/
global folder
folder = "./musique/"


#principal function, download at mp3 format, then calls tag & clear function
def download(entries):

    orig_ext = '.webm' #webm is the file format before ffmpeg process
    final_ext = '.mp3' #output format

    #retrieve the URL, the split("&") is here to remove options like timestamps, playlist etc.
    video_url = (str(entries['Youtube URL'].get())).split("&")[0]
    
    #retrieve name given by user
    title = (str(entries['Titre'].get()))

    #if no url, do some nasty stuff
    if video_url == '':
        video_url = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
        title = "C'est quoi ça"

    video_info = yt_dlp.YoutubeDL().extract_info(
        url = video_url,download=False
    )

    #File will be named as the title of the song if given by user in the folder given
    if(title != ''):
        filename = folder + title
    #else, name will be the youtube title
    else: 
        filename = folder + {video_info['title']}

    #options of the download
    options={
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192'
        }],
        'keepvideo':False,
        'outtmpl':filename + orig_ext,
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([video_info['webpage_url']])

    print("Download complete... {}".format(filename))

    #tag the song
    tagSong(entries, filename + final_ext)

    #clear the field
    clear(entries)
   
def clear(entries):
    #clear the field of the form if checkbox isnt ticked
    if(var1.get() == 0):
        for entry in entries:
            entries[entry].delete(0, END)
    else:
        for entry in entries:
            if(entry == 'Youtube URL' or entry == 'Titre'): 
                entries[entry].delete(0, END) #if checkbox is ticked, delete URL and Title Field
            if(entry == 'Piste n°'): 
                try:
                    trackNumber = (int(entries[entry].get()))
                    entries[entry].delete(0, END)
                    entries[entry].insert(0, trackNumber+1) #If checkbox is ticked, increment track number by 1
                except ValueError:
                    print(ValueError)


#function called by the download function once download is over.
#Tags the file with user info
def tagSong(entries, filename):
    
    #Fetch every info from the form
    tracktitle = (str(entries['Titre'].get()))
    album = (str(entries['Album'].get()))
    albumartist = (str(entries["Interprète de l'album"].get()))
    genre =  (str(entries["Genre"].get()))
    year =  (str(entries["Année"].get()))
    otherArtist = (str(entries["Autre artistes (ex: artiste1;artiste2)"].get()))
    trackNumber = (str(entries["Piste n°"].get()))
    albumcover = (str(entries["Pochette"].get()))
    discnumber = (str(entries["n° Disque (Nombre entier)"].get()))

    print(year, type(year), year != "")
    #load file, for mp3 we can use eyed3
    audiofile = eyed3.load(filename)

    print(dir(audiofile.tag))

    #set tag if defined and valid
    if(tracktitle != ""):
        audiofile.tag.title = tracktitle
    if(album != ""):
        audiofile.tag.album = album
    if(albumartist != ""):
        audiofile.tag.album_artist = albumartist
    if(genre != ""):
        try:
            audiofile.tag.genre = str(genre)
        except ValueError:
            print('Incorrect value for genre')
    if(year != ""):
        try:
            audiofile.tag.recording_date = Date(int(year))
        except:
            print("error")
        # audiofile.tag.year = year
    if(otherArtist != ""):
        audiofile.tag.artist = otherArtist

    if(trackNumber != ""):
        try:
            audiofile.tag.track_num = int(trackNumber)     
        except ValueError:
            print('Please enter an integer')
    
    if(discnumber != ""):
        try:
            audiofile.tag.disc_num = discnumber
        except:
            print("Error when setting disc number tag")


    if(albumcover != ""):
        #check if cover is link
        if(albumcover[0:4] == 'http'):
            try:
                audiofile.tag.images.set(3, urllib.request.urlopen(albumcover).read(), 'image/jpeg')
            except:
                print("lol")
        else:
            try:
                audiofile.tag.images.set(3, open(albumcover, 'rb').read(), 'image/jpeg')
            except FileNotFoundError:
                print(FileNotFoundError)

    #save the tags
    audiofile.tag.save(version=eyed3.id3.ID3_V2_3)



#Function called on main to build the form with given fields
def makeform(root, fields):
    entries = {}
    for field in fields:
        row = Frame(root)
        lab = Label(row, width=50, text=field+": ", anchor='w', padx = 5)
        ent = Entry(row)
        ent.insert(0,"")
        row.pack(side = TOP, fill = X, ipadx = 150 , pady = 5)
        lab.pack(side = LEFT)
        ent.pack(side = RIGHT, expand = YES, fill = X, padx = 5)
        entries[field] = ent
    return entries

#called on button click to select directory where music will be downloaded
def choseDirectory():
    global folder
    folder = filedialog.askdirectory() + "/"

#called on album cover button press
def choseAlbumCover(entries):
    cover = filedialog.askopenfilename()
    entries['Pochette'].delete(0, END)
    entries['Pochette'].insert(0, cover)

#call on default thumbnail button
def defaultThumbnail(entries):

    video_id = ((str(entries['Youtube URL'].get())).split("&")[0]).split("=")[1] #fetch the url from the form and split it to only keep the id
    cover = 'https://img.youtube.com/vi/' + video_id + '/maxresdefault.jpg' #default url to get youtube thumbnails
    entries['Pochette'].delete(0, END) #delete previous art cover field
    entries['Pochette'].insert(0, cover) #fill it with the http link

#main
if __name__ == '__main__':
    root = Tk()
    root.title('Youtube Downloader')
    ents = makeform(root, fields)

    #add two buttons to select art cover after form build
    row = Frame(root)
    lab = Label(row, width=50, anchor='w')
    coverButton = Button(row, text="Selectionner une illustration", command =(lambda e = ents: choseAlbumCover(e)))
    thumbnailButton = Button(row, text="Utiliser la miniature youtube comme illustration", command = (lambda e = ents: defaultThumbnail(e)))

    row.pack(side = TOP, ipadx = 150 , pady = 5)
    lab.pack(side = LEFT)
    coverButton.pack(side = RIGHT, padx = 5)
    thumbnailButton.pack(side = RIGHT, padx=5)


    var1 = IntVar() #checkbox variable
    c1 = Checkbutton(root, text='Conserver info',variable=var1, onvalue=1, offvalue=0)
    c1.pack(side = LEFT, padx = 5, pady = 5)

    #call download on Enter button
    root.bind('<Return>', (lambda event, e = ents: download(e)))
    
    b1 = Button(root, text = 'Télécharger', command=(lambda e = ents: download(e)))
    b1.pack(side = LEFT, padx = 5, pady = 5)
    b2 = Button(root, text="Changer le dossier de destination", command = choseDirectory)
    b2.pack(side = RIGHT, padx = 5, pady = 5)
    
    
    root.mainloop()