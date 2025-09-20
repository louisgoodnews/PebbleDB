"""
Author: Louis Goodnews
Date: 2025-09-13
"""

import asyncio
import inspect
import threading

from typing import (
    get_args,
    get_origin,
    Any,
    Callable,
    Coroutine,
    Dict,
    Final,
    List,
    Literal,
    Optional,
    Set,
    Tuple,
    Type,
    Union,
)


__all__: Final[list[str]] = [
    "analyze_property",
    "analyze_typing",
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


def analyze_property(property_: Any) -> Type[Any]:
    """
    Analyze the passed property and return the result.

    Args:
        property_ (Any): The property to analyze.

    Returns:
        Type[Any]: The result of the analysis.
    """

    # Check if the passed property is a property
    if not isinstance(
        property_,
        property,
    ):
        # Return the type of the property
        return property_.__class__

    # Return the return type of the property
    return property_.fget.__annotations__.get(
        "return",
        Any,
    )


def analyze_typing(
    typing: Type[Any],
) -> Union[list[Any], Type[Any]]:
    """
    Analyze the passed typing and return the result.

    Args:
        typing (Type[Any]): The typing to analyze.

    Returns:
        Union[list[Any], Type[Any]]: The result of the analysis.
    """

    # Initialize the result to None
    result: Optional[Union[list[Any], Type[Any]]] = None

    # Check if the typing is Any
    if typing is Any:

        class AnyType:
            """
            Dummy class that passes isinstance checks for Any.
            """

            def __instancecheck__(
                self,
                instance,
            ) -> bool:
                """
                Check if the passed instance is an instance of the AnyType class.

                Args:
                    instance (Any): The instance to check.

                Returns:
                    bool: True if the instance is an instance of the AnyType class, False otherwise.
                """

                # Return True
                return True

        # Return the AnyType class
        return AnyType

    try:
        # Attempt to get the origin of the typing
        origin: Type[Any] = get_origin(typing)
    except Exception:
        # Return the typing to the caller
        return typing

    # Check if the origin of the typing is Final, Literal or Optional
    if origin in {
        Dict,
        Final,
        List,
        Literal,
        Optional,
        Set,
        Tuple,
        Union,
    }:
        # Get the args of the typing
        args: tuple[Any] = get_args(typing)

        # Initialize the result list to an empty list
        result = []

        # Iterate over the args
        for arg in args:
            # Append the current argument to the result list
            result.append(analyze_typing(typing=arg))

    # Check, if the result is None:
    if result is None:
        # Return the typing to the caller
        return typing

    # Check, if the result list contains only one element:
    if len(result) == 1:
        # Return the single element of the result list
        return result[0]

    # Return the result list to the caller
    return result


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
