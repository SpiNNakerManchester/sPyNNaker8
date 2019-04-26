from spynnaker.pyNN.models.neural_projections.connectors import (
    KernelConnector as
    CommonKernelConnector)


class KernelConnector(CommonKernelConnector):
    """
    Create a kernel connector

    :param  descriptions to follow, see sPyNNaker class
    """
    __slots__ = []

    def __init__(
            self, shape_pre, shape_post, shape_kernel, weight_kernel=None,
            delay_kernel=None, shape_common=None, pre_sample_steps=None,
            pre_start_coords=None, post_sample_steps=None,
            post_start_coords=None, safe=True, space=None, verbose=False):
        # pylint: disable=too-many-arguments
        super(KernelConnector, self).__init__(
            shape_pre, shape_post, shape_kernel, weight_kernel,
            delay_kernel, shape_common, pre_sample_steps, pre_start_coords,
            post_sample_steps, post_start_coords, safe, space, verbose)
