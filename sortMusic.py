import os
import music_tag
from pathlib import Path
from tkinter import filedialog
from tkinter import * 


# folder = './musique' #default music folder

root = Tk()
root.withdraw()
folder = filedialog.askdirectory(title = "Selectionner le dossier à trier")
root.destroy() 


#function that checks if the file has a music file extension
def isMusic(file):
    musicExt = ['mp3', 'm4a', 'wav', 'webm', 'aac', 'flac'] #list of recognize music extensions. Simply add an ext to this list to include the files in the sort
    file_ext = file.split('.')[-1]  #take only the extension of the input file
    for i in range(len(musicExt)):
        if(file_ext == musicExt[i]):
            return True
    return False



for file in os.listdir(folder): #os.listdir instead of os.walk to not dig into the file tree
    if(os.path.isfile(folder + '/' + file)): #check if current file is file or folder
        if isMusic(file): #check if file has a music extension to continue
            f = music_tag.load_file(folder + '/' + file)
            album = str(f['album']).lower()
            artist = str(f['albumartist']).lower()
            if(album != '' and artist != ''): #sort by artist then album if we have both the informations
                source_path = folder + '/' + file
                dest_path =   folder + '/' + artist + '/' + album + '/'
                Path(dest_path).mkdir(parents=True, exist_ok=True) #create the path if it doesnt exist already
                os.rename(source_path, dest_path + file)
            
            if(album == '' and artist != ''): #only sort by artist if we dont have the album
                source_path = folder + '/' + file
                dest_path =   folder + '/' + artist + '/'
                Path(dest_path).mkdir(parents=True, exist_ok=True)
                os.rename(source_path, dest_path + file)
