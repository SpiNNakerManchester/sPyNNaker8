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

import unittest
from spinnman.model import BMPConnectionData
from spalloc import Job
from spinnman.transceiver import create_transceiver_from_hostname
from spinnman.get_cores_in_run_state import main


class TestGetCoresInRunState(unittest.TestCase):

    def test_with_spalloc(self):
        n_boards = 2
        spalloc_machine = None
        spalloc_user = "integration tests"
        spalloc_server = "spinnaker.cs.man.ac.uk"
        job = Job(
            n_boards,
            hostname=spalloc_server, owner=spalloc_user,
            machine=spalloc_machine)
        job.wait_until_ready()

        job.set_power(True)
        job.wait_until_ready()
        txrx = create_transceiver_from_hostname(job.hostname, version=5)
        txrx.ensure_board_is_ready()

        # run GetCoresInRunState
        main(["-a", str(job.id), job.hostname])

        txrx.close()
        job.set_power(False)
        job.destroy()

    def test_with_bmp(self):
        bmp_connection_data = [BMPConnectionData(
            0, 0, "spinn-4c.cs.man.ac.uk", [0], None)]
        txrx = create_transceiver_from_hostname(
            "spinn-4.cs.man.ac.uk", 5,
            bmp_connection_data=bmp_connection_data)
        txrx.ensure_board_is_ready()

        # run GetCoresInRunState with host
        main(["spinn-4.cs.man.ac.uk"])

        # run GetCoresInRunState with cfg
        main([])
        txrx.close()


if __name__ == '__main__':
    unittest.main()
