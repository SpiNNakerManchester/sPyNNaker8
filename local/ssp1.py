import spynnaker8 as p

pre_rate = 500
dt=2

p.setup(1)
simtime = 20

pop_src = p.Population(1, p.SpikeSourcePoisson(rate=pre_rate), label="src")
pop_src.record('spikes')

for i in range(simtime//dt):
    print(i)
    p.run(dt)

pre_spikes = pop_src.spinnaker_get_data("spikes")
print(pre_spikes)
p.end()
print("\n job done")