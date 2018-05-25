import os

from setuptools import find_packages
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES')) as f:
    CHANGES = f.read()

requires = []
with open(os.path.join(here, 'requirements/base.txt')) as f:
    requires = f.readlines()

tests_require = ''
with open(os.path.join(here, 'requirements/test.txt')) as f:
    tmp = f.readlines()
    tests_require = filter(lambda x: not x.startswith('-r'), tmp)

print('tests_require', tests_require)

setup(
    name='image_api',
    version='0.0',
    description='image-api',
    long_description=README + '\n\n' + CHANGES,
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Pyramid',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
    ],
    author='Nielson Santana',
    author_email='',
    url='',
    keywords='web pyramid pylons',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    extras_require={
        'testing': tests_require,
    },
    install_requires=requires,
    entry_points={
        'paste.app_factory': [
            'main = image_api:main',
        ],
        'console_scripts': [
            'initialize_image_api_db = image_api.scripts.initializedb:main',
        ],
    },
)
