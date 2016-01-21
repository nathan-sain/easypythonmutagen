
import os
import shutil
import unittest
from easypythonmutagen import EasyPythonMutagen, getAudioDuration, getEmpiricalBitrate


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
        for file in os.listdir('./test/media'):
            shutil.copy('./test/media/'+file, self.tmpdir+'/'+file)

    def tearDown(self):
        if 'testeasypythonmutagen' in self.tmpdir and os.path.exists(self.tmpdir):
            shutil.rmtree(self.tmpdir)
    
    
    def test_lengthAndBitrate(self):
        # get duration; no tag object provided
        tmpdirsl = self.tmpdir+'/'
        self.assertEqual(1023, int(1000*getAudioDuration(tmpdirsl+'flac.flac')))
        self.assertEqual(1160, int(1000*getAudioDuration(tmpdirsl+'m4a16.m4a')))
        self.assertEqual(1091, int(1000*getAudioDuration(tmpdirsl+'m4a128.m4a')))
        self.assertEqual(1091, int(1000*getAudioDuration(tmpdirsl+'m4a224.m4a')))
        self.assertEqual(2773, int(1000*getAudioDuration(tmpdirsl+'mp3_avgb16.mp3')))
        self.assertEqual(2773, int(1000*getAudioDuration(tmpdirsl+'mp3_avgb128.mp3')))
        self.assertEqual(2773, int(1000*getAudioDuration(tmpdirsl+'mp3_avgb224.mp3')))
        self.assertEqual(2873, int(1000*getAudioDuration(tmpdirsl+'mp3_cnsb16.mp3')))
        self.assertEqual(2773, int(1000*getAudioDuration(tmpdirsl+'mp3_cnsb128.mp3')))
        self.assertEqual(2773, int(1000*getAudioDuration(tmpdirsl+'mp3_cnsb224.mp3')))
        self.assertEqual(1591, int(1000*getAudioDuration(tmpdirsl+'ogg_01.ogg')))
        self.assertEqual(1591, int(1000*getAudioDuration(tmpdirsl+'ogg_10.ogg')))
        
        # get duration; tag object provided
        self.assertEqual(1023, int(1000*getAudioDuration(tmpdirsl+'flac.flac', EasyPythonMutagen(tmpdirsl+'flac.flac'))))
        self.assertEqual(1160, int(1000*getAudioDuration(tmpdirsl+'m4a16.m4a', EasyPythonMutagen(tmpdirsl+'m4a16.m4a'))))
        self.assertEqual(1091, int(1000*getAudioDuration(tmpdirsl+'m4a128.m4a', EasyPythonMutagen(tmpdirsl+'m4a128.m4a'))))
        self.assertEqual(1091, int(1000*getAudioDuration(tmpdirsl+'m4a224.m4a', EasyPythonMutagen(tmpdirsl+'m4a224.m4a'))))
        self.assertEqual(2773, int(1000*getAudioDuration(tmpdirsl+'mp3_avgb16.mp3', EasyPythonMutagen(tmpdirsl+'mp3_avgb16.mp3'))))
        self.assertEqual(2773, int(1000*getAudioDuration(tmpdirsl+'mp3_avgb128.mp3', EasyPythonMutagen(tmpdirsl+'mp3_avgb128.mp3'))))
        self.assertEqual(2773, int(1000*getAudioDuration(tmpdirsl+'mp3_avgb224.mp3', EasyPythonMutagen(tmpdirsl+'mp3_avgb224.mp3'))))
        self.assertEqual(2873, int(1000*getAudioDuration(tmpdirsl+'mp3_cnsb16.mp3', EasyPythonMutagen(tmpdirsl+'mp3_cnsb16.mp3'))))
        self.assertEqual(2773, int(1000*getAudioDuration(tmpdirsl+'mp3_cnsb128.mp3', EasyPythonMutagen(tmpdirsl+'mp3_cnsb128.mp3'))))
        self.assertEqual(2773, int(1000*getAudioDuration(tmpdirsl+'mp3_cnsb224.mp3', EasyPythonMutagen(tmpdirsl+'mp3_cnsb224.mp3'))))
        self.assertEqual(1591, int(1000*getAudioDuration(tmpdirsl+'ogg_01.ogg', EasyPythonMutagen(tmpdirsl+'ogg_01.ogg'))))
        self.assertEqual(1591, int(1000*getAudioDuration(tmpdirsl+'ogg_10.ogg', EasyPythonMutagen(tmpdirsl+'ogg_10.ogg'))))
        
        # get empirical bitrate
        self.assertEqual(29, int(getEmpiricalBitrate(tmpdirsl+'m4a16.m4a')))
        self.assertEqual(136, int(getEmpiricalBitrate(tmpdirsl+'mp3_avgb128.mp3')))
        self.assertEqual(233, int(getEmpiricalBitrate(tmpdirsl+'mp3_cnsb224.mp3')))
        
        # unsupported extensions
        self.assertRaisesRegexp(ValueError, 'unsupported', lambda:getAudioDuration('missing_extension'))
        self.assertRaisesRegexp(ValueError, 'unsupported', lambda:getAudioDuration('unsupported.mp3.extension.mp5'))
        self.assertRaisesRegexp(ValueError, 'unsupported', lambda:getEmpiricalBitrate('missing_extension'))
        self.assertRaisesRegexp(ValueError, 'unsupported', lambda:getEmpiricalBitrate('unsupported.mp3.extension.mp5'))
        

# expect KeyError
# or mutagen.easymp4.EasyMP4KeyError

if __name__ == '__main__':
    unittest.main()
