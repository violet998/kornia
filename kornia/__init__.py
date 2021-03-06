# Make sure that kornia is running on Python 3.6.0 or later
# (to avoid running into this bug: https://bugs.python.org/issue29246)
import sys
if sys.version_info < (3, 6, 0):
    raise RuntimeError("Kornia requires Python 3.6.0 or later")

from .version import __version__

from kornia import color
from kornia import contrib
from kornia import feature
from kornia import filters
from kornia import geometry
from kornia import losses
from kornia import utils

# Exposes package functional to top level

from kornia.color import (
    rgb_to_grayscale,
    bgr_to_rgb,
    rgb_to_bgr,
    rgb_to_hsv,
    hsv_to_rgb,
    normalize,
)
from kornia.contrib import (
    spatial_soft_argmax2d,
    extract_tensor_patches,
    max_blur_pool2d,
)
from kornia.feature import (
    non_maxima_suppression2d,
    corner_harris,
)
from kornia.filters import (
    get_gaussian_kernel,
    get_gaussian_kernel2d,
    get_laplacian_kernel,
    get_laplacian_kernel2d,
    gaussian_blur,
    laplacian,
    sobel,
    spatial_gradient,
    box_blur,
    median_blur,
)
from kornia.losses import (
    ssim,
    dice_loss,
    tversky_loss,
    inverse_depth_smoothness_loss,
)
from kornia.utils import (
    one_hot,
    create_meshgrid,
    tensor_to_image,
    image_to_tensor,
)
from kornia.geometry import *
