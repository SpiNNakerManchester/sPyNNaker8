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
    else:
        raise ImportError(_msg)
else:
    if neo_version.startswith("0.5"):
        pynn8_syntax = False
    else:
        raise ImportError(_msg)
