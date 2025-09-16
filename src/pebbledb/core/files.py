"""
Author: Louis Goodnews
Date: 2025-09-13
"""

import aiofiles
import asyncio

from pathlib import Path
from typing import Final, Optional


__all__: Final[list[str]] = [
    "create_file",
    "create_file_if_not_exists",
    "delete_file",
    "read_file",
    "read_file_if_not_exists",
    "write_file",
    "write_file_if_not_exists",
]


# Initialize the asyncio.Lock object to None
_LOCK: Optional[asyncio.Lock] = None


def _lock() -> asyncio.Lock:
    """
    Return a lock object.

    Returns:
        asyncio.Lock: The lock object.
    """

    # Declare the global _LOCK variable
    global _LOCK

    # Check if the global _LOCK variable is None
    if _LOCK is None:
        # Create a new asyncio.Lock object
        _LOCK = asyncio.Lock()

    # Return the global _LOCK variable
    return _LOCK


async def create_file(
    path: Path,
) -> bool:
    """
    Create a file at the passed path.

    Args:
        path (Path): The path to the file to create.

    Returns:
        bool: True if the file was created, False otherwise.
    """

    # Acquire the lock
    async with _lock():
        try:
            # Open the file
            async with aiofiles.open(
                path.as_posix(),
                encoding="utf-8",
                mode="w",
            ) as file:
                # Write an empty string to the file
                await file.write("")

            # Return True if the file was created
            return True
        except Exception:
            # Return False if the file was not created
            return False


async def create_file_if_not_exists(
    path: Path,
) -> bool:
    """
    Create a file at the passed path if it does not exist.

    This method is a wrapper around the create_file method.
    It is used to create a file if it does not exist.

    Args:
        path (Path): The path to the file to create.

    Returns:
        bool: True if the file was created, False otherwise.
    """

    # Check if the file exists
    if not path.exists():
        # Create the file
        return await create_file(path=path)

    # Return True if the file was created
    return True


async def delete_file(
    path: Path,
) -> bool:
    """
    Delete a file at the passed path.

    Args:
        path (Path): The path to the file to delete.

    Returns:
        bool: True if the file was deleted, False otherwise.
    """

    # Acquire the lock
    async with _lock():
        try:
            # Check if the file exists
            if not path.exists():
                # Return True if the file was deleted
                return True

            # Delete the file
            path.unlink()

            # Return True if the file was deleted
            return True
        except Exception:
            # Return False if the file was not deleted
            return False


async def read_file(
    path: Path,
) -> str:
    """
    Read a file at the passed path.

    Args:
        path (Path): The path to the file to read.

    Returns:
        str: The content of the file if it was read, an empty string otherwise.
    """

    # Acquire the lock
    async with _lock():
        try:
            # Open the file
            async with aiofiles.open(
                path.as_posix(),
                encoding="utf-8",
                mode="r",
            ) as file:
                # Return the content of the file
                return await file.read()
        except Exception:
            # Return an empty string if the file was not read
            return ""


async def read_file_if_not_exists(
    path: Path,
) -> str:
    """
    Read a file at the passed path if it exists.

    This method is a wrapper around the create_file and read_file methods.
    It is used to create a file if it does not exist and read it.

    Args:
        path (Path): The path to the file to read.

    Returns:
        str: The content of the file if it was read, an empty string otherwise.
    """

    # Check if the file exists
    if not path.exists():
        # Create the file
        await create_file(path=path)

    # Read the file
    return await read_file(path=path)


async def write_file(
    path: Path,
    content: str,
) -> bool:
    """
    Write a file at the passed path.

    Args:
        path (Path): The path to the file to write.
        content (str): The content to write to the file.

    Returns:
        bool: True if the file was written, False otherwise.
    """

    # Acquire the lock
    async with _lock():
        try:
            # Open the file
            async with aiofiles.open(
                path.as_posix(),
                encoding="utf-8",
                mode="w",
            ) as file:
                # Write the content to the file
                await file.write(content)

            # Return True if the file was written
            return True
        except Exception:
            # Return False if the file was not written
            return False


async def write_file_if_not_exists(
    path: Path,
    content: str,
) -> bool:
    """
    Write a file at the passed path if it does not exist.

    This method is a wrapper around the create_file and write_file methods.
    It is used to create a file if it does not exist and write to it.

    Args:
        path (Path): The path to the file to write.
        content (str): The content to write to the file.

    Returns:
        bool: True if the file was written, False otherwise.
    """

    # Check if the file exists
    if not path.exists():
        # Create the file
        await create_file(path=path)

    # Write the file
    return await write_file(
        path=path,
        content=content,
    )
