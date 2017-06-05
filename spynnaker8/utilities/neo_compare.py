import quantities

def compare_spiketrain(spiketrain1, spiketrain2):
    id1 = spiketrain1.annotations['source_index']
    id2 = spiketrain2.annotations['source_index']
    if id1 != id2:
        msg = "Different annotations['source_index'] found {} and {}" \
              "".format(id1, id2)
        raise AssertionError(msg)
    if len(spiketrain1) != len(spiketrain2):
        msg = "spiketrains1 has {} spikes while spiketrains2 as {} for " \
              "id {}".format(len(spiketrain1), len(spiketrain2), id1)
        raise AssertionError(msg)
    for spike1, spike2 in zip(spiketrain1, spiketrain2):
        if spike1 != spike2:
            print id1, spiketrain1, spiketrain2
            msg = "spike1 is {} while spike2 is {} for " \
                  "id {}".format(spike1, spike2, id1)
            raise AssertionError(msg)


def compare_spiketrains(spiketrains1, spiketrains2):
    if len(spiketrains1) != len(spiketrains2):
        msg = "spiketrains1 has {} spiketrains while spiketrains2 as {} " \
              "analogsignalarrays".format(len(spiketrains1),
                                          len(spiketrains2))
        raise AssertionError(msg)
    for spiketrain1, spiketrain2 in zip(spiketrains1, spiketrains2):
        compare_spiketrain(spiketrain1, spiketrain2)


def compare_analogsignalarray(asa1, asa2):
    if asa1.name != asa2.name:
        msg = "analogsignalarray1 has name {} while analogsignalarray1 has " \
              "{} ".format(asa1.name, asa2.name)
        raise AssertionError(msg)
    if len(asa1.channel_index) != len(asa2.channel_index):
        msg = "channel_index 1 has len {} while channel_index 2 has {} " \
              "for {}".format(len(asa1.channel_index),
                              len(asa2.channel_index), asa1.name)
        raise AssertionError(msg)
    for channel1, channel2 in zip(asa1.channel_index, asa2.channel_index):
        if channel1 != channel2:
            msg = "channel 1 is  while channel 2 is {} " \
                  "for {}".format(channel1, channel2, asa1.name)
            raise AssertionError(msg)
    if len(asa1.times) != len(asa2.times):
        msg = "times 1 has len {} while times 2 has {} " \
              "for {}".format(len(asa1.times),
                              len(asa2.times), asa1.name)
        raise AssertionError(msg)
    for time1, time2 in zip(asa1.times, asa2.times):
        if time1 != time2:
            msg = "time 1 is  while time 2 is {} " \
                  "for {}".format(time1, time2, asa1.name)
            raise AssertionError(msg)
    if len(asa1) != len(asa2):
        msg = "analogsignalarray 1 has len {} while analogsignalarray 2 has " \
              "{} for {}".format(len(asa1), len(asa2), asa1.name)
        raise AssertionError(msg)
    for signal1, signal2 in zip(asa1, asa2):
        # print signal1, signal2
        if len(signal1) != len(signal2):
            msg = "signal 1 has len {} while signal 2 has " \
                  "{} for {}".format(len(signal1), len(signal2), asa1.name)
            raise AssertionError(msg)
        for value1, value2 in zip(signal1, signal2):
            if value1 != value2:
                msg = "value 1 is  while value2 is {} " \
                      "for {}".format(value1, value2, asa1.name)
                raise AssertionError(msg)


def compare_segments(seg1, seg2):
    compare_spiketrains(seg1.spiketrains, seg2.spiketrains)
    if len(seg1.analogsignalarrays) != len(seg2.analogsignalarrays):
        msg = "Segment1 has {} analogsignalarrays while Segment2 as {} " \
              "analogsignalarrays".format(len(seg1.analogsignalarrays),
                                          len(seg1.analogsignalarrays))
        raise AssertionError(msg)
    for analogsignalarray1 in seg1.analogsignalarrays:
        name = analogsignalarray1.name
        analogsignalarray2 = seg2.filter(name=name)[0]
        compare_analogsignalarray(analogsignalarray1, analogsignalarray2)


def compare_blocks(neo1, neo2):
    if len(neo1.segments) != len(neo2.segments):
        msg = "Block1 has {} segments while block2 as {} segments" \
              "".format(len(neo1.segments), len(neo2.segments))
        raise AssertionError(msg)
    for seg1, seg2 in zip(neo1.segments, neo2.segments):
        compare_segments(seg1, seg2)
