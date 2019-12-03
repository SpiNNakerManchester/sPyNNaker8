# Copyright (c) 2017-2019 The University of Manchester
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from spynnaker.pyNN.models.neural_projections.connectors import (
    KernelConnector as
    CommonKernelConnector)


class KernelConnector(CommonKernelConnector):
    """
    Where the pre- and post-synaptic populations are considered as a 2D array.\
    Connect every post(row, col) neuron to many pre(row, col, kernel) through\
    a (kernel) set of weights and/or delays.

    .. todo::
        TODO: should these include `allow_self_connections` and \
        `with_replacement`?
    """
    __slots__ = []

    def __init__(
            self, shape_pre, shape_post, shape_kernel, weight_kernel=None,
            delay_kernel=None, shape_common=None, pre_sample_steps=None,
            pre_start_coords=None, post_sample_steps=None,
            post_start_coords=None, safe=True, space=None, verbose=False):
        r"""
        :param shape_pre:
            2D shape of the pre population (rows/height, cols/width, usually
            the input image shape)
        :type shape_pre: list(int) or tuple(int,int)
        :param shape_post:
            2D shape of the post population (rows/height, cols/width)
        :type shape_post: list(int) or tuple(int,int)
        :param shape_kernel:
            2D shape of the kernel (rows/height, cols/width)
        :type shape_kernel: list(int) or tuple(int,int)
        :param weight_kernel: (optional)
            2D matrix of size shape_kernel describing the weights
        :type weight_kernel: ~numpy.ndarray or ~pyNN.random.NumpyRNG
            or int or float or list(int) or list(float) or None
        :param delay_kernel: (optional)
            2D matrix of size shape_kernel describing the delays
        :type delay_kernel: ~numpy.ndarray or ~pyNN.random.NumpyRNG
            or int or float or list(int) or list(float) or None
        :param shape_common: (optional)
            2D shape of common coordinate system (for both pre and post,
            usually the input image sizes)
        :type shape_common: list(int) or tuple(int,int) or None
        :param pre_sample_steps: (optional)
            Sampling steps/jumps for pre pop :math:`\Leftrightarrow`
            :math:`((\mathsf{start}_x, \mathsf{end}_x, \mathsf{step}_x),
            (\mathsf{start}_y, \mathsf{end}_y, \mathsf{step}_y))`
        :type pre_sample_steps: None or list(tuple(int,int,int))
        :param pre_start_coords: (optional)
            Starting row/col for pre sampling :math:`\Leftrightarrow`
            :math:`((\mathsf{start}_x, \mathsf{end}_x, \mathsf{step}_x),
            (\mathsf{start}_y, \mathsf{end}_y, \mathsf{step}_y))`
        :type pre_start_coords: None or list(tuple(int,int,int))
        :param post_sample_steps: (optional)
            Sampling steps/jumps for post pop :math:`\Leftrightarrow`
            :math:`((\mathsf{start}_x, \mathsf{end}_x, \mathsf{step}_x),
            (\mathsf{start}_y, \mathsf{end}_y, \mathsf{step}_y))`
        :type post_sample_steps: None or list(tuple(int,int,int))
        :param post_start_coords: (optional)
            Starting row/col for post sampling :math:`\Leftrightarrow`
            :math:`((\mathsf{start}_x, \mathsf{end}_x, \mathsf{step}_x),
            (\mathsf{start}_y, \mathsf{end}_y, \mathsf{step}_y))`
        :type post_start_coords: None or list(tuple(int,int,int))
        """
        # pylint: disable=too-many-arguments
        super(KernelConnector, self).__init__(
            shape_pre, shape_post, shape_kernel, weight_kernel,
            delay_kernel, shape_common, pre_sample_steps, pre_start_coords,
            post_sample_steps, post_start_coords, safe, space, verbose)
