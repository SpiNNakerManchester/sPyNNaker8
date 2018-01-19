from spynnaker.pyNN.models.neural_projections.connectors \
    import MultapseConnector as CommonMultapseConnector


class MultapseConnector(CommonMultapseConnector):
    """
    Create a multapse connector. The size of the source and destination\
    populations are obtained when the projection is connected. The number of\
    synapses is specified. when instantiated, the required number of synapses\
    is created by selecting at random from the source and target populations\
    with replacement. Uniform selection probability is assumed.

    :param num_synapses:
        The total number of synapses in the connection.
    :type num_synapses: int
    """
    def __init__(self, num_synapses, weights=0.0, delays=1, safe=True,
                 verbose=False):
        # pylint: disable=too-many-arguments
        super(MultapseConnector, self).__init__(
            num_synapses=num_synapses, safe=safe, verbose=verbose)
        self.set_weights_and_delays(weights, delays)
