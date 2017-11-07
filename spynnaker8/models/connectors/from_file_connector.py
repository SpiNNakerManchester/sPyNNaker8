from spynnaker.pyNN.models.neural_projections.connectors \
    import FromFileConnector as CommonFromFileConnector

from pyNN.connectors import FromFileConnector as PyNNFromFileConnector
from pyNN.recording import files


class FromFileConnector(CommonFromFileConnector, PyNNFromFileConnector):
    def __init__(
            self, file, callback=None,  # @ReservedAssignment
            distributed=False, safe=True, verbose=False):
        CommonFromFileConnector.__init__(
            self, file=None, distributed=distributed, safe=safe,
            verbose=verbose)
        PyNNFromFileConnector.__init__(
            self, file=file, distributed=distributed, safe=safe,
            callback=callback)

    def get_reader(self, file):
        """
        get a filereader object using the pynn methods

        :return: A pynn StandardTextFile or similar
        """
        return files.StandardTextFile(file, mode="r")
