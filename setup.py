# This program is free software: you can redistribute it and/or modify it under the
# terms of the Apache License (v2.0) as published by the Apache Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE. See the Apache License for more details.
#
# You should have received a copy of the Apache License along with this program.
# If not, see <https://www.apache.org/licenses/LICENSE-2.0>.

"""Build and installation script for delete-cli."""

# standard libs
from setuptools import setup, find_packages

# metadata
from delete.__meta__ import (__appname__, __version__, __authors__, __contact__,
                             __license__, __website__, __keywords__, __description__)


# grab long description from README.rst
with open('README.rst', mode='r') as readme:
    long_description = readme.read()


setup(
    name                 = __appname__,
    version              = __version__,
    author               = __authors__,
    author_email         = __contact__,
    description          = __description__,
    license              = __license__,
    keywords             = __keywords__,
    url                  = __website__,
    packages             = find_packages(),
    include_package_data = True,
    long_description     = long_description,
    classifiers          = ['Development Status :: 5 - Production/Stable',
                            'Topic :: Utilities',
                            'Programming Language :: Python :: 3',
                            'Programming Language :: Python :: 3.7',
                            'Programming Language :: Python :: 3.8',
                            'Operating System :: POSIX :: Linux',
                            'Operating System :: MacOS',
                            'Operating System :: Microsoft :: Windows',
                            'License :: OSI Approved :: Apache Software License', ],
    entry_points         = {'console_scripts': ['delete=delete:main', ]},
    install_requires     = ['cmdkit>=1.2.1', 'logalpha>=2.0.2', ],
    extras_require       = {
        'dev': ['ipython', 'pytest', 'hypothesis', 'pylint', 'sphinx',
                'sphinx-rtd-theme', 'twine', ]},
    data_files = [
        ('share/man/man1', ['man/man1/delete.1', ]),
    ],
)
