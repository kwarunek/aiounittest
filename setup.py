#!/usr/bin/env python
# -*- coding:utf-8 -*-
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='aiounittest',
    packages=['aiounittest'],
    version='1.2.1',
    author='Krzysztof Warunek',
    author_email='krzysztof@warunek.net',
    description='Test asyncio code more easily.',
    include_package_data=True,
    keywords='asyncio, async, unittest, coroutine',
    url='https://github.com/kwarunek/aiounittest',
    long_description=open('README.rst').read(),
    tests_require=['nose', 'coverage'],
    license="MIT",
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ]
)
