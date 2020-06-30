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

from pyNN import common as PyNNCommon


class ID(int, PyNNCommon.IDMixin):
    """ A filter container for allowing random setters of values
    """

    def __init__(self, n):
        """ Create an ID object with numerical value ``n``.

        :param int n: The value of the object.
        """
        int.__init__(n)
        PyNNCommon.IDMixin.__init__(self)
