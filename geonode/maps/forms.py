# -*- coding: utf-8 -*-
import autocomplete_light
from django import forms
from django.utils import simplejson as json
import os
import tempfile
from django.utils.translation import ugettext as _
from geonode.maps.models import LayerAttribute, Contact, Layer, ContactRole, Map
from geonode.flexidates import FlexiDateFormField
import taggit

SRS_CHOICES = (
    ('EPSG:4326', 'EPSG:4326 (WGS 84 Lat/Long)'),
    ('EPSG:900913', 'EPSG:900913 (Web Mercator)'),
)

GEOMETRY_CHOICES = [
    ['Point', 'Points'],
    ['LineString', 'Lines'],
    ['Polygon', 'Polygons (Shapes)']
]


TYPE_CHOICES = (
       ('java.lang.Boolean', 'Boolean (true/false)'),
       ('java.util.Date', 'Date/Time'),
       ('java.lang.Float', 'Number (Float)'),
       ('java.lang.Integer', 'Number (Integer)'),
       ('java.lang.String', 'Text'),
)


class JSONField(forms.CharField):
    def clean(self, text):
        text = super(JSONField, self).clean(text)
        try:
            return json.loads(text)
        except ValueError:
            raise forms.ValidationError("this field must be valid JSON")


class LayerCreateForm(forms.Form):
    name = forms.CharField(label="Name", max_length=256,required=True)
    title = forms.CharField(label="Title",max_length=256,required=True)
    srs = forms.CharField(label="Projection",initial="EPSG:4326",required=True)
    geom = forms.ChoiceField(label="Data type", choices=GEOMETRY_CHOICES,required=True)
    keywords = forms.CharField(label = '*' + ('Keywords (separate with spaces)'), widget=forms.Textarea)
    abstract = forms.CharField(widget=forms.Textarea, label="Abstract", required=True)
    permissions = JSONField()

class LayerUploadForm(forms.Form):
    base_file = forms.FileField()
    dbf_file = forms.FileField(required=False)
    shx_file = forms.FileField(required=False)
    prj_file = forms.FileField(required=False)
    sld_file = forms.FileField(required=False)
    encoding = forms.ChoiceField(required=False)
    spatial_files = ("base_file", "dbf_file", "shx_file", "prj_file", "sld_file")

    def clean(self):
        cleaned = super(LayerUploadForm, self).clean()
        base_name, base_ext = os.path.splitext(cleaned["base_file"].name)
        if base_ext.lower() not in (".shp", ".tif", ".tiff", ".geotif", ".geotiff", ".zip"):
            raise forms.ValidationError("Only Shapefiles and GeoTiffs are supported. You uploaded a %s file" % base_ext)
        if base_ext.lower() == ".shp":
            dbf_file = cleaned["dbf_file"]
            shx_file = cleaned["shx_file"]
            if dbf_file is None or shx_file is None:
                raise forms.ValidationError("When uploading Shapefiles, .SHX and .DBF files are also required.")
            dbf_name, __ = os.path.splitext(dbf_file.name)
            shx_name, __ = os.path.splitext(shx_file.name)
            if dbf_name != base_name or shx_name != base_name:
                raise forms.ValidationError("It looks like you're uploading "
                    "components from different Shapefiles. Please "
                    "double-check your file selections.")
            if cleaned["prj_file"] is not None:
                prj_file = cleaned["prj_file"].name
                if os.path.splitext(prj_file)[0] != base_name:
                    raise forms.ValidationError("It looks like you're "
                        "uploading components from different Shapefiles. "
                        "Please double-check your file selections.")
        return cleaned

    def write_files(self):
        tempdir = tempfile.mkdtemp()
        for field in self.spatial_files:
            f = self.cleaned_data[field]
            if f is not None:
                path = os.path.join(tempdir, f.name)
                with open(path, 'w') as writable:
                    for c in f.chunks():
                        writable.write(c)
        absolute_base_file = os.path.join(tempdir,
                self.cleaned_data["base_file"].name)
        sld_file = None
        if self.cleaned_data["sld_file"]:
            sld_file = os.path.join(tempdir, self.cleaned_data["sld_file"].name)
        return tempdir,  absolute_base_file, sld_file

class WorldMapLayerUploadForm(LayerUploadForm):
    sld_file = forms.FileField(required=False)
    encoding = forms.ChoiceField(required=False)
    layer_abstract = forms.CharField(required=False)
    layer_keywords = forms.CharField(required=False)
    layer_title = forms.CharField(required=False)
    keywords = forms.CharField(required=False)
    permissions = JSONField()

    spatial_files = ("base_file", "dbf_file", "shx_file", "prj_file", "sld_file")

class GazetteerForm(forms.Form):

    project = forms.CharField(label=_('Project'), max_length=128, required=False)
    startDate = forms.ModelChoiceField(label = _("Start Date attribute"),
                                       required=False,
                                       queryset = LayerAttribute.objects.none())

    startDateFormat = forms.CharField(label=_("Date format"), max_length=256, required=False)

    endDate = forms.ModelChoiceField(label = _("End Date attribute"),
                                     required=False,
                                     queryset = LayerAttribute.objects.none())

    endDateFormat = forms.CharField(label=_("Date format"), max_length=256, required=False)


class LayerContactForm(forms.Form):
    poc = forms.ModelChoiceField(empty_label = _("Person outside WorldMap (fill form)"),
                                 label = "*" + _("Point Of Contact"), required=False,
                                 queryset = Contact.objects.exclude(user=None),
                                 widget=autocomplete_light.ChoiceWidget('ContactAutocomplete'))

    metadata_author = forms.ModelChoiceField(empty_label = _("Person outside WorldMap (fill form)"),
                                             label = _("Metadata Author"), required=False,
                                             queryset = Contact.objects.exclude(user=None),
                                             widget=autocomplete_light.ChoiceWidget('ContactAutocomplete'))

    class Meta:
        model = Contact


class LayerForm(forms.ModelForm):
    from geonode.maps.models import CONSTRAINT_OPTIONS
    CONSTRAINT_HELP = _('''<p>Please choose the appropriate type of restriction (if any) for the use of your data.
    Then use the "Constraints Other" form below to provide any necessary details.</p>
    <p>
    Public Domain Dedication and License<br />
    http://opendatacommons.org/licenses/pddl/
    </p>
    <p>
    Attribution License (ODC-By)<br />
    http://opendatacommons.org/licenses/by/
    </p>
    <p>
    Open Database License (ODC-ODbL)<br />
    http://opendatacommons.org/licenses/odbl/
    </p>
    <p>
    CC-BY-SA<br />
    http://creativecommons.org/licenses/by-sa/2.0/
    ''')

    map_id = forms.CharField(widget=forms.HiddenInput(), initial='', required=False)
    date = forms.DateTimeField(label='*' + (_('Date')), widget=forms.SplitDateTimeWidget)
    date.widget.widgets[0].attrs = {"class":"date"}
    date.widget.widgets[1].attrs = {"class":"time"}
    temporal_extent_start = FlexiDateFormField(required=False,label= _('Temporal Extent Start Date'))
    temporal_extent_end = FlexiDateFormField(required=False,label= _('Temporal Extent End Date'))
    title = forms.CharField(label = '*' + _('Title'), max_length=255)
    abstract = forms.CharField(label = '*' + _('Abstract'), widget=forms.Textarea(attrs={'cols': 60}))
    constraints_use = forms.ChoiceField(label= _('Contraints'), choices=CONSTRAINT_OPTIONS,
                                        help_text=CONSTRAINT_HELP)
    keywords = taggit.forms.TagField(required=False)
    class Meta:
        model = Layer
        exclude = ('service', 'owner', 'contacts','workspace', 'store', 'name', 'uuid', 'storeType', 'typename', 'topic_category', 'bbox', 'llbbox', 'srs', 'geographic_bounding_box', 'in_gazetteer', 'gazetteer_project' ) #, 'topic_category'

class RoleForm(forms.ModelForm):
    class Meta:
        model = ContactRole
        exclude = ('contact', 'layer')

class PocForm(forms.Form):
    contact = forms.ModelChoiceField(label = _("New point of contact"),
                                     queryset = Contact.objects.exclude(user=None))


class MapForm(forms.ModelForm):
    keywords = taggit.forms.TagField(required=False)
    title = forms.CharField()
    abstract = forms.CharField(widget=forms.Textarea(attrs={'cols': 40, 'rows': 10}), required=False)
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10, 'id':'mapdescription'}), required=False)

    class Meta:
        model = Map
        exclude = ('contact', 'zoom', 'projection', 'center_x', 'center_y', 'owner', 'officialurl', 'urlsuffix', 'keywords', 'use_custom_template', 'group_params')
