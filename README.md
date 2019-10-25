sPyNNaker8 has now been merged into [sPynnaker](https://github.com/SpiNNakerManchester/sPyNNaker)


Please replace the import lines as followes.

import spynnaker8 as ....
becomes  
import spynnaker as ...

import spynnaker8.XYZ ...
becomes  
import spynnaker.pyNN.XYZ ....

You may also need to run:
    spynnaker.pyNN.setup_pynn.py

[![Build Status](https://travis-ci.org/SpiNNakerManchester/sPyNNaker8.svg?branch=master)](https://travis-ci.org/SpiNNakerManchester/sPyNNaker8)
[![Coverage Status](https://coveralls.io/repos/github/SpiNNakerManchester/sPyNNaker8/badge.svg?branch=master)](https://coveralls.io/github/SpiNNakerManchester/sPyNNaker8?branch=master)



``