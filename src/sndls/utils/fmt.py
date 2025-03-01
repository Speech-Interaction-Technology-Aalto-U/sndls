import sys
from tqdm import tqdm
from typing import Optional
from .config import (
    _get_text_color_tags,
    _get_text_decorator_tags
)


def _decorate_str(s: str) -> str:
    """Replaces colors and decorators in a string.

    Args:
        s (str): The input string to be decorated.

    Returns:
        str: The decorated string.
    """
    # Replace colors and decorators
    for k, v in _get_text_decorator_tags().items():
        s = s.replace(k, v)

    for k, v in _get_text_color_tags().items():
        s = s.replace(k, v)

    return s


def printc(s: str, writer: Optional[tqdm] = None) -> None:
    """Prints a formatted string.

    Args:
        s (str): The string to print.
        writer (Optional[tqdm]): Writer to use.
    """
    return (
        print(_decorate_str(s)) if writer is None
        else writer.write(_decorate_str(s))
    )


def printc_exit(
        s: str,
        code: int = 0,
        writer: Optional[tqdm] = None
) -> None:
    """Prints a formatted string and exits the program with a specified exit
    code.

    Args:
        s (str): The string to print.
        code (int): Exit code.
        writer (Optional[tqdm]): Writer to use.
    """
    printc(s=s, writer=writer)
    sys.exit(code)


def print_error(s: str, writer: Optional[tqdm] = None) -> None:
    """Prints an error.
    
    Args:
        s (str): Error message print.
        writer (Optional[tqdm]): Writer to use.
    """
    printc(f"<error>{s}</error>", writer=writer)


def print_warning(s: str, writer: Optional[tqdm] = None) -> None:
    """Prints a warning.
    
    Args:
        s (str): Warning message to print.
        writer (Optional[tqdm]): Writer to use.
    """
    printc(f"<warning>{s}</warning>", writer=writer)


def exit_error(s: str, code: int = 1, writer: Optional[tqdm] = None) -> None:
    """Prints an error and stops the execution of the program.
    
    Args:
        s (str): Error message to print.
        code (int): Exit code.
        writer (Optional[tqdm]): Writer to use.
    """
    print_error(s, writer=writer)
    sys.exit(code)


def exit_warning(s: str, code: int = 1, writer: Optional[tqdm] = None) -> None:
    """Prints a warning and stops the execution of the program.

    Args:
        s (str): Warning message to print.
        code (int): Exit code.
        writer (Optional[tqdm]): Writer to use.
    """
    print_warning(s, writer=writer)
    sys.exit(code)


def bytes_to_str(bytes: int) -> str:
    """Returns an amount of bytes in a human readable format.
    
    Args:
        bytes (int): Number of bytes to represent.

    Returns:
        (str): `str` representation of `bytes`.
    """
    if bytes / (1024 ** 4) > 1.0:
        repr = f"{bytes / 1024 ** 4:.1f}T"

    elif bytes / (1024 ** 3) > 1.0:
        repr = f"{bytes / 1024 ** 3:.1f}G"
        
    elif bytes / (1024 ** 2) > 1.0:
        repr = f"{bytes / 1024 ** 2:.1f}M"
        
    elif bytes / 1024 > 1.0:
        repr = f"{bytes / 1024:.1f}K"
        
    else:
        repr = f"{bytes:d}B"
    
    return repr


def time_to_str(time: float, abbrev: bool = False) -> str:
    """Returns a time in seconds in a human readable format.
    
    Args:
        time (float): Time in seconds.
        abbrev (bool): If `True`, abbreviations to represent different time
            units are used.
    
    Returns:
        (str): `str` representation of `time`.
    """
    if abbrev:
        ms_repr = "ms"
        s_repr = "s"
        m_repr = "m"
        h_repr = "h"
    
    else:
        ms_repr = "millisecond(s)"
        s_repr = "second(s)"
        m_repr = "minute(s)"
        h_repr = "hour(s)"

    if time < 1.0:
        time_repr = f"{time * 1e3:.1f} {ms_repr}"

    elif time < 60.0:
        time_repr = f"{time:.1f} {s_repr}"
    
    elif time < 3600.0:
        time_mins = time // 60.0
        time_secs = time % 60
        time_repr = f"{int(time_mins)} {m_repr} {int(time_secs)} {s_repr}" 

    else:            
        time_hours = time // 3600.0
        remaining_time = time % 3600.0
        time_mins = remaining_time // 60.0
        time_secs = remaining_time % 60
        time_repr = (
            f"{int(time_hours)} {h_repr} {int(time_mins)} {m_repr} "
            f"{int(time_secs)} {s_repr}"
        )

    return time_repr
