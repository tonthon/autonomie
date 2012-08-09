# -*- coding: utf-8 -*-
# * File Name : test_fileupload.py
#
# * Copyright (C) 2010 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 06-04-2012
# * Last Modified :
#
# * Project :
#
"""
    Tests
"""
import os
from mock import MagicMock
from pyramid import testing

from .base import BaseFunctionnalTest
from .base import BaseViewTest
from .base import TMPDIR, DATASDIR
from autonomie.utils import fileupload

FAKEURL = "/assets/company/stuff"

class TestFileTempStore(BaseFunctionnalTest):
    def test_setitem(self):
        request = self.get_csrf_request()
        session = request.session
        tempstore = fileupload.FileTempStore(session, TMPDIR, FAKEURL)
        self.assertEqual(None, tempstore.preview_url("dummy"))
        #coming from database
        cstruct1 = {'uid':'test', 'filename':'testfile1.jpg'}
        tempstore[cstruct1['uid']] = cstruct1
        cstruct1['mimetype'] = None
        cstruct1['size'] = None
        self.assertEqual(tempstore.get(cstruct1['uid']), cstruct1)
        self.assertEqual(tempstore.get(cstruct1['uid'])['preview_url'],
                        os.path.join(FAKEURL, cstruct1['filename']))

        # just submitted
        cstruct2 = {'uid':'test', 'filename':'testfile2.jpg',
                    'fp':file(os.path.join(DATASDIR, 'image.jpg'), 'r'),
                    'mimetype':'image/jpeg', 'size':15}
        tempstore[cstruct2['uid']] = cstruct2
        self.assertEqual(tempstore.get(cstruct2['uid'])['mimetype'],
                                                cstruct2['mimetype'])
        self.assertFalse('fp' in tempstore.get(cstruct2['uid']).keys())
        self.assertTrue(os.path.isfile(os.path.join(TMPDIR, 'testfile2.jpg')))
        self.assertTrue(tempstore.get(cstruct2['uid'])['preview_url'],
                                os.path.join(FAKEURL, cstruct2['filename']))
