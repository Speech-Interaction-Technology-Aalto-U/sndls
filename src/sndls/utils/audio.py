import numpy as np
from typing import Optional
from scipy.signal import stft
from .config import get_default_eps
from .collections import flatten_nested_list


def amp_to_db(x: np.ndarray, eps: float = get_default_eps()) -> np.ndarray:
    """Returns the amplitude in decibels of every sample.
    
    Args:
        x (np.ndarray): Input audio data.
        eps (float): Machine epsilon.
    
    Returns:
        np.ndarray: Array containing values in decibel scale.
    """
    return 20.0 * np.log10(np.clip(x, a_min=eps, a_max=None))


def db_to_amp(x: np.ndarray, min: Optional[float] = None) -> np.ndarray:
    """Transforms decibel values to amplitude values.
    
    Args:
        x (np.ndarray): Array containing decibel values.
        min (Optional[float]): Minimum decibel value. Values below this
            threshold will be replaced by 0.0 to eliminate denormals.
    
    Returns:
        np.ndarray: Array containing amplitude values.
    """
    amp = 10.0 ** (x / 20.0)

    if min is not None:
        amp = np.where(amp <= min, 0.0, amp)
    
    return amp


def peak_amp(x: np.ndarray, axis: int = -1) -> np.ndarray:
    """Returns the peak amplitude of a `np.ndarray`.
    
    Args:
        x (np.ndarray): Input audio data.
        axis (int): Axis along which the peak amplitude is calculated.
    
    Returns:
        np.ndarray: Array containing peak amplitude values.
    """
    return np.amax(np.abs(x), axis=axis, keepdims=True)


def peak_db(
        x: np.ndarray,
        axis: int = -1,
        eps: float = get_default_eps()
) -> np.ndarray:
    """ Returns the peak amplitude of a `np.ndarray` in decibel scale.
    
    Args:
        x (np.ndarray): Input audio data.
        axis (int): Axis along which the peak amplitude is calculated.
        eps (float): Machine epsilon.
    
    Returns:
        np.ndarray: Array containing peak amplitude values in decibel scale.
    """
    return amp_to_db(peak_amp(x, axis=axis), eps=eps)


def rms(x: np.ndarray, axis: int = -1) -> np.ndarray:
    """Returns the root mean square level of a `np.ndarray`.
    
    Args:
        x (np.ndarray): Input audio data.
        axis (int): Axis along which the root mean square level is calculated.
    
    Returns:
        np.ndarray: Array containing the root mean square level.
    """
    return np.mean(x ** 2, axis=axis, keepdims=True) ** 0.5


def rms_db(x: np.ndarray, axis: int = -1) -> np.ndarray: 
    """ Returns the root mean square level of a `np.ndarray` in decibel scale.
    
    Args:
        x (np.ndarray): Input audio data.
        axis (int): Axis along which the root mean square level is calculated.
    
    Returns:
        np.ndarray: Array containing the root mean square level in decibels.
    """
    return amp_to_db(rms(x, axis=axis))


def is_clipped(x: np.ndarray, min: float = -1.0, max: float = 1.0) -> bool:
    """Returns `True` if a `np.ndarray` containing audio data has values
    above or below a certain range.

    Args:
        x (np.ndarray): Input audio data.
        min (float): Lower limit of the allowed range.
        max (float): Upper limit of the allowed range.
    
    Returns:
        bool: `True` if the file contains at least one value outside the given
            range.
    """
    result = np.logical_or(np.any(x > max), np.any(x < min))
    return bool(result)


def is_anomalous(x: np.ndarray) -> bool:
    """ Retruns `True`if a `np.ndarray` containing audio data has `inf`, `-inf`
    or `NaN` values.
    
    Args:
        x (np.ndarray): Input audio data.
    
    Returns:
        bool: `True` if the file contains at least one `inf`, `-inf` or `NaN`
            value.
    """
    result = np.logical_or(
        np.logical_or(np.isinf(x).any(), np.isneginf(x).any()),
        np.isnan(x).any()
    )
    return bool(result)

def is_silent(x: np.ndarray, thresh_db: float = -80.0, axis: int = -1) -> bool:
    """Returns `True` if a `np.ndarray` containing audio data is silent. That
    is, the root mean square level of the files in decibels is below a certain
    threshold.

    Args:
        x (np.ndarray): Input audio data.
        thresh_db (float): Minimum threshold below which a file is considered
            silent.
        axis (int): Axis along which the root mean square level in decibels is
            computed and contrasted again the given threshold in decibels.
    
    Returns:
        bool: `True` if `x` is silent, `False` otherwise.
    """
    db_rms = flatten_nested_list(rms_db(x, axis=axis).tolist())
    return all(chl_db_rms < thresh_db for chl_db_rms in db_rms)


def spectral_rolloff(
        x: np.ndarray,
        fs: int,
        fft_size: int,
        hop_size: Optional[int],
        window: str = "hann",
        rolloff: float = 0.9
) -> np.ndarray:
    """Calculates the spectral rolloff of an input array `x`. That is, the
    frequency bin under which `rolloff` percent of the energy is
    accumulated.

    Args:
        x (np.ndarray): Input audio data.
        fs (int): Sample rate.
        fft_size (int): Size of the FFT.
        hop_size (Optional[int]): Hop size of the FFT.
        window (str): Window type.
        rolloff (float): Rolloff percent between 0.0 and 1.0. Rolloff of
            0.9 means that the resulting rolloff for a given frequency is
            the value under which 90 percent of the energy is accumulated.
    
    Returns:
        np.ndarray: Array containing framewise roll-off.
    """
    if rolloff < 0.0 or rolloff > 1.0:
        raise ValueError("rolloff must be between 0.0 and 1.0")
    
    # Compute magnitude
    fc, _, x_stft = stft(
        x,
        fs=fs,
        nperseg=fft_size,
        nfft=fft_size,
        noverlap=hop_size,
        window=window,
        return_onesided=True,
        padded=False,
        scaling="spectrum"
    )
    x_mag = np.abs(x_stft)
    fc = np.expand_dims(fc, axis=(0, -1))
    fc = np.broadcast_to(fc, x_mag.shape)

    # Get cumulative sum and obtain rolloff threshold per frame
    x_mag_cumsum = np.cumsum(x_mag, axis=-2)
    rolloff_threshold = rolloff * x_mag_cumsum[..., -1, :]

    # Mask all values below threshold as inf
    rolloff_idx = np.where(x_mag_cumsum < rolloff_threshold, np.inf, 1.0)

    with np.errstate(invalid="ignore"):
        rolloff_freq = fc * rolloff_idx
    
    rolloff_freq[np.isnan(rolloff_freq)] = np.inf
    rolloff_freq = np.min(rolloff_freq, axis=-2, keepdims=True)

    return rolloff_freq
