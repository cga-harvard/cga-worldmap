from celery.task import task
from geonode.maps import autocomplete_light_registry


@task
def import_indexed_wms_service_layers(service, wms, layers):
    from geonode.contrib.services.views import _register_indexed_layers
    _register_indexed_layers(None, service, layers, None, wms=wms)


@task
def import_indexed_service(user, url, type):
    from geonode.contrib.services.views import _register_service_by_type
    _register_service_by_type(user, url, type)
