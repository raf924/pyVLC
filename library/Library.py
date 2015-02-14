import sqlite3
from PyQt5.QtCore import *
import sys,os
sys.path.append("..")
import vlc
from core import Media

class Library(QObject):
    libraryUpdated = pyqtSignal()
    def __init__(self, parent=None):
        QObject.__init__(self, parent)
        self._songList = []
        self.conn = sqlite3.connect(QStandardPaths.writableLocation(QStandardPaths.MusicLocation)+"/inVLC/library2.db")
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT name FROM sqlite_master")
        tableFound = False
        for row in self.cur:
            if 'library' in row:
                tableFound = True
        if not tableFound:
            self.cur.execute("CREATE TABLE `library` (`Path` TEXT NOT NULL UNIQUE, `Id` INTEGER PRIMARY KEY AUTOINCREMENT);")        
            for i in range(0, 22):
                print(str(vlc.Meta(i)).split(".")[1])
                self.cur.execute("ALTER TABLE library ADD COLUMN {} TEXT".format(str(vlc.Meta(i)).split(".")[1]))
            self.cur.execute("ALTER TABLE library ADD COLUMN Duration NUMBER")
            self.conn.commit()
        self.conn.row_factory = song_factory
        self.cur = self.conn.cursor()
        self.checkExist()
        self.updateSongList()
    
    def checkExist(self):
        self.cur.execute("SELECT Path, Id FROM library")
        for song in self.cur:
            if not os.path.exists(song["Path"]):
                self.removeItem(song["Id"])
    def removeItem(self,id):
        self.cur.execute("DELETE FROM library WHERE Id = ?",(id,))
    def updateSongList(self):
        self._songList = self.library()
        self.libraryUpdated.emit()
    
    def addFile(self,  path):
        media = Media.Media(path)
        self.cur.execute("INSERT INTO library(Path) VALUES(?)", (path, ))
        metadata = media.getMetaData()
        for tag in metadata:
            self.cur.execute("UPDATE library SET {} = ? WHERE Path = ?".format(tag), (metadata[tag],path))
        self.conn.commit()
        self.updateSongList()
        
    def getPath(self,  id):
        for song in self._songList:
            if song["Id"] == id:
                return song["Path"]
                
    def getSong(self,  id):
        d = None
        if isinstance(id,  int):
            for d in self._songList:
                if d["Id"] == id:
                    break
            return d
        elif isinstance(id,  str):
            return Media.Media(str).getMetaData()
        
    def songList(self):
        return self._songList
    def library(self):
        self.cur.execute("SELECT * FROM library")
        fe =  self.cur.fetchall()
        return fe
        
       
def song_factory(cursor, row):
    s= {}
    for idx, col in enumerate(cursor.description):
        s[col[0]] = row[idx]
    return s
    
if __name__=="__main__":
    library = Library()
    library.library()
    sys.exit()
