#build app with pyinstaller --onefile --windowed app.py
#or run with python app.py
#TODO:1 install conda, install ffmpeg and existing packages, try to make same program to mp3 and export with pyinstaller
from tkinter import filedialog
from tkinter import *
import yt_dlp
import music_tag

fields = ('Youtube URL', 'Titre', "Interprète de l'album", 'Album', "Année", "Piste n°", 'Autre artistes (ex: artiste1;artiste2)', 'Genre')
global folder
folder = "./musique/"

def download(entries):
    video_url = (str(entries['Youtube URL'].get())).split("&")[0]
    
    title = (str(entries['Titre'].get()))
    if video_url == '':
        video_url = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
        title = "C'est quoi ça"
    video_info = yt_dlp.YoutubeDL().extract_info(
        url = video_url,download=False
    )
    if(title != ''):
        filename = folder + title + ".m4a"
    else: 
        filename = folder + {video_info['title']} + ".m4a"
    options={
        'format':'m4a',
        'keepvideo':False,
        'outtmpl':filename,
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([video_info['webpage_url']])

    print("Download complete... {}".format(filename))

    tagSong(entries, filename)
    clear(entries)
   
def clear(entries):
    if(var1.get() == 0):
        for entry in entries:
            entries[entry].delete(0, END)
    else:
        for entry in entries:
            if(entry == 'Youtube URL' or entry == 'Titre'):
                entries[entry].delete(0, END)
            if(entry == 'Piste n°'):
                try:
                    trackNumber = (int(entries[entry].get()))
                    entries[entry].delete(0, END)
                    entries[entry].insert(0, trackNumber+1)
                except ValueError:
                    print(ValueError)

def tagSong(entries, filename):
    print(entries, filename)
    tracktitle = (str(entries['Titre'].get()))
    album = (str(entries['Album'].get()))
    albumartist = (str(entries["Interprète de l'album"].get()))
    genre =  (str(entries["Genre"].get()))
    year =  (str(entries["Année"].get()))
    otherArtist = (str(entries["Autre artistes (ex: artiste1;artiste2)"].get()))
    trackNumber = (str(entries["Piste n°"].get()))
    f = music_tag.load_file(filename)

    if(tracktitle != ""):
        f.append_tag('tracktitle', tracktitle) #titre
    if(album != ""):
        f.append_tag('album', album) #album
    if(albumartist != ""):
        f.append_tag('albumartist', albumartist) #interprète de l'album
    if(genre != ""):
        try:
            f.append_tag('genre', str(genre)) #genre
        except ValueError:
            print("Incorrect value for genre")
    if(year != ""):
        try:
            f.raw['year'] = int(year)
        except ValueError:
            # Handle the exception
            print('Please enter an integer')
        
    if(otherArtist != ""):
        f.append_tag('artist', otherArtist)
    if(trackNumber != ""):
        try:
            f.raw['tracknumber'] = int(trackNumber)
        except ValueError:
            # Handle the exception
            print('Please enter an integer')
    f.save()

def makeform(root, fields):
   entries = {}
   for field in fields:
      row = Frame(root)
      lab = Label(row, width=50, text=field+": ", anchor='w')
      ent = Entry(row)
      ent.insert(0,"")
      row.pack(side = TOP, fill = X, ipadx = 150 , pady = 5)
      lab.pack(side = LEFT)
      ent.pack(side = RIGHT, expand = YES, fill = X)
      entries[field] = ent
   return entries

def choseDirectory():
    global folder
    folder = filedialog.askdirectory() + "/"


if __name__ == '__main__':
    root = Tk()
    ents = makeform(root, fields)
    var1 = IntVar()
    c1 = Checkbutton(root, text='Conserver info',variable=var1, onvalue=1, offvalue=0)
    c1.pack(side = LEFT, padx = 5, pady = 5)
    root.bind('<Return>', (lambda event, e = ents: download(e)))
    b1 = Button(root, text = 'Télécharger', command=(lambda e = ents: download(e)))
    b1.pack(side = LEFT, padx = 5, pady = 5)
    b2 = Button(root, text="Changer le dossier de destination", command = choseDirectory)
    b2.pack(side = RIGHT, padx = 5, pady = 5)
    
    root.mainloop()