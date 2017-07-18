"""
retina example that just feeds data from a retina to live output via an
intermediate population
"""
try:
    import pyNN.spiNNaker as p
except Exception as e:
    import spynnaker8 as p
import spynnaker8_external_devices_plugin.pyNN as q

import retina_lib as retina_lib

connected_chip_details = {
    "spinnaker_link_id": 0,
}


def get_updated_params(params):
    params.update(connected_chip_details)
    return params


# Setup
p.setup(timestep=1.0)

# # Munich Right Retina - Down Polarity
# retina_pop = p.Population(
#     None, q.MunichRetinaDevice, get_updated_params({
#         'retina_key': 0x5,
#         'polarity': q.MunichRetinaDevice.DOWN_POLARITY,
#         'position': q.MunichRetinaDevice.RIGHT_RETINA}),
#     label='External retina')

# # Munich Right Retina - Up Polarity
# retina_pop = p.Population(
#     None, q.MunichRetinaDevice, get_updated_params({
#         'retina_key': 0x5,
#         'polarity': q.MunichRetinaDevice.UP_POLARITY,
#         'position': q.MunichRetinaDevice.RIGHT_RETINA}),
#     label='External retina')

# # Munich Left Retina - Merged Polarity
# retina_pop = p.Population(
#     None, q.MunichRetinaDevice, get_updated_params({
#         'retina_key': 0x5,
#         'polarity': q.MunichRetinaDevice.MERGED_POLARITY,
#         'position': q.MunichRetinaDevice.LEFT_RETINA}),
#     label='External retina')

# # FPGA Retina - Merged Polarity
# retina_pop = p.Population(
#     None, q.ExternalFPGARetinaDevice, get_updated_params({
#         'retina_key': 0x5,
#         'mode': q.ExternalFPGARetinaDevice.MODE_128,
#         'polarity': q.ExternalFPGARetinaDevice.MERGED_POLARITY}),
#     label='External retina')

# # FPGA Retina - Up Polarity
# retina_pop = p.Population(
#     None, q.ExternalFPGARetinaDevice, get_updated_params({
#         'retina_key': 0x5,
#         'mode': q.ExternalFPGARetinaDevice.MODE_128,
#         'polarity': q.ExternalFPGARetinaDevice.UP_POLARITY}),
#     label='External retina')

# FPGA Retina - Down Polarity
retina = q.ExternalFPGARetinaDevice(**get_updated_params({
    'retina_key': 0x5,
    'mode': q.ExternalFPGARetinaDevice.MODE_128,
    'polarity': q.ExternalFPGARetinaDevice.DOWN_POLARITY}))

retina_pop = p.Population(
    retina.get_n_neurons(), retina, label='External retina')

population = p.Population(1024, p.IF_curr_exp(), label='pop_1')
p.Projection(retina_pop, population,
             p.FromListConnector(retina_lib.subSamplerConnector2D(
                 128, 32, 2.0, 1)))

# q.activate_live_output_for(population)
p.run(1000)
p.end()
