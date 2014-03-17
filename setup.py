from setuptools import setup, find_packages
import os

version = '1.0'

setup(name='uniofleicester.jscontent',
      version=version,
      description="Add-on for extedned Page views",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='accordion tabbed plone',
      author='Matous Hora',
      author_email='matous@fry-it.com',
      url='https://github.com/university-of-leicester/uniofleicester.jscontent',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['uniofleicester'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      setup_requires=["PasteScript"],
      paster_plugins=["ZopeSkel"],
      )
