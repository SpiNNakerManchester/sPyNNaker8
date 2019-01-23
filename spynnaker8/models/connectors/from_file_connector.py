from spinn_utilities.abstract_base import AbstractBase, abstractmethod
from .from_list_connector import FromListConnector
import os
import numpy
from six import add_metaclass, string_types

from pyNN.connectors import FromFileConnector as PyNNFromFileConnector
from pyNN.recording import files


class FromFileConnector(FromListConnector, PyNNFromFileConnector):
    # pylint: disable=redefined-builtin
    __slots__ = ["_file"]

    def __init__(
            self, file,  # @ReservedAssignment
            distributed=False, safe=True, callback=None, verbose=False):
        self._file = file
        if isinstance(file, string_types):
            real_file = self.get_reader(file)
            try:
                conn_list = self._read_conn_list(real_file, distributed)
            finally:
                real_file.close()
        else:
            conn_list = self._read_conn_list(file, distributed)

        column_names = self.get_reader(self._file).get_metadata().get(
            'columns')

        # pylint: disable=too-many-arguments
        FromListConnector.__init__(
            self, conn_list, safe=safe, verbose=verbose,
            column_names=column_names, callback=callback)
        PyNNFromFileConnector.__init__(
            self, file=file, distributed=distributed, safe=safe,
            callback=callback)

    def _read_conn_list(self, the_file, distributed):
        if not distributed:
            return the_file.read()
        filename = "{}.".format(os.path.basename(the_file.file))

        conns = list()
        for found_file in os.listdir(os.path.dirname(the_file.file)):
            if found_file.startswith(filename):
                file_reader = self.get_reader(found_file)
                try:
                    conns.append(file_reader.read())
                finally:
                    file_reader.close()
        return numpy.concatenate(conns)

    def __repr__(self):
        return "FromFileConnector({})".format(self._file)

    def get_reader(self, file):  # @ReservedAssignment
        """ Get a file reader object using the PyNN methods.

        :return: A pynn StandardTextFile or similar
        """
        return files.StandardTextFile(file, mode="r")
