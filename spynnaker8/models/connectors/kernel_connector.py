from spynnaker.pyNN.models.neural_projections.connectors import (
    KernelConnector as
    CommonKernelConnector)


class KernelConnector(CommonKernelConnector):
    """
    Where the pre- and post-synaptic populations are considered as a 2D array.
    Connect every post(row, col) neuron to many pre(row, col, kernel) through
    a (kernel) set of weights and/or delays.

    TODO: should these include allow_self_connections and with_replacement?

    :param shape_pre:\
        2D shape of the pre population (rows/height, cols/width, usually \
        the input image shape)
    :param shape_post:\
        2D shape of the post population (rows/height, cols/width)
    :param shape_kernel:\
        2D shape of the kernel (rows/height, cols/width)
    :param weight_kernel (optional):\
        2D matrix of size shape_kernel describing the weights
    :param delay_kernel (optional):\
        2D matrix of size shape_kernel describing the delays
    :param shape_common (optional):\
        2D shape of common coordinate system (for both pre and post, \
        usually the input image sizes)
    :param pre/post_sample_steps (optional):\
        Sampling steps/jumps for pre/post pop <=> (startX, endX, _stepX_)
        None or 2-item array
    :param pre/post_start_coords (optional):\
        Starting row/col for pre/post sampling <=> (_startX_, endX, stepX)
        None or 2-item array
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
