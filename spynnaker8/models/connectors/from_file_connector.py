from spynnaker.pyNN.models.neural_projections.connectors \
    import FromFileConnector as CommonFromFileConnector

from pyNN.connectors import FromFileConnector as PyNNFromFileConnector
from pyNN.recording import files


class FromFileConnector(CommonFromFileConnector, PyNNFromFileConnector):
    # pylint: disable=redefined-builtin
    def __init__(
            self, file, callback=None,  # @ReservedAssignment
            distributed=False, safe=True, verbose=False):
        # pylint: disable=too-many-arguments
        CommonFromFileConnector.__init__(
            self, file=file, distributed=distributed, safe=safe,
            verbose=verbose)
        PyNNFromFileConnector.__init__(
            self, file=file, distributed=distributed, safe=safe,
            callback=callback)

    def get_reader(self, file):  # @ReservedAssignment
        """ Get a file reader object using the PyNN methods.

        :return: A pynn StandardTextFile or similar
        """
        return files.StandardTextFile(file, mode="r")
