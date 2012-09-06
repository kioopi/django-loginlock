#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
execfile('loginlock/version.py')

setup(
    name='django-loginlock',
    version=__version__,
    description="""Block login from user/ip combination after a number
of failed login attempts in Django projects.""",
    long_description=open('README.md', 'r').read(),
    keywords='django, security, authentication, bruteforce, login',
    author='Vangelis Tsoumenis',
    author_email='kioopi@gmail.com',
    url='http://github.com/kioopi/django-loginlock/',
    license='MIT',
    package_dir={'loginlock': 'loginlock'},
    include_package_data=True,
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Security',
        'Topic :: System :: Logging',
    ],
    zip_safe=False,
)
