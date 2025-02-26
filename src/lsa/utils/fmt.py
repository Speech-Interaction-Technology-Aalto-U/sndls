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


def print_error(s: str) -> None:
    """Prints an error."""
    printc(f"<error>{s}</error>")


def print_warning(s: str) -> None:
    """Prints a warning."""
    printc(f"<warning>{s}</warning>")


def exit_error(s: str, code: int = 1) -> None:
    """Prints an error and stops the execution of the program."""
    print_error(s)
    sys.exit(code)


def exit_warning(s: str, code: int = 1) -> None:
    """Prints a warning and stops the execution of the program."""
    print_warning(s)
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
