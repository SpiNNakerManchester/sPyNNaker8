import spynnaker8 as p
import spynnaker8_external_devices_plugin.pyNN as e
from spynnaker8_external_devices_plugin.pyNN import PushBotRetinaViewer

p.setup(1.0)

# Set up the PushBot devices
pushbot_protocol = e.MunichIoSpiNNakerLinkProtocol(
    mode=e.MunichIoSpiNNakerLinkProtocol.MODES.PUSH_BOT, uart_id=0)
spinnaker_link = 0
board_address = None
motor_0 = e.PushBotSpiNNakerLinkMotorDevice(
    e.PushBotMotor.MOTOR_0_PERMANENT, pushbot_protocol,
    spinnaker_link, board_address=board_address)
motor_1 = e.PushBotSpiNNakerLinkMotorDevice(
    e.PushBotMotor.MOTOR_1_PERMANENT, pushbot_protocol,
    spinnaker_link, board_address=board_address)
speaker = e.PushBotSpiNNakerLinkSpeakerDevice(
    e.PushBotSpeaker.SPEAKER_TONE, pushbot_protocol,
    spinnaker_link, board_address=board_address)
laser = e.PushBotSpiNNakerLinkLaserDevice(
    e.PushBotLaser.LASER_ACTIVE_TIME, pushbot_protocol,
    spinnaker_link, board_address=board_address, start_total_period=1000)
led_front = e.PushBotSpiNNakerLinkLEDDevice(
    e.PushBotLED.LED_FRONT_ACTIVE_TIME, pushbot_protocol,
    spinnaker_link, board_address=board_address,
    start_total_period=1000)
led_back = e.PushBotSpiNNakerLinkLEDDevice(
    e.PushBotLED.LED_BACK_ACTIVE_TIME, pushbot_protocol,
    spinnaker_link, board_address=board_address,
    start_total_period=1000)

weights = {
    motor_0: 10.0,
    motor_1: 10.0,
    speaker: 100.0,
    laser: 100.0,
    led_front: 100.0,
    led_back: 100.0,
}

devices = [motor_0, motor_1, speaker, laser, led_front, led_back]

# Set up the PushBot control
pushbot = p.Population(
    len(devices), e.PushBotLifSpinnakerLink(
        protocol=pushbot_protocol,
        devices=devices,
        tau_syn_E=500.0),
    label="PushBot"
)

# Send in some spikes
stimulation = p.Population(
    len(devices), p.SpikeSourceArray(
        spike_times=[[i * 1000] for i in range(len(devices))]),
    label="input"
)

connections = [
    (i, i, weights[device], 1) for i, device in enumerate(devices)
]
p.Projection(stimulation, pushbot, p.FromListConnector(connections))

retina_resolution = e.PushBotRetinaResolution.DOWNSAMPLE_64_X_64
pushbot_retina = p.Population(
    retina_resolution.value.n_neurons,
    e.PushBotSpiNNakerLinkRetinaDevice(
        spinnaker_link_id=spinnaker_link,
        board_address=board_address,
        protocol=pushbot_protocol,
        resolution=retina_resolution))

viewer = PushBotRetinaViewer(
    retina_resolution.value, port=17895)
e.activate_live_output_for(pushbot_retina, port=viewer.local_port,
                           notify=False)

viewer.start()
p.run(len(devices) * 1000)
p.end()
