import os
from setuptools import setup
from collections import defaultdict

__version__ = None
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

setup(
    name="sPyNNaker8",
    version=__version__,
    description="Tools for simulating neural models generated using "
                "PyNN 0.8 on the SpiNNaker platform",
    author="University of Manchester",
    classifiers=[
        "Development Status :: 3 - Alpha",

        "Intended Audience :: Science/Research",

        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",

        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",

        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",

        "Topic :: Scientific/Engineering",
    ],
    keywords="spinnaker pynn0.8 neural simulation",
    url="https://github.com/SpiNNakerManchester/SpyNNaker8",
    packages=packages,
    package_data=package_data,
    install_requires=[
        'SpiNNUtilities >= 1!4.0.1, < 1!5.0.0',
        'SpiNNStorageHandlers >= 1!4.0.1, < 1!5.0.0',
        'SpiNNMachine >= 1!4.0.1, < 1!5.0.0',
        'SpiNNMan >= 1!4.0.1, < 1!5.0.0',
        'SpiNNaker_PACMAN >= 1!4.0.1, < 1!5.0.0',
        'SpiNNaker_DataSpecification >= 1!4.0.1, < 1!5.0.0',
        'spalloc >= 1.0.1, < 2.0.0',
        'SpiNNFrontEndCommon >= 1!4.0.1, < 1!5.0.0',
        'sPyNNaker >= 1!4.0.1, < 1!5.0.0',
        'quantities >= 0.12.1',
        'pynn >= 0.9.1, < 0.10.0 ',
        'lazyarray >= 0.2.9, <= 0.4.0',
        'appdirs >= 1.4.2 , < 2.0.0',
        'neo >= 0.5.2, < 0.7.0']
)
