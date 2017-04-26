import os
from setuptools import setup
from collections import defaultdict

exec(open("spynnaker8/_version.py").read())

if os.environ.get('READTHEDOCS', None) == 'True':
    # scipy must be added in config.py as a mock
    install_requires = ['sPyNNaker == 1!4.0.0a1',
                        'pynn>=0.8, <0.9',
                        'deprecation >= 1.0, < 2.0.0',
                        'six >=1.0.0, < 2.0.0',
                        'numpy >= 1.9.0',
                        'quantities  >= 0.11.1, <= 0.11.1',
                        'lazyarray >= 0.2.9, <= 0.2.9',
                        'appdirs >=1.4.2 , < 2.0.0',
                        'neo >= 0.3.0, <=0.4.1'],
else:
    install_requires = ['sPyNNaker == 1!4.0.0a1',
                        'pynn>=0.8, <0.9',
                        'deprecation >= 1.0, < 2.0.0',
                        'six >=1.0.0, < 2.0.0',
                        'numpy >= 1.9.0',
                        'scipy',
                        'quantities >= 0.11.1, <= 0.11.1',
                        'lazyarray >= 0.2.9, <= 0.2.9',
                        'appdirs >=1.4.2 , < 2.0.0',
                        'neo >= 0.3.0, <=0.4.1'],

# Build a list of all project modules, as well as supplementary files
main_package = "spynnaker8"
data_extensions = {".aplx", ".xml", ".json", ".xsd"}
config_extensions = {".cfg", ".template"}
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
        if ext in data_extensions:
            package = "{}{}".format(
                main_package, dirname[start:].replace(os.sep, '.'))
            package_data[package].append("*{}".format(ext))
            break
        if ext in config_extensions:
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
    install_requires=install_requires
)











