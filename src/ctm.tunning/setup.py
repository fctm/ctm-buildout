from setuptools import setup, find_packages
import sys, os

version = '0.0'

setup(name='ctm.tunning',
      version=version,
      description="Tunning package for ctm sites",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Ramon Navarro Bosch',
      author_email='r.navarro@iskra.cat',
      url='http://iskra.cat',
      license='GPL',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      namespace_packages=['ctm'],
      install_requires=[
          'setuptools'
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
