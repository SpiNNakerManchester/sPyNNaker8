from pyNN import __version__ as pynn_version
from neo import __version__ as neo_version
from distutils.version import StrictVersion

_msg = "pyNN version {} and neo version {} are not supported together.\n" \
       "Tested combinations are:\n" \
       "\tpyNN 0.8.3 and neo 0.4.0 or\n" \
       "\tpyNN 0.8.3 and neo 0.4.1 or\n" \
       "\tpyNN 0.9.1 and neo 0.5.2".format(pynn_version, neo_version)
_pynn_ver = StrictVersion(pynn_version)
_neo_ver = StrictVersion(neo_version)

print("Detected pynn version {} and neo version {}".format(
    pynn_version, neo_version))

if _pynn_ver >= "0.9": 
    if _neo_ver < "0.5":
        raise ImportError(_msg)
    pynn8_syntax = False
elif _pynn_ver >= "0.8":
    if _neo_ver < "0.3" or _neo_ver >= "0.5":
        raise ImportError(_msg)
    pynn8_syntax = True
    print("WARNING: PyNN 0.8 is deprecated at the request of the PyNN team.")
    print("Please upgrade your PyNN and Neo installations to at least "
          "PyNN 0.9.2 and Neo 0.5.2")
    print("If you specifically need PyNN 0.8 please contact us *URGENTLY* "
          "otherwise PyNN 0.8 will be removed with the next sub-release. "
          "(Before PyNN 0.7")
else:
    # Really old version of PyNN?! How...
    raise ImportError(_msg)
