import pyNN
import os

if not pyNN.__version__.startswith("0.8"):
    raise Exception(
        "PyNN version {} found; SpyNNaker 8 requires PyNN version 0.8".format(
            pyNN.__version__))

pynn_path = os.path.dirname(pyNN.__file__)
spinnaker_dir = os.path.join(pynn_path, "spiNNaker")
spinnaker_init = os.path.join(spinnaker_dir, "__init__.py")

if not os.path.exists(spinnaker_dir):
    os.mkdir(spinnaker_dir)
spinn_file = open(spinnaker_init, "w")
spinn_file.write("from spynnaker8 import *\n")
spinn_file.close()
print "Created", spinnaker_init
