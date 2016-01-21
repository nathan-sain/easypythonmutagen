# easypythonmutagen
Easily read/write metadata for mp3, m4a, ogg, flac. A simplified interface for Mutagen.



 * Use the same interface for different audio formats.
 
 * If writing to a file with no metadata, adds metadata instead of throwing exception.
 
 * Much easier to write tags in id3v2.3, for compat. with Windows and smartphone apps.
 
 * Method to get the empirical ("actual") bitrate in addition to stated bitrate.
 
Examples:

    o = EasyPythonMutagen('file.mp3')
    o.set('title', 'song title')
    o.save()
    o = EasyPythonMutagen('file.flac')
    o.set('title', 'song title')
    o.save()
    
    o = EasyPythonMutagen('file in id3_v23.mp3', use_id3_v23=True)
    o.set('title', u'title with uni\u0107ode')
    o.save()
    
    print(get_audio_duration('file.mp3'))
    print(get_empirical_bitrate('file.mp3'))
    
    