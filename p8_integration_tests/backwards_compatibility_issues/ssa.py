import spynnaker8 as p
p.setup()
p.Population(10, p.SpikeSourceArray,
             {'spike_times': [100, 200]}, label='messed up')
