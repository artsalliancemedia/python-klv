from distutils.core import setup
from klv import __version__

setup(
    name='klv',
    version=__version__,
    license='MIT',
    description='Key Length Value encoding and decoding',
    author='Arts Alliance Media',
    author_email='dev@artsalliancemedia.com',
    url='https://github.com/artsalliancemedia/python-klv',
    packages=('klv',),
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    )
)