import os
from distutils.version import StrictVersion as Version
import pyNN


def version_satisfies(module, requirement):
    """ Perform a version check. This code could be smarter...
    """
    return Version(module.__version__) > Version(requirement)


def install_sPyNNaker8_into(module):
    """ Do the actual installation by creating a package within the given\
        module's implementation. This is very nasty!
    """
    spinnaker_dir = os.path.join(os.path.dirname(module.__file__), "spiNNaker")
    if not os.path.exists(spinnaker_dir):
        os.mkdir(spinnaker_dir)

    spinnaker_init = os.path.join(spinnaker_dir, "__init__.py")
    with open(spinnaker_init, "w") as spinn_file:
        spinn_file.write("from spynnaker8 import *\n")

    print("Created {}".format(spinnaker_init))


# Check the version; we really want PyNN 0.9
if not version_satisfies(pyNN, "0.9"):
    raise Exception(
        "PyNN version {} found; SpyNNaker 9 requires PyNN version 0.9".format(
            pyNN.__version__))

# Perform the installation
install_sPyNNaker8_into(pyNN)
