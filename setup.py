# Copyright (c) 2017-2019 The University of Manchester
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
from setuptools import setup
from collections import defaultdict

__version__ = None
__version_type__ = None
exec(open("spynnaker8/_version.py").read())
assert __version__


# Build a list of all project modules, as well as supplementary files
main_package = "spynnaker8"
extensions = {".aplx", ".boot", ".cfg", ".json", ".sql", ".template", ".xml",
              ".xsd"}
main_package_dir = os.path.join(os.path.dirname(__file__), main_package)
start = len(main_package_dir)
packages = []
package_data = defaultdict(list)
for dirname, dirnames, filenames in os.walk(main_package_dir):
    if '__init__.py' in filenames:
        package = "{}{}".format(
            main_package, dirname[start:].replace(os.sep, '.'))
        packages.append(package)
    for filename in filenames:
        _, ext = os.path.splitext(filename)
        if ext in extensions:
            package = "{}{}".format(
                main_package, dirname[start:].replace(os.sep, '.'))
            package_data[package].append(filename)

install_requires = [
    'SpiNNUtilities >= 1!5.1.1, < 1!6.0.0',
    'SpiNNMachine >= 1!5.1.1, < 1!6.0.0',
    'SpiNNMan >= 1!5.1.1, < 1!6.0.0',
    'SpiNNaker_PACMAN >= 1!5.1.1, < 1!6.0.0',
    'SpiNNaker_DataSpecification >= 1!5.1.1, < 1!6.0.0',
    'spalloc >= 2.0.2, < 3.0.0',
    'SpiNNFrontEndCommon >= 1!5.1.1, < 1!6.0.0',
    'sPyNNaker >= 1!5.1.1, < 1!6.0.0',
    'quantities >= 0.12.1',
    'pynn >= 0.9.1, < 0.10.0 ',
    'lazyarray >= 0.2.9, <= 0.4.0',
    'appdirs >= 1.4.2 , < 2.0.0',
    'neo >= 0.5.2, < 0.9.0']
if os.environ.get('READTHEDOCS', None) != 'True':
    install_requires.append('scipy')
    install_requires.append('csa')

long_description = {}
this_directory = os.path.abspath(os.path.dirname(__file__))
try:
    with open(os.path.join(this_directory, 'README.md')) as f:
        long_description["long_description"] = f.read()
        long_description["long_description_content_type"] = "text/markdown"
except IOError:
    # If we can't read the long description, so be it; it's not a fatal error
    pass

# Classifiers: https://pypi.org/classifiers/
_status_map = {
    "alpha": "Development Status :: 3 - Alpha",
    "beta": "Development Status :: 4 - Beta",
    "production": "Development Status :: 5 - Production/Stable",
}
assert __version_type__ in _status_map

setup(
    name="sPyNNaker8",
    version=__version__,
    description="Tools for simulating neural models generated using "
                "PyNN 0.9 on the SpiNNaker platform",
    author="University of Manchester",
    classifiers=[
        _status_map[__version_type__],

        "Environment :: Console",

        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",

        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",

        "Natural Language :: English",

        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",

        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",

        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Neuroscience",
    ],
    keywords=["spinnaker", "pynn0.9", "neural simulation"],
    url="https://github.com/SpiNNakerManchester/SpyNNaker8",
    packages=packages,
    package_data=package_data,
    install_requires=install_requires,
    maintainer="SpiNNaker Team",
    maintainer_email="spinnakerusers@googlegroups.com",
    **long_description
)
