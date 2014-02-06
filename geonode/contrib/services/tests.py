# -*- coding: utf-8 -*-
#########################################################################
#
# Copyright (C) 2012 OpenPlans
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#########################################################################

import json

from django.conf import settings
from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User, AnonymousUser
from django.core.urlresolvers import reverse

class ServicesTests(TestCase):
    """Tests geonode.contrib.services app/module
    """

    def setUp(self):
        self.user = 'admin'
        self.passwd = 'admin'

    fixtures = ['map_data.json', 'initial_data.json']

    def test_register_indexed_wms(self):
        """Test registering demo.geonode.org as an indexed WMS
        """
        c = Client()
        c.login(username='admin', password='admin')
        response = c.post(reverse('register_service'), 
                            {'method':'I',
                             'type':'WMS',
                             'url':'http://demo.geonode.org/geoserver/wms',
                             'name':'demo.geonode.org:wms'})
        self.assertEqual(response.status_code, 200)
        response_dict = json.loads(response.content) 
        self.assertEqual(response_dict['status'], 'ok')
        response = c.post(reverse('register_layers'),
                            {'service_id': int(response_dict['id']),
                             'layer_list': ','.join(response_dict['available_layers'])})
        self.assertEqual(response.status_code, 200)
        response_dict = json.loads(response.content)
        self.assertEqual(response_dict['status'], 'ok')
