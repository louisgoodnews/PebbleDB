"""
Author: Louis Goodnews
Date: 2025-09-13
"""

import asyncio
import inspect
import threading

from typing import Any, Callable, Coroutine, Final, Optional


__all__: Final[list[str]] = [
    "merge_dicts",
    "NotACoroutineFunctionError",
    "run_async",
]


# Initialize the asyncio.AbstractEventLoop object to None
_LOOP: Optional[asyncio.AbstractEventLoop] = None

# Initialize the threading.Lock object
_LOOP_LOCK: Final[threading.Lock] = threading.Lock()


class NotACoroutineFunctionError(Exception):
    """
    Exception raised when the passed function is not a coroutine function.
    """


def _loop() -> asyncio.AbstractEventLoop:
    """
    Return the asyncio.AbstractEventLoop object in a thread-safe manner.
    Uses a lock to prevent race conditions when multiple threads try to access
    or modify the _LOOP variable simultaneously.

    Returns:
        asyncio.AbstractEventLoop: The asyncio.AbstractEventLoop object.

    Note:
        This function is thread-safe. The first call will initialize the event loop
        and subsequent calls will return the cached instance.
    """

    # Declare the global _LOOP variable
    global _LOOP

    # Fast path: If _LOOP is already set, return it immediately
    if _LOOP is not None:
        # Return the asyncio.AbstractEventLoop object
        return _LOOP

    # Use a lock to ensure thread safety during initialization
    with _LOOP_LOCK:
        # Double-checked locking pattern: check again in case another thread
        # initialized _LOOP while we were waiting for the lock
        if _LOOP is None:
            try:
                # Get the asyncio.AbstractEventLoop object
                _LOOP = asyncio.get_event_loop()
            except RuntimeError:
                # Create a new asyncio.AbstractEventLoop object
                _LOOP = asyncio.new_event_loop()

        # Set the asyncio.AbstractEventLoop object
        asyncio.set_event_loop(loop=_LOOP)

    # Return the asyncio.AbstractEventLoop object
    return _LOOP


def merge_dicts(
    new: dict[str, Any],
    old: dict[str, Any],
) -> dict[str, Any]:
    """
    Merge the passed new dictionary into the passed old dictionary.

    Args:
        new (dict[str, Any]): The new dictionary to merge.
        old (dict[str, Any]): The old dictionary to merge into.

    Returns:
        dict[str, Any]: The merged dictionary.
    """

    # Initialize the result to a copy of the old dictionary
    result: dict[str, Any] = old.copy()

    # Iterate over the new dictionary
    for (
        new_key,
        new_value,
    ) in new.items():
        # Get the old value
        old_value = result.get(new_key)

        # Check if the old value is None
        if old_value is None:
            # Set the new value
            result[new_key] = new_value
        else:
            # Check if both values are dictionaries
            if isinstance(
                old_value,
                dict,
            ) and isinstance(
                new_value,
                dict,
            ):
                # Merge the dictionaries
                result[new_key] = merge_dicts(
                    new=new_value,
                    old=old_value,
                )
            else:
                # Set the new value
                result[new_key] = new_value

    return result


def run_async(
    function: Callable[..., Any],
    *args,
    **kwargs,
) -> Any:
    """
    Run the passed function asynchronously.

    Args:
        function (Callable[..., Any]): The function to run asynchronously.
        *args: The arguments to pass to the function.
        **kwargs: The keyword arguments to pass to the function.

    Returns:
        Any: The result of the function.

    Raises:
        NotACoroutineFunctionError: If the passed function is not a coroutine function.
    """

    # Check if the passed function is a coroutine function
    if not inspect.iscoroutinefunction(obj=function):
        # Raise a NotACoroutineFunctionError exception
        raise NotACoroutineFunctionError(
            "The passed function is not a coroutine function.",
        )

    # Get the asyncio.AbstractEventLoop object
    loop: asyncio.AbstractEventLoop = _loop()

    # Create a coroutine object
    coroutine: Coroutine = function(
        *args,
        **kwargs,
    )

    # Check if the asyncio.AbstractEventLoop object is running
    if not loop.is_running():
        # Run the passed function asynchronously
        return asyncio.run(main=coroutine)

    # Return the result of the function
    return loop.run_until_complete(future=coroutine)
