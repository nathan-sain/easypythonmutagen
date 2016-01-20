
import os
import shutil
import mutagen
from mutagen import easymp4

# tags are intentionally restricted; otherwise a typo like o['aartist'] would succeed silently.
# use Mutagen directly if you want to intentionally add rare or custom fields.

class EasyPythonMutagen(object):
    pass

class EasyPythonMutagenFlac(object):
    ''' An interface like EasyId3, but for Flac files.'''
    
    def __init__(self, filename):
        from mutagen import flac
        self.obj = flac.FLAC(filename)
        self.map = {
            'desc': 'desc',
            'description': 'desc',
            'album': 'album',
            'comment': 'comment',
            'artist': 'artist',
            'title': 'title',
            'tracknumber': 'tracknumber',
            'discnumber': 'discnumber',
            'albumartist': 'albumartist',
            'composer': 'composer',
            'disccount': 'disccount',
            'tracktotal': 'tracktotal',
            'date': 'date',
            'genre': 'genre',
            'website': 'www',
            }
        
    def __getitem__(self, key):
        return self.obj[self.map[key]]
            
    def __setitem__(self, key, val):
        self.obj[self.map[key]] = val
            
    def __contains__(self, key):
        return key in self.map and self.map[key] in self.obj
    
    def save(self):
        self.obj.save()
        
class EasyPythonMutagenOggVorbis(object):
    ''' An interface like EasyId3, but for OggVorbis files.'''
    
    def __init__(self, filename):
        from mutagen.oggvorbis import OggVorbis
        self.obj = OggVorbis(filename)
        self.map = {
            'album': 'album',
            'comment': 'comment',
            'artist': 'artist',
            'title': 'title',
            'albumartist': 'albumartist',
            'tracknumber': 'tracknumber',
            'discnumber': 'discnumber',
            'composer': 'composer',
            'genre': 'genre',
            'website': 'www',
            }
        
    def __getitem__(self, key):
        return self.obj[self.map[key]]
            
    def __setitem__(self, key, val):
        self.obj[self.map[key]] = val
            
    def __contains__(self, key):
        return key in self.map and self.map[key] in self.obj
    
    def save(self):
        self.obj.save()
        
class EasyPythonMutagenM4a(easymp4.EasyMP4):
    '''EasyMp4, with added fields.
        EasyMp4 already provides
        title
        album
        artist
        albumartist
        date
        comment
        genre, and more'''
    
    def __init__(self, filename):
        super(EasyPythonMutagenM4a, self).__init__(filename)
        easymp4.EasyMP4Tags.RegisterTextKey('composer', b'\xa9wrt')
        easymp4.EasyMP4Tags.RegisterTextKey('desc', b'desc')
        easymp4.EasyMP4Tags.RegisterTextKey('website', b'----:com.apple.iTunes:WWW')

def getAudioDuration(filename, alreadyobj=None):
    filenamelower = filename.lower()
    if filenamelower.endswith('.mp3'):
        from mutagen.mp3 import MP3
        length = MP3(filename).info.length
        
    elif filenamelower.endswith('.mp4') or filenamelower.endswith('.m4a'):
        if isinstance(alreadyobj, EasyPythonMutagen):
            length = alreadyobj.obj.info.length
        elif isinstance(alreadyobj, easymp4.EasyMP4):
            length = alreadyobj.info.length
        else:
            length = easymp4.EasyMP4(filename).info.length
            
    elif filenamelower.endswith('.flac'):
        if isinstance(alreadyobj, EasyPythonMutagen):
            length = alreadyobj.obj.obj.info.length
        elif isinstance(alreadyobj, EasyPythonMutagenFlac):
            length = alreadyobj.obj.info.length
        else:
            length = EasyPythonMutagenFlac(filename).obj.info.length
            
    elif filenamelower.endswith('.ogg'):
        if isinstance(alreadyobj, EasyPythonMutagen):
            length = alreadyobj.obj.obj.info.length
        elif isinstance(alreadyobj, EasyPythonMutagenOggVorbis):
            length = alreadyobj.obj.info.length
        else:
            length = EasyPythonMutagenOggVorbis(filename).obj.info.length

    else:
        return ValueError('unsupported extension')
        
    return length


