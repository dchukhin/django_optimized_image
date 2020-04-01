import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-optimized-image',
    version='0.3.0',
    packages=find_packages(),
    include_package_data=True,
    license='BSD License',
    description='A simple Django app that allows for optimization of images.',
    long_description=README,
    install_requires=['tinify'],
    url='https://github.com/dchukhin/django_optimized_image',
    download_url='https://github.com/dchukhin/django_optimized_image/tarball/0.3.0',
    author='Dmitriy Chukhin',
    author_email='dchukhin@caktusgroup.com',
    keywords=['django', 'image', 'optimize', 'imagefield'],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
