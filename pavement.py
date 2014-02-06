from __future__ import with_statement
from paver import svn
from paver.easy import *
from paver.easy import options
from paver.path25 import pushd
import functools
import os
import sys
import time
from datetime import date
import socket
import ConfigParser
import paver.doctools
import paver.misctasks
import pkg_resources
import subprocess
import shutil
from shutil import move, copy
import zipfile
import tarfile
import urllib
from urllib import urlretrieve
import glob

assert sys.version_info >= (2,7),\
SystemError("WorldMap Build requires python 2.7 or better")

venv = os.environ.get('VIRTUAL_ENV')
curdir = os.getcwd()

settings_file = os.environ.get("DJANGO_SETTINGS_MODULE", "geonode.settings.base")
os.environ["DJANGO_SETTINGS_MODULE"] = settings_file

deploy_req_txt = """
# NOTE... this file is generated
-r %(curdir)s/requirements/base.txt
-e %(curdir)s
""" % locals()

bundle = path('package/worldmap.pybundle')
dlname = 'worldmap.bundle'

geoserver_target = path('src/geoserver-geonode-ext/target/geoserver.war')
gs_data = "./webapps/gs-data"
gs_data_url="http://worldmap.harvard.edu/media/geoserver/geonode-geoserver-data.zip"

package_outdir = "./package"

def geonode_client_target(): return package_outdir / "geonode-client.zip"
geonode_client_target_war = path('webapps/geonode-client.war')




geonetwork_target = path('webapps/geonetwork.war')
geonetwork_zip="geonetwork.war"
geonetwork_war_url="http://worldmap.harvard.edu/media/geoserver/"
intermap_war_url="http://worldmap.harvard.edu/media/geoserver/intermap.war"



@task
def install_deps(options):
    """Installs all the python deps from a requirements file"""
    if bundle.exists():
        info('using to install python deps bundle')
        call_task('install_bundle')
    else:
        info('Installing from requirements file. '\
             'Use "paver bundle_deps" to create an install bundle')
        pip_install("-r requirements/base.txt")
        pip_install('-e .')


@task
def bundle_deps(options):
    """
    Create a pybundle of all python dependencies.  If created, this
    will be the default for installing python deps.
    """
    pip_bundle("-r requirements/base.txt %s" % bundle)


@task
def install_bundle(options):
    """
    Installs a bundle of dependencies located at %s.
    """ % bundle

    info('install the bundle')
    pip_install(bundle)




@task
def install_25_deps(options):
    """Fetch python 2_5-specific dependencies (not maintained)"""
    pass



#TODO Move svn urls out to a config file

def grab(src, dest):
    urlretrieve(str(src), str(dest))

@task
def setup_gs_data(options):
    """Fetch a data directory to use with GeoServer for testing."""
    src_url = gs_data_url
    dev = path("./webapps")
    if not dev.exists():
        dev.mkdir()

    dst_url = dev / "geonode-geoserver-data.zip"
    grab(src_url, dst_url)

    if getattr(options, 'clean', False): path(gs_data).rmtree()
    if not path(gs_data).exists(): unzip_file(dst_url, gs_data)


@task
@needs(['setup_gs_data'])
def setup_geoserver(options):
    """Prepare a testing instance of GeoServer."""
    with pushd('src/geoserver-geonode-ext'):
        sh("mvn clean install")

@task
def setup_geonetwork(options):
    """Fetch the geonetwork.war and intermap.war to use with GeoServer for testing."""
    war_zip_file = geonetwork_zip
    src_url = str(geonetwork_war_url + war_zip_file)
    info("geonetwork url: %s" %src_url)
    # where to download the war files. If changed change also
    # src/geoserver-geonode-ext/jetty.xml accordingly

    webapps = path("./webapps")
    if not webapps.exists():
        webapps.mkdir()

    dst_url = webapps / war_zip_file
    dst_war = webapps / "geonetwork.war"
    deployed_url = webapps / "geonetwork"

    if getattr(options, 'clean', False):
        deployed_url.rmtree()

    if not dst_war.exists():
    	info("getting geonetwork.war")
        grab(src_url, dst_url)
        zip_extractall(zipfile.ZipFile(dst_url), webapps)
    if not deployed_url.exists():
        zip_extractall(zipfile.ZipFile(dst_war), deployed_url)

    src_url = intermap_war_url
    dst_url = webapps / "intermap.war"

    if not dst_url.exists():
        grab(src_url, dst_url)

@task
@needs([
    'setup_geoserver',
    'setup_geonetwork',
    'setup_geonode_client'
])
def setup_webapps(options):
    pass


@task
@needs([
    'install_deps',
    'setup_webapps',
    'sync_django_db',
    'package_client'
])
def build(options):
    """Get dependencies and generally prepare a WorldMap development environment."""
    info("""WorldMap development environment successfully set up.\nIf you have not set up an administrative account, please do so now.\nUse "paver host" to start up the server.""")


@task
@needs([
    'build'
])
def setup(options):
    """Get dependencies and generally prepare a WorldMap development environment."""
    info("""Deprecated - use 'paver setup' instead""")


@task
@needs([
    'install_deps',
    'setup_geonode_client',
    'sync_django_db',
    'package_client'
])
def fastbuild(options):
    """Get dependencies and generally prepare a WorldMap development environment."""
    info("""WorldMap development environment successfully set up minus GeoServer and Geonetwork.\nIf you have not set up an administrative account, please do so now.\nUse "paver host" to start up the server.""")


@task
def setup_geonode_client(options):
    """
    Fetch geonode-client
    """
    static = path("./geonode/static/geonode")
    if not static.exists():
        static.mkdir()

    sh("git submodule update --init")

    with pushd("src/geonode-client/"):
        sh("ant clean zip")

    src_zip = "src/geonode-client/build/geonode-client.zip"
    zip_extractall(zipfile.ZipFile(src_zip), static)


@task
def sync_django_db(options):
    sh("python manage.py syncdb  --noinput")
    try:
        sh("python manage.py syncdb --database=wmdata  --noinput")
    except:
        info("******CREATION OF GAZETTEER TABLE FAILED - if you want the gazetteer enabled, \n \
unescape the 'DATABASES' AND 'DATABASE_ROUTERS' settings in your settings file \n \
and modify the default values if necessary")
    sh("python manage.py migrate --noinput")


@task
def package_dir(options):
    """
    Adds a packaging directory
    """
    package_path = path(package_outdir)
    if not package_path.exists():
        package_outdir.mkdir()


@task
@needs('package_dir', 'setup_geonode_client')
@cmdopts([
    ('use_war', 'w', 'Use a war to deploy geonode-client')
])
def package_client(options):
    """Package compressed client resources (JavaScript, CSS, images)."""

    if(hasattr(options, 'use_war')):
    	geonode_client_target_war.copy(options.deploy.out_dir)
    else:
        # Extract static files to static_location
    	geonode_media_dir = path("./geonode/media")
        static_location = geonode_media_dir / "static"

        dst_zip = "src/geonode-client/build/geonode-client.zip"

        zip_extractall(zipfile.ZipFile(dst_zip), static_location)
        os.remove(dst_zip)

@task
@needs('package_dir', 'setup_geoserver')
def package_geoserver(options):
    """Package GeoServer WAR file with appropriate extensions."""
    geoserver_target.copy(package_outdir)


@task
@needs('package_dir', 'setup_geonetwork')
def package_geonetwork(options):
    """Package GeoNetwork WAR file for deployment."""
    geonetwork_target.copy(package_outdir)


@task
@needs('package_dir')
def package_webapp(options):

    sh("python manage.py collectstatic -v0  --noinput")

    """Package (Python, Django) web application and dependencies."""
    #with pushd('worldmap'):
    
    req_file = path('package/requirements.txt')
    req_file.write_text(deploy_req_txt)    
    
    sh('python setup.py egg_info sdist')
    pip_bundle("-r %s package/worldmap-webapp.pybundle" % (req_file))


@task
@needs(
    'build',
    'package_geoserver',
    'package_geonetwork',
    'package_webapp',
    'package_bootstrap'
)
def package_all(options):
    info('all is packaged, ready to deploy')


def create_version_name():
    # we'll use the geonodepy version as our "official" version number
    # for now
    slug = "WorldMap-%s" % (
        pkg_resources.get_distribution('worldmap').version,
        date.today().isoformat()
    )

    return slug


@task
@cmdopts([
    ('name=', 'n', 'Release number or name'),
    ('no_svn', 'D', 'Do not append svn version number as part of name '),
    ('append_to=', 'a', 'append to release name'),
    ('skip_packaging', 'y', 'Do not call package_all when creating a release'),
])
def make_release(options):
    """
    Creates a tarball to use for building the system elsewhere
    (production, distribution, etc)
    """

    if not hasattr(options, 'skip_packaging'):
        call_task("package_all")
    if hasattr(options, 'name'):
        pkgname = options.name
    else:
        pkgname = create_version_name()
        if hasattr(options, 'append_to'):
            pkgname += options.append_to

    out_pkg = path(pkgname)
    out_pkg.rmtree()
    path('./package').copytree(out_pkg)

    tar = tarfile.open("%s.tar.gz" % out_pkg, "w:gz")
    for file in out_pkg.walkfiles():
        tar.add(file)
    tar.add('README.release.rst', arcname=('%s/README.rst' % out_pkg))
    tar.close()

    out_pkg.rmtree()
    info("%s.tar.gz created" % out_pkg.abspath())


def unzip_file(src, dest):
    zip = zipfile.ZipFile(src)
    if not path(dest).exists():
        path(dest).makedirs()

    for name in zip.namelist():
        if name.endswith("/"):
            (path(dest) / name).makedirs()
        else:
            parent, file = path(name).splitpath()
            parent = path(dest) / parent
            if parent and not parent.isdir():
                path(parent).makedirs()
            out = open(path(parent) / file, 'wb')
            out.write(zip.read(name))
            out.close()


def pip(*args):
    try:
        pkg_resources.require('pip>=0.6')
    except :
        error("**ATTENTION**: Update your 'pip' to at least 0.6")
        raise

    full_path_pip = 'pip'

    sh("%(cmd)s %(args)s" % {
        "cmd": full_path_pip,
        "args": " ".join(args)
    })

pip_install = functools.partial(pip, 'install')
pip_bundle = functools.partial(pip, 'bundle')


@task
@needs('package_dir')
def package_bootstrap(options):
    """Create a bootstrap script for deployment"""

    try:
        from paver.virtual import bootstrap
        options.virtualenv = options.deploy
        call_task("paver.virtual.bootstrap")
    except ImportError, e:
        info("VirtualEnv must be installed to enable 'paver bootstrap'. If you " +
             "need this command, run: pip install virtualenv")

@task
@needs(['start'])
@cmdopts([
             ('bind=', 'b', 'Bind server to provided IP address and port number.')
         ], share_with=['start_django'])
def host():
    """
    Start GeoNode (Django, GeoServer & Client)
    """
    info("Deprecated - use 'paver start' instead")

@task
@needs(['install_deps',
        'start_django',
        'start_geoserver'])
@cmdopts([
    ('bind=', 'b', 'Bind server to provided IP address and port number.')
], share_with=['start_django'])
def start():
    """
    Start WorldMap (Django, GeoServer & Client)
    """
    info("WorldMap is now available.")

@task
def stop_django():
    """
    Stop the WorldMap Django application
    """
    kill('python', 'runserver')


@task
def stop_geoserver():
    """
    Stop GeoServer
    """
    kill('java', 'jetty')


@task
def stop():
    """
    Stop WorldMap
    """
    info("Stopping WorldMap ...")
    stop_django()
    stop_geoserver()



@cmdopts([
    ('bind=', 'b', 'Bind server to provided IP address and port number.')
])
@task
@needs(['install_deps'])
def start_django():
    """
    Start the WorldMap Django application
    """
    bind = options.get('bind', '')
    sh('python manage.py runserver %s &' % bind)
    

@task
@cmdopts([
    ('bind=', 'b', 'IP address to bind to. Default is localhost.')
])
def start_geoserver(options):
    from django.conf import settings
    
    url = "http://localhost:8080/geoserver/"
    if settings.GEOSERVER_BASE_URL != url:
        print 'your GEOSERVER_BASE_URL does not match %s' % url
        sys.exit(1)
	
	
    jettylog = open("jetty.log", "w")
    with pushd("src/geoserver-geonode-ext"):
        os.environ["MAVEN_OPTS"] = " ".join([
            "-XX:CompileCommand=exclude,net/sf/saxon/event/ReceivingContentHandler.startElement",
            "-Xmx512M",
            "-XX:MaxPermSize=256m"
        ])
        mvn = subprocess.Popen(
            ["mvn", "jetty:run"],
            stdout=jettylog,
            stderr=jettylog
        )


    socket.setdefaulttimeout(1)

    info("Logging servlet output to jetty.log...")
    info("Jetty is starting up, please wait...")
    waitfor(settings.GEOSERVER_BASE_URL)
    info("Development GeoServer/GeoNetwork is running")
    sh('python manage.py updatelayers') 
  


@task
def test(options):
    pip_install("-r requirements/test.txt")
    sh("python manage.py test --settings=geonode.settings.test")


def zip_extractall(zf, path=None, members=None, pwd=None):
    if sys.version_info >= (2, 6, 2):
        zf.extractall(path=path, members=members, pwd=pwd)
    else:
        _zip_extractall(zf, path=path, members=members, pwd=pwd)

def _zip_extractall(zf, path=None, members=None, pwd=None):
    """Extract all members from the archive to the current working
       directory. `path' specifies a different directory to extract to.
       `members' is optional and must be a subset of the list returned
       by namelist().
    """
    if members is None:
        members = zf.namelist()

    for zipinfo in members:
        _zip_extract(zf, zipinfo, path, pwd)

def _zip_extract(zf, member, path=None, pwd=None):
    """Extract a member from the archive to the current working directory,
       using its full name. Its file information is extracted as accurately
       as possible. `member' may be a filename or a ZipInfo object. You can
       specify a different directory using `path'.
    """
    if not isinstance(member, zipfile.ZipInfo):
        member = zf.getinfo(member)

    if path is None:
        path = os.getcwd()

    return _zip_extract_member(zf, member, path, pwd)


def _zip_extract_member(zf, member, targetpath, pwd):
    """Extract the ZipInfo object 'member' to a physical
       file on the path targetpath.
    """
    # build the destination pathname, replacing
    # forward slashes to platform specific separators.
    # Strip trailing path separator, unless it represents the root.
    if (targetpath[-1:] in (os.path.sep, os.path.altsep)
        and len(os.path.splitdrive(targetpath)[1]) > 1):
        targetpath = targetpath[:-1]

    # don't include leading "/" from file name if present
    if member.filename[0] == '/':
        targetpath = os.path.join(targetpath, member.filename[1:])
    else:
        targetpath = os.path.join(targetpath, member.filename)

    targetpath = os.path.normpath(targetpath)

    # Create all upper directories if necessary.
    upperdirs = os.path.dirname(targetpath)
    if upperdirs and not os.path.exists(upperdirs):
        os.makedirs(upperdirs)

    if member.filename[-1] == '/':
        if not os.path.isdir(targetpath):
            os.mkdir(targetpath)
        return targetpath

    source = zf.open(member, pwd=pwd)
    target = file(targetpath, "wb")
    shutil.copyfileobj(source, target)
    source.close()
    target.close()

    return targetpath

def kill(arg1, arg2):
    """Stops a proces that contains arg1 and is filtered by arg2
    """
    from subprocess import Popen, PIPE

    # Wait until ready
    t0 = time.time()
    # Wait no more than these many seconds
    time_out = 30
    running = True

    while running and time.time() - t0 < time_out:
        p = Popen('ps aux | grep %s' % arg1, shell=True,
                  stdin=PIPE, stdout=PIPE, stderr=PIPE, close_fds=True)

        lines = p.stdout.readlines()

        running = False
        for line in lines:

            if '%s' % arg2 in line:
                running = True

                # Get pid
                fields = line.strip().split()

                info('Stopping %s (process number %s)' % (arg1, fields[1]))
                kill = 'kill -9 %s 2> /dev/null' % fields[1]
                os.system(kill)

        # Give it a little more time
        time.sleep(1)
    else:
        pass

    if running:
        raise Exception('Could not stop %s: '
                        'Running processes are\n%s'
                        % (arg1, '\n'.join([l.strip() for l in lines])))


def waitfor(url, timeout=300):
    started = False
    for a in xrange(timeout):
        try:
            resp = urllib.urlopen(url)
        except IOError, e:
            pass
        else:
            if resp.getcode() == 200:
                started = True
                break
        time.sleep(1)
    return started


def justcopy(origin, target):
    import shutil
    if os.path.isdir(origin):
        shutil.rmtree(target, ignore_errors=True)
        shutil.copytree(origin, target)
    elif os.path.isfile(origin):
        if not os.path.exists(target):
            os.makedirs(target)
        shutil.copy(origin, target)

@task
@needs(['package_geonetwork', 'package_geoserver'])
def package(options):
    """
    Creates a tarball to use for building the system elsewhere
    """
    import pkg_resources
    import tarfile
    import geonode

    version = geonode.get_version()
    # Use WorldMap's version for the package name.
    pkgname = 'worldmap-%s-all' % version

    # Create the output directory.
    out_pkg = path(pkgname)
    out_pkg_tar = path("%s.tar.gz" % pkgname)

    # Create a distribution in zip format for the WorldMap python package.
    dist_dir = path('dist')
    dist_dir.rmtree()
    sh('python setup.py sdist --formats=zip')

    with pushd('package'):

        #Delete old tar files in that directory
        for f in glob.glob('worldmap*.tar.gz'):
            old_package = path(f)
            if old_package != out_pkg_tar:
                old_package.remove()

        if out_pkg_tar.exists():
            info('There is already a package for version %s' % version)
            return

        # Clean anything that is in the oupout package tree.
        out_pkg.rmtree()
        out_pkg.makedirs()

        support_folder = path('support')
        install_file = path('install.sh')

        # And copy the default files from the package folder.
        justcopy(support_folder, out_pkg / 'support')
        justcopy(install_file, out_pkg)

        geonode_dist = path('..') / 'dist' / 'worldmap-%s.zip' % version
        justcopy(geonode_dist, out_pkg)

        # Create a tar file with all files in the output package folder.
        tar = tarfile.open(out_pkg_tar, "w:gz")
        for file in out_pkg.walkfiles():
            tar.add(file)

        # Add the README with the license and important links to documentation.
        #tar.add('README.rst', arcname=('%s/README.rst' % out_pkg))
        tar.close()

        # Remove all the files in the temporary output package directory.
        out_pkg.rmtree()

    # Report the info about the new package.
    info("%s created" % out_pkg_tar.abspath())
