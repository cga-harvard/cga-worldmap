from django.conf.urls import include, patterns, url
from django.views.generic.base import RedirectView

from geonode.maps.views import snapshot_create

from .views import (proxy, ajax_layer_update, ajax_layer_edit_check, upload_layer,
    create_pg_layer, ajax_increment_layer_stats, new_map_wm, new_map_json_wm, map_view_wm, map_json_wm,
    add_endpoint)
from tastypie.api import Api
from .api.resources import LayerResource, TagResource, TopicCategoryResource

# api
wm_api = Api(api_name='2.6')
wm_api.register(LayerResource())
wm_api.register(TagResource())
wm_api.register(TopicCategoryResource())

urlpatterns = patterns('',
                        # api
                        (r'^api/', include(wm_api.urls)),
                        # maps
                        url(r'^maps/new$', new_map_wm, name="new_map_wm"),
                        url(r'^maps/new/data$', new_map_json_wm, name='new_map_json_wm'),
                        url(r'^maps/(?P<mapid>[^/]+)/data$', map_json_wm, name='map_json'),
                        #url(r'^maps/add_layer$', add_layer_wm, name='add_layer_wm'),
                        url(r'^maps/(?P<mapid>[^/]+)/view$', map_view_wm, name='map_view_wm'),
                        url(r'^maps/add_endpoint?$', add_endpoint, name='add_endpoint'),
                        url(r'^snapshot/create/?$', snapshot_create, name='snapshot_create'),
                        url(r'^maps/(?P<mapid>[^/]+)/(?P<snapshot>[A-Za-z0-9_\-]+)/$', map_view_wm, name='map_view_wm'),
                        # TODO develop the create layer app
                        # layers
                        url(r'^data/(?P<layername>[^/]*)$', RedirectView.as_view(pattern_name='layer_detail', permanent=False)),
                        url(r'^data/(?P<layername>[^/]*)/ajax-edit-check/?$', ajax_layer_edit_check, name = 'ajax_layer_edit_check'),
                        url(r'^data/(?P<layername>[^/]*)/ajax_layer_update/?$', ajax_layer_update, name = 'ajax_layer_update'),
                        #url(r'^data/create_pg_layer', create_pg_layer, name='create_pg_layer'),
                        url(r'^/data/upload', upload_layer, name='data_upload'),
                        url(r'^data/layerstats', ajax_increment_layer_stats, name='layer_stats'),
)
