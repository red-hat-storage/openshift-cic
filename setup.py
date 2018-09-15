from setuptools import setup, find_packages
from os import path
from io import open

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='openshift_cic',
    version='0.0.1',
    description='An Openshift Gluster Configuration Generator',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/ramkrsna/openshift-cic',
    author='RAMKY',
    author_email='ramkrsna@redhat.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: System Administrator',
        'Topic :: Software Development :: Config Generator',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
    packages=find_packages(exclude=['tests']),
    install_requires=['jinja2'],
    entry_points={
        'console_scripts': [
            'cic=openshift_cic.cic:main',
        ],
    }

)
