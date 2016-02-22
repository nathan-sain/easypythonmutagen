
import os
import shutil
import unittest
from easypythonmutagen import EasyPythonMutagen, get_audio_duration, get_empirical_bitrate


class EasyPythonMutagenComponentTests(unittest.TestCase):
    def setUp(self):
        import tempfile
        
        # create an empty directory
        self.tmpdir = tempfile.gettempdir()+'/testeasypythonmutagen'
        if os.path.exists(self.tmpdir):
            shutil.rmtree(self.tmpdir)
        os.makedirs(self.tmpdir)
        
        # copy test media to the directory
        if not os.path.exists('./test/media/flac.flac'):
            raise RuntimeError('could not find test media.')
            
        testfiles = ['flac.flac', 'm4a128.m4a', 'm4a16.m4a', 'm4a224.m4a', 'mp3_avgb128.mp3', 
            'mp3_avgb16.mp3', 'mp3_avgb224.mp3', 'mp3_cnsb128.mp3', 'mp3_cnsb16.mp3', 'mp3_cnsb224.mp3',
            'ogg_01.ogg', 'ogg_10.ogg']
        for file in testfiles:
            shutil.copy('./test/media/'+file, self.tmpdir+'/'+file)

    def tearDown(self):
        if 'testeasypythonmutagen' in self.tmpdir and os.path.exists(self.tmpdir):
            shutil.rmtree(self.tmpdir)
    
    def test_lengthAndBitrate(self):
        # get duration; no tag object provided
        tmpdirsl = self.tmpdir+'/'
        self.assertEqual(1023, int(1000*get_audio_duration(tmpdirsl+'flac.flac')))
        self.assertEqual(1160, int(1000*get_audio_duration(tmpdirsl+'m4a16.m4a')))
        self.assertEqual(1091, int(1000*get_audio_duration(tmpdirsl+'m4a128.m4a')))
        self.assertEqual(1091, int(1000*get_audio_duration(tmpdirsl+'m4a224.m4a')))
        self.assertEqual(2773, int(1000*get_audio_duration(tmpdirsl+'mp3_avgb16.mp3')))
        self.assertEqual(2773, int(1000*get_audio_duration(tmpdirsl+'mp3_avgb128.mp3')))
        self.assertEqual(2773, int(1000*get_audio_duration(tmpdirsl+'mp3_avgb224.mp3')))
        self.assertEqual(2873, int(1000*get_audio_duration(tmpdirsl+'mp3_cnsb16.mp3')))
        self.assertEqual(2773, int(1000*get_audio_duration(tmpdirsl+'mp3_cnsb128.mp3')))
        self.assertEqual(2773, int(1000*get_audio_duration(tmpdirsl+'mp3_cnsb224.mp3')))
        self.assertEqual(1591, int(1000*get_audio_duration(tmpdirsl+'ogg_01.ogg')))
        self.assertEqual(1591, int(1000*get_audio_duration(tmpdirsl+'ogg_10.ogg')))
        
        # get duration; tag object provided
        self.assertEqual(1023, int(1000*get_audio_duration(tmpdirsl+'flac.flac', EasyPythonMutagen(tmpdirsl+'flac.flac'))))
        self.assertEqual(1160, int(1000*get_audio_duration(tmpdirsl+'m4a16.m4a', EasyPythonMutagen(tmpdirsl+'m4a16.m4a'))))
        self.assertEqual(1091, int(1000*get_audio_duration(tmpdirsl+'m4a128.m4a', EasyPythonMutagen(tmpdirsl+'m4a128.m4a'))))
        self.assertEqual(1091, int(1000*get_audio_duration(tmpdirsl+'m4a224.m4a', EasyPythonMutagen(tmpdirsl+'m4a224.m4a'))))
        self.assertEqual(2773, int(1000*get_audio_duration(tmpdirsl+'mp3_avgb16.mp3', EasyPythonMutagen(tmpdirsl+'mp3_avgb16.mp3'))))
        self.assertEqual(2773, int(1000*get_audio_duration(tmpdirsl+'mp3_avgb128.mp3', EasyPythonMutagen(tmpdirsl+'mp3_avgb128.mp3'))))
        self.assertEqual(2773, int(1000*get_audio_duration(tmpdirsl+'mp3_avgb224.mp3', EasyPythonMutagen(tmpdirsl+'mp3_avgb224.mp3'))))
        self.assertEqual(2873, int(1000*get_audio_duration(tmpdirsl+'mp3_cnsb16.mp3', EasyPythonMutagen(tmpdirsl+'mp3_cnsb16.mp3'))))
        self.assertEqual(2773, int(1000*get_audio_duration(tmpdirsl+'mp3_cnsb128.mp3', EasyPythonMutagen(tmpdirsl+'mp3_cnsb128.mp3'))))
        self.assertEqual(2773, int(1000*get_audio_duration(tmpdirsl+'mp3_cnsb224.mp3', EasyPythonMutagen(tmpdirsl+'mp3_cnsb224.mp3'))))
        self.assertEqual(1591, int(1000*get_audio_duration(tmpdirsl+'ogg_01.ogg', EasyPythonMutagen(tmpdirsl+'ogg_01.ogg'))))
        self.assertEqual(1591, int(1000*get_audio_duration(tmpdirsl+'ogg_10.ogg', EasyPythonMutagen(tmpdirsl+'ogg_10.ogg'))))
        
        # get empirical bitrate
        self.assertEqual(29, int(get_empirical_bitrate(tmpdirsl+'m4a16.m4a')))
        self.assertEqual(136, int(get_empirical_bitrate(tmpdirsl+'mp3_avgb128.mp3')))
        self.assertEqual(233, int(get_empirical_bitrate(tmpdirsl+'mp3_cnsb224.mp3')))
        
        # unsupported extensions
        self.assertRaisesRegexp(ValueError, 'unsupported', lambda:get_audio_duration('missing_extension'))
        self.assertRaisesRegexp(ValueError, 'unsupported', lambda:get_audio_duration('unsupported.mp3.extension.mp5'))
        self.assertRaisesRegexp(ValueError, 'unsupported', lambda:get_empirical_bitrate('missing_extension'))
        self.assertRaisesRegexp(ValueError, 'unsupported', lambda:get_empirical_bitrate('unsupported.mp3.extension.mp5'))
    
    def test_metadataTags(self):
        # saving in id3_23 should be different than saving in id3_24
        import filecmp
        tmpdirsl = self.tmpdir+'/'
        shutil.copy(tmpdirsl+'mp3_avgb128.mp3', tmpdirsl+'mp3_id3_23.mp3')
        shutil.copy(tmpdirsl+'mp3_avgb128.mp3', tmpdirsl+'mp3_id3_24.mp3')
        self.assertTrue(filecmp.cmp(tmpdirsl+'mp3_id3_23.mp3', tmpdirsl+'mp3_id3_24.mp3', shallow=False))
        o23 = EasyPythonMutagen(tmpdirsl+'mp3_id3_23.mp3', True)
        o23.set('title', 'test')
        o23.save()
        o24 = EasyPythonMutagen(tmpdirsl+'mp3_id3_24.mp3', False)
        o24.set('title', 'test')
        o24.save()
        self.assertFalse(filecmp.cmp(tmpdirsl+'mp3_id3_23.mp3', tmpdirsl+'mp3_id3_24.mp3', shallow=False))
        
        # unsupported extensions
        self.assertRaisesRegexp(ValueError, 'unsupported', lambda:EasyPythonMutagen('missing_extension'))
        self.assertRaisesRegexp(ValueError, 'unsupported', lambda:EasyPythonMutagen('unsupported.mp3.extension.mp5'))
        
        # test reading and writing
        for file in os.listdir(self.tmpdir):
            if 'id3' in file:
                continue
                
            fields = dict(album=1, comment=1, artist=1, title=1, 
                composer=1, discnumber=1, tracknumber=1, albumartist=1, website=1)
            obj = EasyPythonMutagen(tmpdirsl+file)
            self.assertRaises(KeyError, lambda: obj.get('composer'))
            if not file.endswith('.mp3'):
                fields['description'] = 1
            
            # we shouldn't be able to set invalid fields
            if '.m4a' in file:
                # workaround for mutagen bug easymp4.py, line 183,  __getitem__ when it fails to raise EasyMP4KeyError("%r is not a valid key" % key)
                self.assertRaisesRegexp(Exception, '(not a valid key)|(object is not callable)', lambda: obj.set('aartist', 'test'))
                self.assertRaisesRegexp(Exception, '(not a valid key)|(object is not callable)', lambda: obj.get('aartist'))
            else:
                self.assertRaises(KeyError, lambda: obj.set('aartist', 'test'))
                self.assertRaises(KeyError, lambda: obj.get('aartist'))
            
            for field in fields:
                # first, all fields should be empty
                self.assertEqual(None, obj.get_or_default(field, None))
                
                # then, put data into the field
                if field=='tracknumber':
                    val = 14
                elif field=='discnumber':
                    val = 7
                elif field=='website':
                    val = 'http://website'+field
                else:
                    val = u'test\u0107test\u1101'+field
                fields[field] = val
                obj.set(field, val)
                self.assertEqual(unicode(fields[field]), obj.get(field))
            
            # verify data was saved
            obj.save()
            obj = EasyPythonMutagen(tmpdirsl+file)
            for field in fields:
                self.assertEqual(unicode(fields[field]), obj.get(field))
                
            # append data to each text field
            for field in fields:
                if not isinstance(fields[field], int):
                    obj.set(field, unicode(fields[field]) + 'appended')
                    obj.save()

            # verify data was saved
            obj = EasyPythonMutagen(tmpdirsl+file)
            for field in fields:
                if not isinstance(fields[field], int):
                    self.assertEqual(unicode(fields[field]) + 'appended', obj.get(field))


if __name__ == '__main__':
    unittest.main()
