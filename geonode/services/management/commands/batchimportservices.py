from django.core.management.base import BaseCommand
from optparse import make_option
from geonode.services.models import Service
import json
from geonode.people.utils import get_valid_user
import sys

from urlparse import urlparse
from geonode.services.views import _register_cascaded_service, _register_indexed_service, \
    _register_harvested_service, _register_cascaded_layers, _register_indexed_layers, _process_wms_service, \
    _register_arcgis_url, _verify_service_type
from django.db.utils import DatabaseError, IntegrityError
from pprint import pprint
import owslib
import traceback
import logging
logger = logging.getLogger(__name__)

class Command(BaseCommand):

    help = 'Import the list of remote services in the specified file'
    option_list = BaseCommand.option_list + (

        make_option('-o', '--owner', dest="owner", default=None,
                    help="Name of the user account which should own the imported layers"),
        make_option('-r', '--registerlayers', dest="registerlayers", default=False,
                    help="Register all layers found in the service"),
        make_option('-u', '--username', dest="username", default=None,
                    help="Username required to login to this service if any"),
        make_option('-p', '--password', dest="password", default=None,
                    help="Username required to login to this service if any"),
        make_option('-s', '--security', dest="security", default=None,
                    help="Security permissions JSON - who can view/edit"),
    )

    args = 'filename type method'

    def handle(self, filename, console=sys.stdout, **options):
        print 'Beginning process of importing url services by batch'
        logger.debug('Begining process of importing data from different services')
        f = file(filename, 'r')
        for line in f:
            try:
                parts = line.split()
                url = parts[0]
                url = Command.cleanup_url(url)
                print url
                # pass url along to existing ingest code
                u = urlparse(url)
                domain = u.netloc
                user = options.get('user')
                owner = get_valid_user(user)
                print 'owner = ', owner, ', url = ', url

                password = None
                service = None
                type, server = _verify_service_type(url)
                logger.debug("Url being processed " +url+ " of type " +type )
                if type in ['WMS', 'OWS']:
                    service = _process_wms_service(url, domain, "WMS", user, password, owner=owner)
                elif type == 'CSW':
                    service = _register_harvested_service(url, domain, user, password, owner=owner)
                elif type == 'REST':
                    service = _register_arcgis_url(url, None, None, None, owner=owner)

                print '  processed service = ', service
                logger.debug("Processed Service ", service);
            except IntegrityError as integrityError:
                print 'integrity error'
                print '    ', integrityError
                pprint(integrityError)
                exc_type, exc_value, exc_traceback = sys.exc_info()
                print exc_type
                print exc_value
                traceback.print_tb(exc_traceback)
                print
                logger.debug(exc_traceback)
            except:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                print exc_type
                print exc_value
                traceback.print_tb(exc_traceback)
                print
                logger.debug(exc_traceback)
            
            

    @staticmethod
    def cleanup_url(url):
        return Command.cleanup_prefix_url(Command.cleanup_suffix_url(url))


    # clip string back to last http(s)://
    @staticmethod
    def cleanup_prefix_url(url):
        if (len(url) == 0):
            return "";
        lower_url = url.lower()
        i = lower_url.rfind("http://")
        if (i == -1):
            i = lower_url.rfind("https://")
        if (i == -1):
            return ""
        return_url = url[i:]
        return return_url

    # delete special characters from end of string
    @staticmethod
    def cleanup_suffix_url(url):
        clip_characters = '">' + "'"
        for i in range(0, len(url)):
            current = url[-1]
            if (current in clip_characters):
                url = url[0:len(url)-1]
            else:
                return url
        return url

