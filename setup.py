from setuptools import setup

requires = [
    'pyramid',
    'pyramid_jinja2',
    'pyramid_tm',
    'sqlalchemy',
    'waitress',
    'zope.sqlalchemy',
]

setup(name='test',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = invoice:main
      [console_scripts]
      initialize_test_db = invoice.scripts.initialize_db:main
      """,
      )
