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
    def __init__(self, num_synapses, allow_self_connections=True,
                 with_replacement=True, safe=True, verbose=False):
        CommonMultapseConnector.__init__(
            self, num_synapses=num_synapses,
            allow_self_connections=allow_self_connections,
            with_replacement=with_replacement, safe=safe, verbose=verbose)

    def get_rng_next(self, num_synapses, prob_connect):
        # This needs to be edited to work with PyNN 0.8+
        # equivalent PyNN 0.7 call with the allowed "multinomial"
        # returns an array, this with "binomial" only returns a single value...

        # loop over prob connect and do a binomial for each for now
        n_prob = len(prob_connect)
        rngs = [
            self._rng.next(1, distribution="binomial",
                           parameters={'n': num_synapses,
                                       'p': prob_connect[i]})[0]
            for i in range(n_prob)]
        return rngs
