def check_neuron_data(spikes, v, exc, expected_spikes, simtime, label, index):
    # Small tolerance as max not spike on first inputs
    if len(spikes) < expected_spikes - 2:
        raise AssertionError(
            "Too few spikes for neuron {} in {}. Expected {} found {}".
            format(index, label, expected_spikes, len(spikes)))
    if len(spikes) > expected_spikes:
        raise AssertionError(
            "Too many spikes for neuron {} in {}. Expected {} found {}".
            format(index, label, expected_spikes, len(spikes)))
    iter_spikes = iter(spikes)
    next_spike = int(next(iter_spikes).magnitude)
    last_spike = -1
    for t in range(simtime):
        if t > next_spike:
            last_spike = next_spike
            try:
                next_spike = int(next(iter_spikes).magnitude)
            except (StopIteration):
                next_spike = simtime
        t_delta = t - last_spike
        if t_delta <= 2:
            if v[t].magnitude != -65:
                raise AssertionError(
                    "Incorrect V for neuron {} at time {} "
                    "(which is {} since last spike) in {}. "
                    "Found {} but expected 65".format(
                        index, t, t_delta, label, v[t].magnitude))
        else:
            target_v = v[t - 1].magnitude + exc[t - 1].magnitude
            if v[t] > target_v:
                raise AssertionError(
                    "Incorrect V for neuron {} at time {} "
                    "(which is {} since last spike) in {}. "
                    "Found {} but expected more than {}".format(
                        index, t, t_delta, label, v[t], target_v))
            if v[t] < target_v - 1:
                raise AssertionError(
                    "Incorrect V for neuron {} at time {} "
                    "(which is {} since last spike) in {}. "
                    "Found {} but expected more than than {}".format(
                        index, t, t_delta, label, v[t], target_v - 1))


def check_data(pop, expected_spikes, simtime):
    neo = pop.get_data("all")
    spikes = neo.segments[0].spiketrains
    v = neo.segments[0].filter(name="v")[0]
    gsyn_exc = neo.segments[0].filter(name="gsyn_exc")[0]
    for i in range(len(spikes)):
        check_neuron_data(spikes[i], v[:, i], gsyn_exc[:, i], expected_spikes,
                          simtime, pop.label, i)
