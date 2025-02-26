from typing import Any
from hashlib import sha256


def generate_sha256(obj: Any) -> str:
    """Generates a SHA-256 hash of an object.
    
    Args:
        obj (Any): Input object.
    
    Returns:
        (str): SHA-256 representation of `obj`.
    """
    hasher = sha256()
    # NOTE: Prevents different hashes caused by different memory addresses
    hasher.update(repr(obj))
    hash = hasher.hexdigest()
    return hash


def verify_sha256(obj: Any, hash: str) -> bool:
    """Checks if the SHA-256 hash of an object matches a given hash.
    
    Args:
        obj (Any): Input object to check.
        hash (str): Ground truth hash to check.
    
    Returns:
        (bool): `True` if `obj` hash and `hash` are the same, `False`
            otherwise.
    """
    obj_hash = generate_sha256(obj)
    return obj_hash == hash


def generate_sha256_from_file(file: str, block_size: int = 65_536) -> str:
    """Generates a SHA-256 hash of a file.
    
    Args:
        file (str): Input file.
        block_size (int): Block size used to read the file.
    
    Returns:
        (str): SHA-256 hash of the file's content.
    """
    # NOTE: block_size should ideally be multiple of the byte digest block
    hasher = sha256()

    with open(file, "rb") as f:
        for block in iter(lambda: f.read(block_size), b""):
            hasher.update(block)

    hash = hasher.hexdigest()
    return hash


def verify_sha256_from_file(
        file: str,
        hash: str,
        block_size: int = 65_536
) -> bool:
    """Checks if the SHA-256 hash of a file matches a given hash.
    
    Args:
        file (str): Input file to check.
        hash (str): Ground truth hash to check.
        block_size (int): Block size used to read the file.
    
    Returns:
        (bool): `True` if the file's hash and `hash` are the same, `False`
            otherwise.
    """
    file_hash = generate_sha256_from_file(file, block_size=block_size)
    return file_hash == hash
