import spynnaker8 as p

def print_spikes(trains):
    nseg = len(trains.segments)
    for i in range(nseg):
        trains1 = trains.segments[i].spiketrains
        ntr = len(trains1)
        print "segment ", i

        for j in range(ntr):
            print "train ", j, " ", trains1[j]


to_plot_wgts = False

p.setup(1)

simtime = 1000

pop_src2 = p.Population(10, p.SpikeSourcePoisson(rate=100), label="drive")
pop_ex = p.Population(10, p.IF_curr_exp(), label="test")

proj2 = p.Projection(pop_src2,  pop_ex,  p.OneToOneConnector(),
               synapse_type=p.StaticSynapse(weight=2.0),  receptor_type='excitatory')

pop_src2.record(['spikes'])
pop_ex.record(['spikes'])
nseg = 0

rates = [100]*10
# for i in range(inp_nrn/20):
#     rates[i]=50
pop_src2.set(rate=rates)


#pop_src2.set(rate=100)
p.run(simtime)
print "run 1, input spikes"
print_spikes(pop_src2.get_data('spikes'))
print "run 1, output spikes"
print_spikes(pop_ex.get_data('spikes'))
#p.reset()
#pop_src2.set(rate=50)
pop_src2.set(rate=rates)
p.run(simtime)
print "run 2, input spikes"
print_spikes(pop_src2.get_data('spikes'))
print "run 2, output spikes"
print_spikes(pop_ex.get_data('spikes'))
#p.reset()
#pop_src2.set(rate=120)
p.run(simtime)
print "run 3, input spikes"
print_spikes(pop_src2.get_data('spikes'))
print "run 3, output spikes"
print_spikes(pop_ex.get_data('spikes'))
#p.reset()

p.end()
print "\n job done"