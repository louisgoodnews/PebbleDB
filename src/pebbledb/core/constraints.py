"""
Author: Louis Goodnews
Date: 2025-09-20
"""

import re

from typing import override, Any, Final, Optional, Set, Union


__all__: Final[list[str]] = [
    "PebbleConstraint",
    "PebbleChoiceConstraint",
    "PebbleMaxLengthConstraint",
    "PebbleMinLengthConstraint",
    "PebbleNotNullConstraint",
    "PebbleRangeConstraint",
    "PebbleRegexConstraint",
    "PebbleTypeConstraint",
    "PebbleUniqueConstraint",
]


class PebbleConstraint:
    """
    A class representing a constraint in the PebbleDB library
    """

    def __repr__(self) -> str:
        """
        Return a string representation of the instance.

        Returns:
            str: The string representation of the instance.
        """

        # Return a string representation of the instance
        return f"<{self.__class__.__name__}({', '.join([f'{key.lstrip('_')}={value!r}' for key, value in self.__dict__.items()])})>"

    def __str__(self) -> str:
        """
        Return a string representation of the instance.

        Returns:
            str: The string representation of the instance.
        """

        # Return a string representation of the instance
        return self.__repr__()

    def validate(
        self,
        **kwargs,
    ) -> bool:
        """
        Validate the passed value.

        Args:
            **kwargs: The keyword arguments to validate.

        Returns:
            bool: True if the value is valid, False otherwise.
        """

        # Raise a NotImplementedError exception
        raise NotImplementedError

    def to_dict(self) -> dict[str, Any]:
        """
        Convert the instance to a dictionary.

        Returns:
            dict[str, Any]: The dictionary representation of the instance.
        """

        # Raise a NotImplementedError exception
        raise NotImplementedError


class PebbleChoiceConstraint(PebbleConstraint):
    """
    A class representing a choice constraint in the PebbleDB library
    """

    def __init__(
        self,
        choices: list[Any],
    ) -> None:
        """
        Initialize the instance.

        Args:
            choices (list[Any]): The choices.

        Returns:
            None
        """

        # Store the passed choices in an instance variable
        self._choices: Final[list[Any]] = choices

    @property
    def choices(self) -> list[Any]:
        """
        Get the choices.

        Returns:
            list[Any]: The choices.
        """

        # Return the choices
        return self._choices

    @override
    def validate(
        self,
        value: Any,
    ) -> bool:
        """
        Validate the passed value.

        Args:
            value (Any): The value to validate.

        Returns:
            bool: True if the value is one of the choices, False otherwise.
        """

        # Return True if the value is one of the choices
        return value in self._choices

    @override
    def to_dict(self) -> dict[str, Any]:
        """
        Convert the instance to a dictionary.

        Returns:
            dict[str, Any]: The dictionary representation of the instance.
        """

        # Return the dictionary representation of the instance
        return {
            "choices": self._choices,
        }


class PebbleIsNullConstraint(PebbleConstraint):
    """
    A class representing a null constraint in the PebbleDB library
    """

    def __init__(
        self,
    ) -> None:
        """
        Initialize the instance.

        Returns:
            None
        """

        # Do nothing
        pass

    @override
    def validate(
        self,
        value: Any,
    ) -> bool:
        """
        Validate the passed value.

        Args:
            value (Any): The value to validate.

        Returns:
            bool: True if the value is null, False otherwise.
        """

        # Return True if the value is null
        return value is None

    @override
    def to_dict(self) -> dict[str, Any]:
        """
        Convert the instance to a dictionary.

        Returns:
            dict[str, Any]: The dictionary representation of the instance.
        """

        # Return the dictionary representation of the instance
        return {
            "is_null": True,
        }


class PebbleMaxLengthConstraint(PebbleConstraint):
    """
    A class representing a maximum length constraint in the PebbleDB library
    """

    def __init__(
        self,
        length: int,
    ) -> None:
        """
        Initialize the instance.

        Args:
            length (int): The maximum length.

        Returns:
            None
        """

        # Store the passed length in an instance variable
        self._length: Final[int] = length

    @property
    def length(self) -> int:
        """
        Get the maximum length.

        Returns:
            int: The maximum length.
        """

        # Return the maximum length
        return self._length

    @override
    def validate(
        self,
        value: Any,
    ) -> bool:
        """
        Validate the passed value.

        Args:
            value (Any): The value to validate.

        Returns:
            bool: True if the value is at most the maximum length, False otherwise.
        """

        # Return True if the value is at most the maximum length
        return len(value) <= self._length

    @override
    def to_dict(self) -> dict[str, Any]:
        """
        Convert the instance to a dictionary.

        Returns:
            dict[str, Any]: The dictionary representation of the instance.
        """

        # Return the dictionary representation of the instance
        return {
            "max_length": self._length,
        }


class PebbleMinLengthConstraint(PebbleConstraint):
    """
    A class representing a minimum length constraint in the PebbleDB library
    """

    def __init__(
        self,
        length: int,
    ) -> None:
        """
        Initialize the instance.

        Args:
            length (int): The minimum length.

        Returns:
            None
        """

        # Store the passed length in an instance variable
        self._length: Final[int] = length

    @property
    def length(self) -> int:
        """
        Get the minimum length.

        Returns:
            int: The minimum length.
        """

        # Return the minimum length
        return self._length

    @override
    def validate(
        self,
        value: Any,
    ) -> bool:
        """
        Validate the passed value.

        Args:
            value (Any): The value to validate.

        Returns:
            bool: True if the value is at least the minimum length, False otherwise.
        """

        # Return True if the value is at least the minimum length
        return len(value) >= self._length

    @override
    def to_dict(self) -> dict[str, Any]:
        """
        Convert the instance to a dictionary.

        Returns:
            dict[str, Any]: The dictionary representation of the instance.
        """

        # Return the dictionary representation of the instance
        return {
            "min_length": self._length,
        }


class PebbleNotNullConstraint(PebbleConstraint):
    """
    A class representing a not null constraint in the PebbleDB library
    """

    def __init__(
        self,
    ) -> None:
        """
        Initialize the instance.

        Returns:
            None
        """

        # Do nothing
        pass

    @override
    def validate(
        self,
        value: Any,
    ) -> bool:
        """
        Validate the passed value.

        Args:
            value (Any): The value to validate.

        Returns:
            bool: True if the value is not null, False otherwise.
        """

        # Return True if the value is not null
        return value is not None

    @override
    def to_dict(self) -> dict[str, Any]:
        """
        Convert the instance to a dictionary.

        Returns:
            dict[str, Any]: The dictionary representation of the instance.
        """

        # Return the dictionary representation of the instance
        return {
            "not_null": True,
        }


class PebbleRangeConstraint(PebbleConstraint):
    """
    A class representing a range constraint in the PebbleDB library
    """

    def __init__(
        self,
        maximum: Union[float, int],
        minimum: Union[float, int],
    ) -> None:
        """
        Initialize the instance.

        Args:
            maximum (Union[float, int]): The maximum value.
            minimum (Union[float, int]): The minimum value.

        Returns:
            None
        """

        # Store the passed maximum value in an instance variable
        self._maximum: Final[Union[float, int]] = maximum

        # Store the passed minimum value in an instance variable
        self._minimum: Final[Union[float, int]] = minimum

    @property
    def maximum(self) -> Union[float, int]:
        """
        Get the maximum value.

        Returns:
            Union[float, int]: The maximum value.
        """

        # Return the maximum value
        return self._maximum

    @property
    def minimum(self) -> Union[float, int]:
        """
        Get the minimum value.

        Returns:
            Union[float, int]: The minimum value.
        """

        # Return the minimum value
        return self._minimum

    @override
    def validate(
        self,
        value: Union[float, int],
    ) -> bool:
        """
        Validate the passed value.

        Args:
            value (Union[float, int]): The value to validate.

        Returns:
            bool: True if the value is within the range, False otherwise.

        Raises:
            TypeError: If the passed value is not a float or an int.
        """

        # Check, if the passed value is a float or an int
        if not isinstance(
            value,
            (
                float,
                int,
            ),
        ):
            # Raise a TypeError exception
            raise TypeError(f"Value must be a float or int, got {type(value)} instead")

        # Return True if the value is within the range
        return self._minimum <= value <= self._maximum

    @override
    def to_dict(self) -> dict[str, Any]:
        """
        Convert the instance to a dictionary.

        Returns:
            dict[str, Any]: The dictionary representation of the instance.
        """

        # Return the dictionary representation of the instance
        return {
            "maximum": self._maximum,
            "minimum": self._minimum,
        }


class PebbleRegexConstraint(PebbleConstraint):
    """
    A class representing a regex constraint in the PebbleDB library
    """

    def __init__(
        self,
        pattern: str,
    ) -> None:
        """
        Initialize the instance.

        Args:
            pattern (str): The regex pattern.

        Returns:
            None
        """

        # Store the passed pattern in an instance variable
        self._pattern: Final[str] = pattern

    @property
    def pattern(self) -> str:
        """
        Get the regex pattern.

        Returns:
            str: The regex pattern.
        """

        # Return the pattern
        return self._pattern

    @override
    def validate(
        self,
        value: Any,
    ) -> bool:
        """
        Validate the passed value.

        Args:
            value (Any): The value to validate.

        Returns:
            bool: True if the value matches the regex, False otherwise.
        """

        # Return True if the value matches the regex
        return re.match(self._pattern, value) is not None

    @override
    def to_dict(self) -> dict[str, Any]:
        """
        Convert the instance to a dictionary.

        Returns:
            dict[str, Any]: The dictionary representation of the instance.
        """

        # Return the dictionary representation of the instance
        return {
            "pattern": self._pattern,
        }


class PebbleRequiredConstraint(PebbleConstraint):
    """ """

    def __init__(
        self,
        field: str,
    ) -> None:
        """ """

        self._field: Final[str] = field

    @override
    def validate(
        self,
        entry: dict[str, Any],
    ) -> bool:
        """
        Validate the passed entry.

        Args:
            entry (dict[str, Any]): The entry to validate.

        Returns:
            bool: True if the entry is valid, False otherwise.
        """

        # Return True if the field is not None
        return entry.get(self._field, None) is not None

    @override
    def to_dict(self) -> dict[str, Any]:
        """
        Convert the instance to a dictionary.

        Returns:
            dict[str, Any]: The dictionary representation of the instance.
        """

        # Return the dictionary representation of the instance
        return {
            "required": self._field,
        }


class PebbleTypeConstraint(PebbleConstraint):
    """
    A class representing a type constraint in the PebbleDB library
    """

    def __init__(
        self,
        type_: type,
    ) -> None:
        """
        Initialize the instance.

        Args:
            type_ (type): The type to validate.

        Returns:
            None
        """

        # Store the passed type in an instance variable
        self._type_: Final[type] = type_

    @property
    def type_(self) -> type:
        """
        Get the type.

        Returns:
            type: The type.
        """

        # Return the type
        return self._type_

    @override
    def validate(self, value: Any) -> bool:
        """
        Validate the passed value.

        Args:
            value (Any): The value to validate.

        Returns:
            bool: True if the value is of the correct type, False otherwise.
        """

        # Return True if the value is of the correct type
        return isinstance(value, self._type_)

    @override
    def to_dict(self) -> dict[str, Any]:
        """
        Convert the instance to a dictionary.

        Returns:
            dict[str, Any]: The dictionary representation of the instance.
        """

        # Return the dictionary representation of the instance
        return {
            "type": self._type_.__name__,
        }


class PebbleUniqueConstraint(PebbleConstraint):
    """
    A class representing a unique constraint in the PebbleDB library
    """

    def __init__(
        self,
        field: str,
    ) -> None:
        """
        Initialize the instance.

        Args:
            field (str): The field to validate.

        Returns:
            None
        """

        # Store the passed field in an instance variable
        self._field: Final[str] = field

    @property
    def field(self) -> str:
        """
        Get the field.

        Returns:
            str: The field.
        """

        # Return the field
        return self._field

    @override
    def validate(
        self,
        entries: list[dict[str, Any]],
    ) -> bool:
        """
        Validate the passed entries.

        Args:
            entries (list[dict[str, Any]]): The entries to validate.

        Returns:
            bool: True if the entries are valid, False otherwise.
        """

        # Initialize an empty set to store the field values
        seen: set[Any] = set()

        # Iterate over the entries
        for entry in entries:
            # Get the field value
            value: Optional[Any] = entry.get(self._field, None)

            # Check if the field value is None
            if value is None:
                # Skip the entry if the field value is None
                continue

            # Check if the field value is already in the store
            if value in seen:
                # Return False if the field value is already in the store
                return False

            # Add the field value to the store
            seen.add(value)

        # Return True if the entries are valid
        return True

    @override
    def to_dict(self) -> dict[str, Any]:
        """
        Convert the instance to a dictionary.

        Returns:
            dict[str, Any]: The dictionary representation of the instance.
        """

        # Return the dictionary representation of the instance
        return {
            "unique": self._field,
        }
