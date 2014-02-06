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

from django.utils.translation import ugettext_lazy as _

SERVICE_TYPES = (
    ('OWS', _('Paired WMS/WFS/WCS')),
    ('WMS', _('Web Map Service')),
    ('WFS', _('Web Feature Service')),
    ('WCS', _('Web Coverage Service')),
    ('WPS', _('Web Processing Service')),
    ('CSW', _('Catalogue Service')),
    ('WMTS', _('Web Map Tile Service')),
    ('TMS', _('Tile Map Service')),
    ('OSG', _('OpenSearch Geo Service')),
    ('ARC', _('ArcGIS REST Service')),
    ('OGP', _('OpenGeoPortal')),
    ('HGL', _('Harvard Geospatial Library')),
)

SERVICE_METHODS = (
    ('L', _('Local')),
    ('C', _('Cascaded')),
    ('H', _('Harvested')),
    ('I', _('Indexed')),
    ('X', _('Live')),
)


GXP_PTYPES = {
    'OWS' : 'gxp_wmscsource',
    'WMS': 'gxp_wmscsource',
    'WFS': 'gxp_wmscsource',
    'WCS': 'gxp_wmscsource',
    'ARC': 'gxp_arcrestsource',
    'HGL': 'gxp_hglsource',
    'WPS': None,
    'CSW': None,
    'WMTS': None,
    'TMS': None,
    'OSG': None,
    'OGP': None
}

