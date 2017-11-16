from pyNN import __version__ as pynn_version
from neo import __version__ as neo_version


_msg = "pyNN version {} and neo version {} are not supported together. \n" \
       "Tested combinations are: \n" \
       "\tpyNN 0.8.3 and neo 0.4.0 or\n" \
       "\tpyNN 0.8.3 and neo 0.4.1 or\n" \
       "\tpyNN 0.9.1 and neo 0.5.2".format(pynn_version, neo_version)

print("Detected pynn version {} and neo version {}"
      "".format(pynn_version, neo_version))

if pynn_version.startswith("0.8"):
    if neo_version.startswith("0.3") or neo_version.startswith("0.4"):
        pynn8_syntax = True
        print ("WARNING PyNN 0.8 is deprecated at the request of the PyNN "
               "team. \n Please upgrade your PyNN and Neo installations to "
               "at least PyNN 0.9.2 and neo 0.5.2\nIf you specifcally need "
               "PyNN 0.8 please contact us URGENTLY otherwise PyNN 0.8 will "
               "be removed with the next sub release. (Before PyNN 0.7")
    else:
        raise ImportError(_msg)
else:
    if neo_version.startswith("0.5"):
        pynn8_syntax = False
    else:
        raise ImportError(_msg)
