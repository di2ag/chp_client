import os
import sys
import re
import io

from setuptools import find_packages
from setuptools import setup

__version__ = re.search(r'__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        io.open('chp_client/_version.py', encoding='utf_8_sig').read()).group(1)

REQUIRED_PACKAGES = [
    'requests'
]

setup(
    name='chp_client',
    version=__version__,
    author='Chase Yakaboski',
    author_email='chase.th@dartmouth.edu',
    description='A light weight Python wrapper of the NCATS CHP Endpoint.',
    packages=find_packages(),
    install_requires=REQUIRED_PACKAGES,
    python_requires='>=3.6'
)

