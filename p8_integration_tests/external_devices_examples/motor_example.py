"""
motor example that just feeds data to the motor pop which starts the motor
going forward
"""

try:
    import pyNN.spiNNaker as p
except Exception as e:
    import spynnaker8 as p
import spynnaker8_external_devices_plugin.pyNN as q

# set up the tools
p.setup(timestep=1.0, min_delay=1.0, max_delay=32.0)

# set up the virtual chip coordinates for the motor
connected_chip_coords = {'x': 0, 'y': 0}
link = 4

populations = list()
projections = list()


input_population = p.Population(6, p.SpikeSourcePoisson(rate=10))
control_population = p.Population(6, p.IF_curr_exp())
motor_device = p.Population(
    6, q.MunichMotorDevice(spinnaker_link_id=0))

p.Projection(
    input_population, control_population, p.OneToOneConnector(),
    synapse_type=p.StaticSynapse(weight=5.0))

q.activate_live_output_to(control_population, motor_device)

p.run(1000)
p.end()
