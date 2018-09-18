import os
from setuptools import setup, find_packages
from os import path
from io import open

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Put templates at proper place
def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths

extra_files = package_files('openshift_cic/templates')


setup(
    name='openshift_cic',
    version='1.0.0',
    description='An Openshift Gluster Configuration Generator',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/red-hat-storage/openshift-cic',
    author='Ramakrishna Reddy Yekulla',
    author_email='rreddy@redhat.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: System Administrator',
        'Topic :: Software Development :: Config Generator',
        'License :: OSI Approved :: GPLv3 License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
    packages=['openshift_cic',],
    package_data={'': extra_files},
    install_requires=['jinja2'],
    entry_points={
        'console_scripts': [
            'cic=openshift_cic.cic',
        ],
    }

)
