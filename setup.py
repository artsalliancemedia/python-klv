"""
Setup script for peepingtom
"""

from distutils.core import setup
from klv import __version__

setup(
    name='klv',
    version=__version__,
    description='Key Length Value encoding and decoding'
    author='Arts Alliance Media',
    author_email='dev@artsalliancemedia.com',
    url='http://www.artsalliancemedia.com',
    packages='klv'
)