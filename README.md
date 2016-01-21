# easypythonmutagen
Easily read/write metadata for mp3, m4a, ogg, flac. A simplified interface for Mutagen.



 * You can use the same class and interface for different audio formats.
 
 * You won't need to catch exceptions in case the mp3 doesn't have an id3 tag yet.
 
 * You won't have to use a low level interface to write tags in id3v2.3, for compat. with Windows and smartphone apps.
 
Examples:

    o = EasyPythonMutagen('file.mp3')
    o.set('title', 'song title')
    o.save()
    o = EasyPythonMutagen('file.flac')
    o.set('title', 'song title')
    o.save()
    
    o = EasyPythonMutagen('file in id3_v23.mp3', use_id3_v23=True)
    o.set('title', u'title with unicode: \u0107')
    o.save()
    
    print(get_audio_duration('file.mp3'))
    print(get_empirical_bitrate('file.mp3'))
    
It'd be nice to add id3v2.3 support in EasyID3 to the mutagen project at some point. In the meantime I'll use this wrapper.

Other small features of easypythonmutagen:

 * Provides method to get the empirical ("actual") bitrate in addition to stated bitrate.

 * The "get" methods directly return a value, instead of a list.
 
 * Intentionally disallows adding unrecognized fields
    * A typo like o['aartist'] fails instead of succeeding silently.
 
 * Added a few fields, like 'Composer' and 'Website' for mp4/m4a.