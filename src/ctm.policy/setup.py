from setuptools import setup, find_packages
import os

version = '1.4dev'

setup(name='ctm.policy',
      version=version,
      description="Paquet que crea l'entorn de treball dels portals del CTM",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='',
      author='Ferran Llamas',
      author_email='llamas.arroniz@gmail.com',
      url='http://svn.plone.org/svn/collective/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['ctm'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'ctm.theme',
          'collective.upload',
          'collective.plonetruegallery',
          'collective.ptg.fancybox',
          'quintagroup.dropdownmenu',
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
