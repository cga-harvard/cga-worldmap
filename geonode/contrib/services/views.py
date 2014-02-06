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
import urllib

import uuid
import logging

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.forms.models import modelformset_factory
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.conf import settings
from django.template import RequestContext, loader
from django.utils.translation import ugettext as _
from django.utils import simplejson as json
from django.shortcuts import get_object_or_404


#from geonode.core.layers.views import layer_set_permissions
from geoserver.catalog import Catalog
from owslib.wms import WebMapService
from owslib.wfs import WebFeatureService
from owslib.tms import TileMapService
from owslib.csw import CatalogueServiceWeb
from arcrest import server as ArcService
from urlparse import urlsplit, urlunsplit


#from geonode.utils import OGC_Servers_Handler
from geonode.contrib.services.models import Service, Layer, ServiceLayer
from geonode.maps.views import _perms_info, bbox_to_wkt
from geonode.core.models import AUTHENTICATED_USERS, ANONYMOUS_USERS
from geonode.contrib.services.forms import CreateServiceForm, ServiceLayerFormSet
from geonode.utils import slugify
from geonode.contrib.services.tasks import import_indexed_wms_service_layers
import re
from geonode.maps.utils import llbbox_to_mercator
from django.db import transaction

logger = logging.getLogger("geonode.core.layers.views")


#ogc_server_settings = OGC_Servers_Handler(settings.OGC_SERVER)['default']

_user, _password = settings.GEOSERVER_CREDENTIALS #ogc_server_settings.credentials

SERVICE_LEV_NAMES = {
    Service.LEVEL_NONE  : _('No Service Permissions'),
    Service.LEVEL_READ  : _('Read Only'),
    Service.LEVEL_WRITE : _('Read/Write'),
    Service.LEVEL_ADMIN : _('Administrative')
}

@login_required
def services(request):
    """
    This view shows the list of all registered services
    """
    services = Service.objects.all()
    return render_to_response("services/service_list.html", RequestContext(request, {
        'services': services,
    }))

@login_required
@transaction.commit_on_success()
def register_service(request):
    """
    This view is used for manually registering a new service, with only URL as a
    parameter.
    """

    if request.method == "GET":
        service_form = CreateServiceForm()
        return render_to_response('services/service_register.html',
                                  RequestContext(request, {
                                      'create_service_form': service_form
                                  }))

    elif request.method == 'POST':
        # Register a new Service
        service_form = CreateServiceForm(request.POST)
        try:

            urlprop = urlsplit(request.POST.get('url'))
            url = urlunsplit((urlprop.scheme, urlprop.netloc, urlprop.path, None, None))

            # method = request.POST.get('method')
            # type = request.POST.get('type')
            # name = slugify(request.POST.get('name'))

            type, server = _guess_service_type(url)


            if "user" in request.POST and "password" in request.POST:
                user = request.POST.get('user')
                password = request.POST.get('password')
            else:
                user = None
                password = None

            if type == "WMS" or type == "OWS":
                return _process_wms_service(request.user, url, type, user, password, server)
            elif type == "ARC":
                return _process_arcgis_service(url, user, password, server=server)

            else:
                return HttpResponse('Not Implemented (Yet)', status=501)
        except Exception, e:
            logger.error("Unexpected Error", exc_info=1) 
            return HttpResponse('Unexpected Error: %s' % e, status=500)
    elif request.method == 'PUT':
        # Update a previously registered Service
        return HttpResponse('Not Implemented (Yet)', status=501)
    elif request.method == 'DELETE':
        # Delete a previously registered Service
        return HttpResponse('Not Implemented (Yet)', status=501)
    else:
        return HttpResponse('Invalid Request', status = 400)

def _is_unique(url):
    """
    Determine if a service is already registered based on matching url
    """
    try:
        service = Service.objects.get(base_url=url)
        return False
    except Service.DoesNotExist:
        return True

def _get_valid_name(proposed_name):
    """
    Return a unique slug name for a service
    """
    name = proposed_name
    if len(proposed_name)>40:
        name = proposed_name[:40]
    existing_service = Service.objects.filter(name=name)
    iter = 1
    while existing_service.count() > 0:
        name = proposed_name + str(iter)
        existing_service = Service.objects.filter(name=name)
        iter+=1
    return name

def _guess_service_type(base_url, type=None):
    """
    Try to determine service type by process of elimination
    """

    if type in ["WMS", "OWS"] or type is None:
        try:
            service = WebMapService(base_url)
            service_type = ['WMS', service]
            try:
                servicewfs = WebFeatureService(base_url)
                service_type = ['OWS', service]
            except:
                pass
            return service_type
        except:
            pass
    if type == "TMS" or type is None:
        try:
            service = TileMapService(base_url)
            return ["TMS", service]
        except:
            pass
    if type == "ARC" or type is None:
        try:
            service = ArcService(base_url)
            return ["ARC", service]
        except:
            pass
    if type in ["CSW", None]:
        try:
            service = CatalogueServiceWeb(base_url)
            return ["CSW", service]
        except:
            pass
    if type in ["OGP", None]:
        try:
            # service = OpenGeoPortalService(base_url)
            # return "OGP"
            return [None,None]
        except:
            return [None,None]


def _register_service_by_type(user, url, type, name=None, password=None):
    try:
        service = Service.objects.get(base_url=url)
        return
    except:
        server, type = _guess_service_type(url, type)

        if server is not None:
            if type == "WMS" or type == "OWS":
                _process_wms_service(user, url, type, name, password, server=server)
            elif type == "ARC":
                _process_arcgis_service(user, url, name, password, server=server)


def _process_wms_service(user, url, type, username, password, server):
    url = server.getOperationByName('GetMap').methods['Get']['url'].rstrip("?")

    try:
        service = Service.objects.get(base_url=url)
        return_dict = {}
        return_dict['service_id'] = service.pk
        return_dict['msg'] = "This is an existing Service"
        return HttpResponse(json.dumps(return_dict),
                            mimetype='application/json',
                            status=200)
    except:
        pass

    title = server.identification.title
    if title:
        name = _get_valid_name(slugify(title))
    else:
        name = _get_valid_name(slugify(urlsplit(url).netloc))
    try:
        supported_crs  = ','.join(server.contents.itervalues().next().crsOptions)
    except:
        supported_crs = None
    if re.search('EPSG:900913|EPSG:3857', supported_crs):
        return _register_indexed_service(user, type, url, name, username, password, server=server)
    else:
        return _register_cascaded_service(user, type, url, name, username, password, server=server)

def _register_cascaded_service(user, type, url, name, username, password,  server=None, owner=None):
    """
    Register a service as cascading WMS
    """
    if type == 'WMS':
        # Register the Service with GeoServer to be cascaded
        cat = Catalog(settings.GEOSERVER_BASE_URL + "rest", 
                        _user , _password)
        # Can we always assume that it is geonode?
        geonode_ws = cat.get_workspace("geonode")
        ws = cat.create_wmsstore(name,geonode_ws, user, password)
        ws.capabilitiesURL = url
        ws.type = "WMS"
        cat.save(ws)
        available_resources = ws.get_resources(available=True)
        
        # Save the Service record
        service = Service(type = type,
                            method='C',
                            base_url = url,
                            name = name,
                            owner = owner)
        service.save()
        message = "Service %s registered" % service.name
        return_dict = {'status': 'ok', 'msg': message, 
                        'id': service.pk,
                        'available_layers': available_resources}
        return HttpResponse(json.dumps(return_dict), 
                            mimetype='application/json',
                            status=200)        
    elif type == 'WFS':
        # Register the Service with GeoServer to be cascaded
        cat = Catalog(settings.GEOSERVER_BASE_URL + "rest", 
                        _user , _password)
        # Can we always assume that it is geonode?
        geonode_ws = cat.get_workspace("geonode")
        wfs_ds = cat.create_datastore(name)
        connection_params = {
            "WFSDataStoreFactory:MAXFEATURES": "0",
            "WFSDataStoreFactory:TRY_GZIP": "true",
            "WFSDataStoreFactory:PROTOCOL": "false",
            "WFSDataStoreFactory:LENIENT": "true",
            "WFSDataStoreFactory:TIMEOUT": "3000",
            "WFSDataStoreFactory:BUFFER_SIZE": "10",
            "WFSDataStoreFactory:ENCODING": "UTF-8",
            "WFSDataStoreFactory:WFS_STRATEGY": "nonstrict",
            "WFSDataStoreFactory:GET_CAPABILITIES_URL": url,
        }
        if user and password:
            connection_params["WFSDataStoreFactory:USERNAME"] = user
            connection_params["WFSDataStoreFactory:PASSWORD"] = password

        wfs_ds.connection_parameters = connection_params
        cat.save(wfs_ds)
        available_resources = wfs_ds.get_resources(available=True)
        
        # Save the Service record
        service = Service(type = type,
                            method='C',
                            base_url = url,
                            name = name,
                            owner = user)
        service.save()
        message = "Service %s registered" % service.name
        return_dict = {'status': 'ok', 'msg': message, 
                        'id': service.pk,
                        'available_layers': available_resources}
        return HttpResponse(json.dumps(return_dict), 
                            mimetype='application/json',
                            status=200)        
    elif type == 'WCS':
        return HttpResponse('Not Implemented (Yet)', status=501)
    else:
        return HttpResponse(
            'Invalid Method / Type combo: ' + 
            'Only Cascaded WMS, WFS and WCS supported',
            mimetype="text/plain",
            status=400)

def _register_cascaded_layers(user, service, layers, perm_spec, verbosity=False):
    """
    Register layers for a cascading WMS
    """
    if service.type == 'WMS' or service.type == "WFS":
        cat = Catalog(settings.GEOSERVER_BASE_URL + "rest", 
                        _user , _password)
        # Can we always assume that it is geonode? 
        geonode_ws = cat.get_workspace("geonode") 
        store = cat.get_store(service.name,geonode_ws)
        count = 0
        for layer in layers: 
            lyr = cat.get_resource(layer)
            if(lyr == None):
                if service.type == "WMS":
                    resource = cat.create_wmslayer(geonode_ws, store, layer) 
                elif service.type == "WFS":
                    resource = cat.create_wfslayer(geonode_ws, store, layer) 
                new_layer, status = Layer.objects.save_layer_from_geoserver(geonode_ws, 
                                                        store, resource)
                new_layer.owner = user
                new_layer.save()
                if perm_spec:
                    #layer_set_permissions(new_layer, perm_spec)
                    pass
                else:
                    pass # Will be assigned default perms
                count += 1
        message = "%d Layers Registered" % count
        return_dict = {'status': 'ok', 'msg': message }
        return HttpResponse(json.dumps(return_dict),
                            mimetype='application/json',
                            status=200)
    elif service.type == 'WCS':
        return HttpResponse('Not Implemented (Yet)', status=501)
    else:
        return HttpResponse('Invalid Service Type', status=400)

def _register_indexed_service(user, type, url, name, username, password, owner=None, server=None, verbosity=False):
    """
    Register a service - WMS or OWS currently supported
    """
    if type == 'WMS' or type == "OWS":
        # TODO: Handle for errors from owslib
        wms = server or WebMapService(url)
        # TODO: Make sure we are parsing all service level metadata
        # TODO: Handle for setting ServiceContactRole
        base_url = wms.getOperationByName('GetMap').methods['Get']['url'].rstrip("?")
        service, created = Service.objects.get_or_create(base_url = base_url)
        if created:
            service.type = type
            service.method='I'
            service.name = name
            service.version = wms.identification.version
            service.title = wms.identification.title
            service.abstract = wms.identification.abstract
            service.keywords = ','.join(wms.identification.keywords)
            service.online_resource = wms.provider.url
            service.owner=user
            service.save()
        available_resources = []
        for layer in list(wms.contents):
            service_layer, created = ServiceLayer.objects.get_or_create(
                service=service,
                typename=wms[layer].name,
                title=wms[layer].title,
                description=wms[layer].abstract,
                styles=wms[layer].styles
                )
            if created:
                available_resources.append([wms[layer].name, wms[layer].title])
        if settings.USE_QUEUE:
            import_indexed_wms_service_layers.delay(service, server, available_resources)
        else:
            _register_indexed_layers(None, service, available_resources, None, wms=server)

        message = "Service %s registered" % service.name
        return_dict = {'status': 'ok', 'msg': message,
                        'service_id': service.pk,
                        'available_layers': available_resources}
        return HttpResponse(json.dumps(return_dict),
                            mimetype='application/json',
                            status=200)
    elif type == 'WFS':
        return HttpResponse('Not Implemented (Yet)', status=501)
    elif type == 'WCS':
        return HttpResponse('Not Implemented (Yet)', status=501)
    else:
        return HttpResponse(
            'Invalid Method / Type combo: ' + 
            'Only Indexed WMS, WFS and WCS supported',
            mimetype="text/plain",
            status=400)

def _register_indexed_layers(user, service, layers, perm_spec, wms=None, verbosity=False):
    """
    Register layers for an indexed service (only WMS/OWS currently supported
    """
    if re.match("WMS|OWS", service.type):
        wms = wms or WebMapService(service.base_url)
        count = 0
        for layer in layers:
            wms_layer = wms[layer[0]]
            if verbosity:
                print "Importing layer %s" % layer
            layer_uuid = str(uuid.uuid1())
            if not wms_layer.keywords:
                keywords = []
            else:
                keywords = map(lambda x: x[:100], wms_layer.keywords)
            if not wms_layer.abstract:
                abstract = ""
            else:
                abstract = wms_layer.abstract

            srs = None
            if 'EPSG:900913' in wms_layer.crsOptions:
                srs = 'EPSG:900913'
            elif len(wms_layer.crsOptions) > 0:
                matches = re.findall('EPSG\:(3857|102100|102113)', ' '.join(wms_layer.crsOptions))
                if matches:
                    srs = matches[0]
            if srs is None:
                message = "%d Incompatible projection - try setting the service as cascaded" % count
                return_dict = {'status': 'ok', 'msg': message }
                return HttpResponse(json.dumps(return_dict),
                                mimetype='application/json',
                                status=200)

            # Need to check if layer already exists??
            saved_layer, created = Layer.objects.get_or_create(name=wms_layer.name,
                defaults=dict(
                    service = service,
                    store=service.name, #??
                    storeType="remoteStore",
                    typename=wms_layer.name,
                    workspace="remoteWorkspace",
                    title=wms_layer.title,
                    abstract=abstract,
                    uuid=layer_uuid,
                    owner=user,
                    srs=srs,
                    bbox = llbbox_to_mercator(list(wms_layer.boundingBoxWGS84)),
                    llbbox = list(wms_layer.boundingBoxWGS84)
                )
            )
            if created:
                saved_layer.set_default_permissions()
                saved_layer.keywords.add(*keywords)
                saved_layer.set_layer_attributes()

                service_layer = ServiceLayer.objects.get(service=service,typename=saved_layer.typename)
                service_layer.layer = saved_layer
                service_layer.save()
            count += 1
        message = "%d Layers Registered" % count
        return_dict = {'status': 'ok', 'msg': message }
        return HttpResponse(json.dumps(return_dict),
                            mimetype='application/json',
                            status=200)
    elif service.type == 'WFS':
        return HttpResponse('Not Implemented (Yet)', status=501)
    elif service.type == 'WCS':
        return HttpResponse('Not Implemented (Yet)', status=501)
    else:
        return HttpResponse('Invalid Service Type', status=400)

def _register_harvested_service(type, url, name, user, password, owner=None):
    """
    Register a CSW or OGP service  - stub only.  Needs to iterate through all layers and register
    the layers and the services they originate from.
    """
    if type == 'CSW':
        # Make this CSW Agnostic (i.e. Not GeoNetwork specific)
        gn = Layer.objects.gn_catalog
        id, service_uuid = gn.add_harvesting_task('CSW', name, url) 
        service = Service(type = type,
                            method='H',
                            base_url = url,
                            name = name,
                            owner=owner,
                            uuid = service_uuid,
                            external_id = id)
        service.save()
        message = "Service %s registered" % service.name
        return_dict = {'status': 'ok', 'msg': message,
                        'id': service.pk,
                        'available_layers': []}
        return HttpResponse(json.dumps(return_dict),
                            mimetype='application/json',
                            status=200)
    elif type== "OGP":
        harvest_ogp_service(name,url)
    else:
        return HttpResponse(
            'Invalid Method / Type combo: ' + 
            'Only Harvested CSW supported',
            mimetype="text/plain",
            status=400
        )

def _process_arcgis_service(url,user, password, owner=None):
    """
    Register an ArcGIS REST service - maybe do this from _register_indexed_service instead?
    """
    #http://maps1.arcgisonline.com/ArcGIS/rest/services
    try:
        service = Service.objects.get(base_url=url)
        return_dict = {}
        return_dict['service_id'] = service.pk
        return_dict['msg'] = "This is an existing Service"
        return HttpResponse(json.dumps(return_dict),
                            mimetype='application/json',
                            status=200)
    except:
        pass

def _register_arcgis_layers(user, service, layers, perm_spec, verbosity=False):
    pass

def harvest_ogp_service(url, num_rows=25, start=0,owner=None):
    base_query_str =  """q=_val_:%22sum(sum(product(9.0,map(sum(map(MinX,-180.0,180,1,0),
        map(MaxX,-180.0,180.0,1,0),map(MinY,-90.0,90.0,1,0),map(MaxY,-90.0,90.0,1,0)),4,4,1,0))),0,0)%22&debugQuery=
        false&&fq={!frange+l%3D1+u%3D10}product(2.0,map(sum(map(sub(abs(sub(0,CenterX)),sum(171.03515625,HalfWidth)),0,
        400000,1,0),map(sub(abs(sub(0,CenterY)),sum(75.84516854027,HalfHeight)),0,400000,1,0)),0,0,1,0))&wt=json
        &fl=Name,CollectionId,Institution,Access,DataType,Availability,LayerDisplayName,Publisher,GeoReferenced,
        Originator,Location,MinX,MaxX,MinY,MaxY,ContentDate,LayerId,score,WorkspaceName,SrsProjectionCode
        &sort=score+desc&fq=DataType%3APoint+OR+DataType%3ALine+OR+DataType%3APolygon+OR+DataType%3ARaster
        +OR+DataType%3APaper+Map&fq=Access:Public"""

    fullurl = url + base_query_str + ("&rows=%d&start=%d" % (num_rows, start))
    response = json.loads(urllib.urlopen(url).read())
    result_count =  response["response"]["numFound"]
    process_ogp_results(response)

    while start < result_count:
        start = start + num_rows
        harvest_ogp_service(url, num_rows, start)

def process_ogp_results(result_json, owner):
    for doc in result_json["response"]["docs"]:
        locations = doc["Location"]
        if "tilecache" in locations:
            service_url = doc["Location"]["tilecache"]
            service_type = "WMS"
        elif "wms" in locations:
            service_url = doc["Location"]["tilecache"]
            service_type = "WMS"
        else:
            pass

        #Harvard is a special case
        if doc["Institution"] == "Harvard":
            service_type = "HGL"

        try:
            service = Service.objects.get(base_url=service_url)
        except Service.DoesNotExist:
            name = slugify(service_url)
            if service_type == "WMS":
                try:
                    r_json = json.loads(_register_indexed_service(service_type, service_url, name, owner=owner))
                    service = r_json["id"]
                except Exception, e:
                    print str(e)
                    service = Service(type = type,
                                      method='I',
                                      base_url = service_url,
                                      name = name,
                                      online_resource = service_url,
                                      owner=owner)

            if service:
                typename = doc["Name"]
                if doc["Workspace"]:
                    typename = doc["Workspace"] + ":" + typename
                service_layer = ServiceLayer(service=service,typename=typename)
                service_layer.save()
                bbox = (
                    float(doc['MinX']),
                    float(doc['MinY']),
                    float(doc['MaxX']),
                    float(doc['MaxY']),
                )
                abstract = json.dumps(doc)
                saved_layer, created = Layer.objects.get_or_create(service=service, typename=typename,
                                                                   defaults=dict(
                                                                       service = service,
                                                                       store=service.name, #??
                                                                       storeType="remoteStore",
                                                                       workspace="remoteWorkspace",
                                                                       abstract=abstract,
                                                                       title=doc["LayerDisplayName"],
                                                                       owner=owner,
                                                                       srs="EPSG:900913", #Assumption
                                                                       geographic_bounding_box = bbox,
                                                                       )
                )

                if created:
                    service_layer.layer = saved_layer
                    service_layer.save

def service_detail(request, service_id):
    '''
    This view shows the details of a service 
    '''
    service = get_object_or_404(Service,pk=service_id)
    """
    if not request.user.has_perm('maps.view_service', obj=map):
        return HttpResponse(loader.render_to_string('401.html',
            RequestContext(request, {'error_message':
                _("You are not allowed to view this Service.")})), status=401)
    """
    layers = Layer.objects.filter(service=service) 
    return render_to_response("services/service_detail.html", RequestContext(request, {
        'service': service,
        'layers': layers,
        'permissions_json': json.dumps(_perms_info(service, SERVICE_LEV_NAMES))
    }))

@login_required
def edit_service(request, service_id):
    """
    Edit an existing Service
    Redirects to Service Detail temporarily
    """
    return HttpResponseRedirect(reverse("service_detail", args=[service_id]))

@login_required
def remove_service(request, service_id):
    '''
    Delete a service, and its constituent layers. 
    '''
    service_obj = get_object_or_404(Service,pk=service_id)

    if not request.user.has_perm('maps.delete_service', obj=service_obj):
        return HttpResponse(loader.render_to_string('401.html', 
            RequestContext(request, {'error_message': 
                _("You are not permitted to remove this service.")})), status=401)

    if request.method == 'GET':
        return render_to_response("services/service_remove.html", RequestContext(request, {
            "service": service_obj
        }))
    elif request.method == 'POST':
        servicelayers = service_obj.servicelayer_set.all()
        for servicelayer in servicelayers:
            servicelayer.delete()

        layers = service_obj.layer_set.all()
        for layer in layers:
            layer.delete()
        service_obj.delete()

        return HttpResponseRedirect(reverse("services"))

def set_service_permissions(service, perm_spec):
    if "authenticated" in perm_spec:
        service.set_gen_level(AUTHENTICATED_USERS, perm_spec['authenticated'])
    if "anonymous" in perm_spec:
        service.set_gen_level(ANONYMOUS_USERS, perm_spec['anonymous'])
    users = [n for (n, p) in perm_spec['users']]
    service.get_user_levels().exclude(user__username__in = users + [service.owner]).delete()
    for username, level in perm_spec['users']:
        user = User.objects.get(username=username)
        service.set_user_level(user, level)

@login_required
def ajax_service_permissions(request, service_id):
    service = get_object_or_404(Service,pk=service_id) 
    if not request.user.has_perm("maps.change_service_permissions", obj=service):
        return HttpResponse(
            'You are not allowed to change permissions for this service',
            status=401,
            mimetype='text/plain'
        )

    if not request.method == 'POST':
        return HttpResponse(
            'You must use POST for editing service permissions',
            status=405,
            mimetype='text/plain'
        )

    spec = json.loads(request.raw_post_data)
    set_service_permissions(service, spec)

    return HttpResponse(
        "Permissions updated",
        status=200,
        mimetype='text/plain')

