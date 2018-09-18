# -*- coding: utf-8 -*-
"""Installer for the collective.pfgsharepoint package."""

from setuptools import find_packages
from setuptools import setup


long_description = '\n\n'.join([
    open('README.rst').read(),
    open('CONTRIBUTORS.rst').read(),
    open('CHANGES.rst').read(),
])


setup(
    name='msgraph-api',
    version='0.1a1',
    description="A python package to make using the Microsoft Graph API easier to use.",
    long_description=long_description,
    # Get more from https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Environment :: Web Environment",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords='Python Graph API',
    author='Michael Finney',
    author_email='mjfinney@gmail.com',
    url='https://pypi.python.org/pypi/msgraph-api',
    license='GPL version 2',
    packages=find_packages('src', exclude=['ez_setup']),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        # -*- Extra requirements: -*-
        'requests',
        'setuptools',
    ],
    extras_require={
        'test': [
            'nose',
            'mock',
            'requests-mock',
        ],
    },
)
