from spynnaker.pyNN.models.neural_projections.connectors \
    import MultapseConnector as CommonMultapseConnector


class MultapseConnector(CommonMultapseConnector):
    """
    Create a multapse connector. The size of the source and destination
    populations are obtained when the projection is connected. The number of
    synapses is specified. when instantiated, the required number of synapses
    is created by selecting at random from the source and target populations
    with replacement. Uniform selection probability is assumed.

    :param num_synapses:
        Integer. This is the total number of synapses in the connection.

    """
    def __init__(self, num_synapses, weights=0.0, delays=1, safe=True,
                 verbose=False):
        CommonMultapseConnector.__init__(
            self, num_synapses=num_synapses, safe=safe, verbose=verbose)
        self.set_weights_and_delays(weights, delays)

    def get_rng_next(self, num_synapses, prob_connect):
        # This needs to be edited to work with PyNN 0.8+
        # equivalent PyNN 0.7 call with the allowed "multinomial"
        # returns an array, this with "binomial" only returns a single value...
        return self._rng.next(1, distribution="binomial",
                              parameters={'n': num_synapses,
                                          'p': prob_connect[0]})
