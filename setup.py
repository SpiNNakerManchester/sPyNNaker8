from setuptools import setup, find_packages
from spynnaker8._version import __version__

setup(
    name="sPyNNaker8",
    version=__version__,
    packages=find_packages(),
    package_data={'spynnaker8': ['model_binaries/*.aplx']},

    # Metadata for PyPi
    url="https://github.com/SpiNNakerManchester/sPyNNaker8",
    author="University of Manchester",
    description="Tools for simulating neural models generated using "
                "PyNN 0.8 on the SpiNNaker platform",
    license="GPLv????",
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

    # Requirements
    install_requires=[
        "pynn>=0.8, <=0.9", "SpiNNFrontEndCommon",
        "PACMAN", "SpiNNMan", "sPyNNaker",
        "spalloc >= 0.2.4",  # For machine allocation
        "deprecation >= 1.0, < 2.0.0",
        "six >=1.0.0, <= 1.6.1",
        "numpy >= 1.9.0, <=1.9.1",
        "scipy >=0.16.0, <=0.16.0",
        "bitarray >=0.8.1, <=0.8.1",
        "quantities  >= 0.11.1, <= 0.11.1",
        'lazyarray >= 0.2.9, <= 0.2.9',
        'appdirs >=1.4.2 , <=1.4.2',
        'neo >= 0.3.0, <=0.4.1'
    ],
)
