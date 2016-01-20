
import os
import shutil
import mutagen
from mutagen import easymp4

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
    '''EasyMp4, with added fields.'''
    
    def __init__(self, filename):
        super(EasyPythonMutagenM4a, self).__init__(filename)
        easymp4.EasyMP4Tags.RegisterTextKey('composer', b'\xa9wrt')
        easymp4.EasyMP4Tags.RegisterTextKey('desc', b'desc')
        easymp4.EasyMP4Tags.RegisterTextKey('description', b'desc')
        easymp4.EasyMP4Tags.RegisterTextKey('website', b'----:com.apple.iTunes:WWW')

        
