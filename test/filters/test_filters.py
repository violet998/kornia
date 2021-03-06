import pytest
import torch
from torch.autograd import gradcheck
from torch.testing import assert_allclose
from common import device_type

import kornia.filters as filters
import utils


@pytest.mark.parametrize("window_size", [5, 11])
@pytest.mark.parametrize("sigma", [1.5, 5.0])
def test_get_gaussian_kernel(window_size, sigma):
    kernel = filters.get_gaussian_kernel(window_size, sigma)
    assert kernel.shape == (window_size,)
    assert kernel.sum().item() == pytest.approx(1.0)


@pytest.mark.parametrize("ksize_x", [5, 11])
@pytest.mark.parametrize("ksize_y", [3, 7])
@pytest.mark.parametrize("sigma", [1.5, 2.1])
def test_get_gaussian_kernel2d(ksize_x, ksize_y, sigma):
    kernel = filters.get_gaussian_kernel2d(
        (ksize_x, ksize_y), (sigma, sigma))
    assert kernel.shape == (ksize_x, ksize_y)
    assert kernel.sum().item() == pytest.approx(1.0)


class TestGaussianBlur:
    @pytest.mark.parametrize("batch_shape",
                             [(1, 4, 8, 15), (2, 3, 11, 7)])
    def test_gaussian_blur(self, batch_shape, device_type):
        kernel_size = (5, 7)
        sigma = (1.5, 2.1)

        input = torch.rand(batch_shape).to(torch.device(device_type))
        gauss = filters.GaussianBlur(kernel_size, sigma)
        assert gauss(input).shape == batch_shape

    def test_gradcheck(self):
        # test parameters
        batch_shape = (2, 3, 11, 7)
        kernel_size = (5, 3)
        sigma = (1.5, 2.1)

        # evaluate function gradient
        input = torch.rand(batch_shape)
        input = utils.tensor_to_gradcheck_var(input)  # to var
        assert gradcheck(filters.gaussian_blur, (input, kernel_size, sigma,),
                         raise_exception=True)

    def test_jit(self):
        @torch.jit.script
        def op_script(img):

            return filters.gaussian_blur(img, (5, 5), (1.2, 1.2))

        batch_size, channels, height, width = 2, 3, 64, 64
        img = torch.ones(batch_size, channels, height, width)
        expected = filters.GaussianBlur((5, 5), (1.2, 1.2))(img)
        actual = op_script(img)
        assert_allclose(actual, expected)


@pytest.mark.parametrize("window_size", [5])
def test_get_laplacian_kernel(window_size):
    kernel = filters.get_laplacian_kernel(window_size)
    assert kernel.shape == (window_size,)
    assert kernel.sum().item() == pytest.approx(0.0)


@pytest.mark.parametrize("window_size", [7])
def test_get_laplacian_kernel2d(window_size):
    kernel = filters.get_laplacian_kernel2d(window_size)
    assert kernel.shape == (window_size, window_size)
    assert kernel.sum().item() == pytest.approx(0.0)
    expected = torch.tensor([[1., 1., 1., 1., 1., 1., 1.],
                             [1., 1., 1., 1., 1., 1., 1.],
                             [1., 1., 1., 1., 1., 1., 1.],
                             [1., 1., 1., -48., 1., 1., 1.],
                             [1., 1., 1., 1., 1., 1., 1.],
                             [1., 1., 1., 1., 1., 1., 1.],
                             [1., 1., 1., 1., 1., 1., 1.]])
    assert_allclose(expected, kernel)


class TestLaplacian:
    @pytest.mark.parametrize("batch_shape",
                             [(1, 4, 8, 15), (2, 3, 11, 7)])
    def test_laplacian(self, batch_shape, device_type):
        kernel_size = 5

        input = torch.rand(batch_shape).to(torch.device(device_type))
        laplace = filters.Laplacian(kernel_size)
        assert laplace(input).shape == batch_shape

    def test_gradcheck(self):
        # test parameters
        batch_shape = (2, 3, 11, 7)
        kernel_size = 9

        # evaluate function gradient
        input = torch.rand(batch_shape)
        input = utils.tensor_to_gradcheck_var(input)
        assert gradcheck(filters.laplacian, (input, kernel_size,),
                         raise_exception=True)
