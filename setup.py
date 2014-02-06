from setuptools import setup, find_packages

setup(name='worldmap',
      version= __import__('geonode').get_version(),
      description="Application for serving and sharing geospatial data",
      long_description=open('README.rst').read(),
      classifiers=[
        "Development Status :: 4 - Beta" ], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='GeoNode & WorldMap Developers',
      author_email='worldmap@harvard.edu',
      url='http://github.com/cga-harvard/cga-worldmap',
      license='GPL',
      packages = find_packages(),
      include_package_data=True,
      zip_safe=False,
      entry_points="""
      # -*- Entry points: -*-
      """,
      )


