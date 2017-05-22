from spynnaker.pyNN.utilities.failed_state import FailedState as \
    CommonFailedState


class FailedState(CommonFailedState):

    def __init__(self):
        CommonFailedState.__init__(self)

    @property
    def name(self):
        return "sPyNNaker8"
