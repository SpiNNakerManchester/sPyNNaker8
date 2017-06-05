from spinn_utilities.progress_bar import ProgressBar
from spynnaker.pyNN.models.common import AbstractGSynExcitatoryRecordable, \
    AbstractSpikeRecordable, AbstractGSynInhibitoryRecordable, \
    AbstractVRecordable


class SPYNNaker8NeoRecordingExtractor(object):

    def __call__(self, populations, read_buffer_token=None):

        if read_buffer_token is not None:

            progress_bar = ProgressBar(
                total_number_of_things_to_do=len(populations) * 4,
                string_describing_what_being_progressed=(
                    "extracting recorded data for Neo.")
            )

            # extract recordings for neo storage
            for pop in populations:
                if isinstance(pop._vertex, AbstractGSynExcitatoryRecordable):
                    if pop._vertex.is_recording_gsyn_excitatory():
                        pop._extract_data(
                            variables="gsyn_exc", clear=False,
                            annotations=None)
                progress_bar.update()
                if isinstance(pop._vertex, AbstractSpikeRecordable):
                    if pop._vertex.is_recording_spikes():
                        pop._extract_data(
                            variables="spikes", clear=False,
                            annotations=None)
                progress_bar.update()
                if isinstance(pop._vertex, AbstractGSynInhibitoryRecordable):
                    if pop._vertex.is_recording_gsyn_inhibitory():
                        pop._extract_data(
                            variables="gsyn_inh", clear=False,
                            annotations=None)
                progress_bar.update()
                if isinstance(pop._vertex, AbstractVRecordable):
                    if pop._vertex.is_recording_v():
                        pop._extract_data(
                            variables="v", clear=False, annotations=None)
                progress_bar.update()

                pop.reset_neo_recorded_trackers()
            progress_bar.end()
