import os
import numpy as np
import soundfile as sf
from glob import (
    escape,
    glob
)
from typing import (
    Callable,
    List,
    Optional,
    Tuple,
    Union
)
from .config import get_default_audio_io_dtype
from .exceptions import FolderNotFoundError
from .guards import is_file_or_error
from .collections import make_list
from .fmt import (
    _decorate_str,
    exit_error,
    exit_warning,
    print_error
)


def get_dir_files(
        dir: Union[str, List[str]],
        ext: Union[str, List[str]] = ".wav",
        recursive: bool = True,
        key: Optional[Callable] = None,
) -> List[str]:
    """Returns a `list` with all the files inside folder with extension `ext`.
    It supports a recursive search and searching in more than one root folder
    at a time if `recursive=True` and `dir` is a `list` of `str`,
    respectively.

    Args:
        dir (Union[str, List[str]]): Folder(s) to be searched.
        ext (Union[str, List[str]]): File extensions to be considered. Accepts
            `.*` as a wild card. Extensions are matched case-insensitively.
        recursive (bool): If `True`, the search inside each folder will be
            recursive.
        key (Optional[Callable]): Key function to sort the results. If it is
            not provided, files will be sorted alphabetically.

    Returns:
        `list` of `str` with the path to each retrieved file.

    Raises:
        FolderNotFoundError: If one of the folder(s) cannot be found.
    """
    dir = make_list(dir)
    ext = make_list(ext)

    # Check dirs exist before fetching content
    for dir_ in dir:
        if not os.path.isdir(dir_):
            raise FolderNotFoundError(f"Folder not found: '{dir_}'")

    all_files = []

    # Search dirs
    # NOTE: Folder names are escaped to support names containing glob special
    # characters (e.g. '[' or ']') and extensions are compared in lowercase to
    # support upper case extensions (e.g. '.WAV')
    any_ext = ".*" in ext
    ext = [e.lower() for e in ext]

    for dir_ in dir:
        if recursive:
            dir_files = glob(
                os.path.join(escape(dir_), "**", "*"),
                recursive=True
            )
        
        else:
            dir_files = glob(os.path.join(escape(dir_), "*"))
        
        all_files.extend(
            file for file in dir_files
            if any_ext or os.path.splitext(file)[1].lower() in ext
        )
    
    # Filter out folders with file-like names (e.g. ending in .wav extension)
    all_files = [file for file in all_files if os.path.isfile(file)]

    return sorted(set(all_files), key=key)


def read_audio_metadata(file: str) -> dict:
    """Reads the metadata block from an audio files and returns it as a
    `dict`.

    Args:
        file (str): Audio file.
    
    Returns:
        (dict): Audio metadata.
    """
    meta = sf.info(file, verbose=False)

    return {
        "fs": meta.samplerate,
        "num_channels": meta.channels,
        "num_samples_per_channel": meta.frames,
        "duration_seconds": meta.duration,
        "fmt": meta.format,
        "subtype": meta.subtype
    }


def read_audio(
        file: str,
        start: int = 0,
        frames: Optional[int] = -1,
        stop: Optional[int] = None,
        dtype: str = get_default_audio_io_dtype(),
) -> Tuple[np.ndarray, int]:
    """Reads an audio file or audio file chunk and returns it as a 
    `np.ndarray`.

    Args:
        file (str): Audio file.
        start (int): Start frame for reading partial frames of the file.
        frames Optional[int]: Number of frames to read.
        stop (Optional[int]): End frame index for reading partial frames of the
            file.
        dtype (str): Data type used to represent the data.
    
    Returns:
        (Tuple[np.ndarray, int]): `np.ndarray` representing the audio data and
            sample rate `tuple`.
    """
    is_file_or_error(file)

    # Read audio in (num_channels, num_samples) format
    data, fs_ = sf.read(
        file,
        dtype=dtype,
        always_2d=True,
        start=start,
        stop=stop,
        frames=frames
    )

    return data.transpose(), fs_


def ask_confirmation(
            s: str = "<magenta><b>Do you want to continue? [y/n]:</b>"
                     "</magenta> ",
            exit_s: str = "Program finished by the user",
            exit: bool = True
    ) -> bool:
        """Request user input to confirm or reject an instruction.

        Args:
            s (str): Message to be printed to ask user confirmation.
            exit_s (str): Message to be printed if the program execution is
                terminated.
            exit (bool): If `True` and user answer is `n` (no), then
                the program execution is terminated.

        Returns:
            bool: User response.
        """
        user_input = None

        while str(user_input) not in ["y", "n"]:
            if user_input is not None:
                print_error(f"Invalid input '{user_input}'")

            try:
                user_input = input(_decorate_str(s))
            
            except EOFError:
                exit_error(
                    "No user input available. Use --unattended or -u to skip "
                    "user confirmation"
                )

            if str(user_input) == "y":
                response = True

            elif str(user_input) == "n":
                if exit:
                    exit_warning(exit_s)

                else:
                    response = False
            else:
                pass

        return response
