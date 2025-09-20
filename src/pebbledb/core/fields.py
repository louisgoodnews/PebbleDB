"""
Author: Louis Goodnews
Date: 2025-09-13
"""

import frozendict
import json

from datetime import date, datetime, time
from decimal import Decimal
from pathlib import Path
from typing import Any, Final, Literal, Optional, Type
from uuid import UUID

from core.constants import (
    BOOLEAN,
    CUSTOM,
    CWD,
    DATE,
    DATETIME,
    DECIMAL,
    DICTIONARY,
    FLOAT,
    FROZENDICT,
    FROZENSET,
    INTEGER,
    LIST,
    MISSING,
    NULL,
    PATH,
    STRING,
    TIME,
    TUPLE,
    UUID,
)

from datautils import DataConversionUtils


__all__: Final[list[str]] = [
    "PebbleField",
    "PebbleBooleanField",
    "PebbleCustomField",
    "PebbleDateField",
    "PebbleDateTimeField",
    "PebbleDecimalField",
    "PebbleDictionaryField",
    "PebbleFloatField",
    "PebbleFrozendictField",
    "PebbleFrozensetField",
    "PebbleIntegerField",
    "PebbleListField",
    "PebbleNullField",
    "PebblePathField",
    "PebbleStringField",
    "PebbleTimeField",
    "PebbleTupleField",
    "PebbleUUIDField",
    "PebbleFieldFactory",
    "PebbleFieldBuilder",
]


class PebbleField:
    """
    A base class for all Pebble fields.
    """

    name: Final[str]

    def __init__(
        self,
        **kwargs,
    ) -> None:
        """
        Initialize the instance.

        Args:
            **kwargs: The keyword arguments to initialize the instance with.

        Returns:
            None
        """

        # Iterate over the field field type pairs in the annotations
        for (
            field,
            field_type,
        ) in self.__annotations__.items():
            # Check if the current field is contained in the keyword arguments
            if field in kwargs:
                # Get the value corresponding to the current fied
                value: Any = kwargs.get(
                    field,
                    getattr(
                        self.__class__,
                        field,
                    ),
                )
            else:
                # Get the value corresponding to the current fied
                value: Any = getattr(
                    self.__class__,
                    field,
                    MISSING,
                )

            # Check if the current field is missing (i.e. the generic missing value)
            if value is MISSING:
                # Raise a ValueError over the missing field
                raise ValueError(f"Missing required field: {field}")

            # Check if the current field's type corresponds to the current field type
            if not isinstance(
                value,
                field_type,
            ):
                # Raise a TypeError if the actual type does not match the annotated one
                raise TypeError(f"Field {field} expected {field_type}, got {type(value)}")

            # Set the current key value pair as attributes of this instance
            setattr(
                self,
                field,
                value,
            )

    def __init_subclass__(cls) -> None:
        """
        Initialize the subclass.

        Args:
            cls (Type): The subclass to initialize.

        Returns:
            None
        """

        # Call the parent class' __init_subclass__ method
        super().__init_subclass__()

        # Iterate over the field field type pairs in the annotations
        for (
            field,
            field_type,
        ) in cls.__annotations__.items():

            def getter(
                self,
                key: str = field,
            ) -> Any:
                """
                Return the value associated with the passed key (i.e. the field).

                Args:
                    key (str, optional): The key to retrieve. Defaults to field.

                Returns:
                    Any: The value associated with the passed key.
                """

                # Return the value associated with the passed key (i.e. the field)
                return self.__dict__[key]

            def setter(
                self,
                value: Any,
                key: str = field,
                type_: Type = field_type,
            ) -> None:
                """
                Set the value associated with the passed key (i.e. the field).

                Args:
                    key (str, optional): The key to retrieve. Defaults to field.
                    type_ (Type, optional): The type of the value to set. Defaults to field_type.
                    value (Any): The value to set.

                Returns:
                    None
                """

                # Check if the values's type corresponds to the passed expected type
                if not isinstance(
                    value,
                    type_,
                ):
                    # Raise a TypeError if the actual type does not match the annotated one
                    raise TypeError(f"Field {key} expected {type_}, got {type(value)}")

                # Set the current key value pair as attributes of this instance
                setattr(
                    self,
                    key,
                    value,
                )

            # Append the property to the subclass
            setattr(
                cls,
                field,
                property(
                    getter,
                    setter,
                ),
            )

    def __getitem__(
        self,
        key: str,
    ) -> Any:
        """
        Return the value associated with the passed key.
        Will raise a KeyError exception if the passed key does not exist in the dictionary representation of this object.

        Args:
            key (str): The key to retrieve.

        Returns:
            Any: The value associated with the passed key.
        """

        # Return the value associated with the passed key
        # Will raise a KeyError exception if the passed key does not exist in the dictionary representation of this object
        return self.__dict__[key]

    def __repr__(self) -> str:
        """
        Return a string representation of the PebbleField instance.

        Returns:
            str: A string representation of the PebbleField instance.
        """

        # Return a string representation of the PebbleField instance
        return f"<{self.__class__.__name__}({', '.join(f'{key}={value}' for key, value in self.__dict__.items())})>"

    def __setitem__(
        self,
        key: str,
        value: Any,
    ) -> None:
        """
        Update the dictionary representation of this object with the passed key value pair.
        Will update the existing key with the passed value.

        Args:
            key (str): The key to update.
            value (Any): The value to update.
        """

        # Update the dictionary representation of this object with the passed key value pair
        # Will update the existing key with the passed value
        self.__dict__[key] = value

    def __str__(self) -> str:
        """
        Return a string representation of the PebbleField instance.

        Returns:
            str: A string representation of the PebbleField instance.
        """

        # Return a string representation of the PebbleField instance
        return self.__repr__()

    @classmethod
    def from_dict(
        cls,
        dictionary: dict[str, Any],
    ) -> "PebbleField":
        """
        Return a dictionary representation of the PebbleField instance.

        Args:
            dictionary (dict[str, Any]): The dictionary to convert to a PebbleField instance.

        Returns:
            PebbleField: A dictionary representation of the PebbleField instance.
        """

        # Return a dictionary representation of the PebbleField instance
        return PebbleField(**dictionary)

    @classmethod
    def from_json(
        cls,
        string: str,
    ) -> "PebbleField":
        """
        Return a dictionary representation of the PebbleField instance.

        Args:
            string (str): The string to convert to a PebbleField instance.

        Returns:
            PebbleField: A dictionary representation of the PebbleField instance.
        """

        # Return a dictionary representation of the PebbleField instance
        return PebbleField(**json.loads(string))

    def to_dict(
        self,
        exclude: Optional[list[str]] = None,
    ) -> dict[str, Any]:
        """
        Return a dictionary representation of the PebbleField instance.

        Args:
            exclude (Optional[list[str]], optional): The keys to exclude from the dictionary representation. Defaults to None.

        Returns:
            dict[str, Any]: A dictionary representation of the PebbleField instance.
        """

        # Check if there are keys to exclude
        if exclude is not None:
            # Return the dictionary representation of this instance without the excluded keys
            return {
                key: value
                for (
                    key,
                    value,
                ) in self.__dict__.items()
                if key not in exclude
            }

        # Return a copy of the dictionary representation of this instance
        return self.__dict__.copy()

    def value_from_json(
        self,
        value: str,
    ) -> Any:
        """
        Return a value from a JSON representation.

        Args:
            value (str): The JSON representation to convert to a value.

        Returns:
            Any: A value from a JSON representation.
        """

        # Raise a NotImplementedError exception
        raise NotImplementedError

    def value_to_json(
        self,
        value: Any,
    ) -> str:
        """
        Return a JSON representation of the value.

        Args:
            value (Any): The value to convert to a JSON representation.

        Returns:
            str: A JSON representation of the value.
        """

        # Raise a NotImplementedError exception
        raise NotImplementedError


class PebbleBooleanField(PebbleField):
    """ """

    # Define the field type as a final literal (i.e. the field type cannot be changed)
    _field_type: Final[Literal["boolean"]] = BOOLEAN

    # Define the default value for this field
    default: bool = False

    # Define if this field can be null
    nullable: bool = True


class PebbleCustomField(PebbleField):
    """ """

    # Define the field type as a final literal (i.e. the field type cannot be changed)
    _field_type: Final[Literal["custom"]] = CUSTOM

    # Define the default value for this field
    default: Any = None

    # Define if this field can be null
    nullable: bool = True


class PebbleDateField(PebbleField):
    """ """

    # Define the field type as a final literal (i.e. the field type cannot be changed)
    _field_type: Final[Literal["date"]] = DATE

    # Define the default value for this field
    default: date = None

    # Define if this field can be null
    nullable: bool = True


class PebbleDateTimeField(PebbleField):
    """ """

    # Define the field type as a final literal (i.e. the field type cannot be changed)
    _field_type: Final[Literal["datetime"]] = DATETIME

    # Define the default value for this field
    default: datetime = None

    # Define if this field can be null
    nullable: bool = True


class PebbleDecimalField(PebbleField):
    """ """

    # Define the field type as a final literal (i.e. the field type cannot be changed)
    _field_type: Final[Literal["decimal"]] = DECIMAL

    # Define the default value for this field
    default: Decimal = None

    # Define if this field can be null
    nullable: bool = True


class PebbleDictionaryField(PebbleField):
    """ """

    # Define the field type as a final literal (i.e. the field type cannot be changed)
    _field_type: Final[Literal["dictionary"]] = DICTIONARY

    # Define the default value for this field
    default: dict = None

    # Define if this field can be null
    nullable: bool = True


class PebbleFloatField(PebbleField):
    """ """

    # Define the field type as a final literal (i.e. the field type cannot be changed)
    _field_type: Final[Literal["float"]] = FLOAT

    # Define the default value for this field
    default: float = None

    # Define if this field can be null
    nullable: bool = True


class PebbleFrozendictField(PebbleField):
    """ """

    # Define the field type as a final literal (i.e. the field type cannot be changed)
    _field_type: Final[Literal["frozendict"]] = FROZENDICT

    # Define the default value for this field
    default: frozendict = None

    # Define if this field can be null
    nullable: bool = True


class PebbleFrozensetField(PebbleField):
    """ """

    # Define the field type as a final literal (i.e. the field type cannot be changed)
    _field_type: Final[Literal["frozenset"]] = FROZENSET

    # Define the default value for this field
    default: frozenset = None

    # Define if this field can be null
    nullable: bool = True


class PebbleIntegerField(PebbleField):
    """ """

    # Define the field type as a final literal (i.e. the field type cannot be changed)
    _field_type: Final[Literal["integer"]] = INTEGER

    # Define the default value for this field
    default: int = None

    # Define if this field can be null
    nullable: bool = True


class PebbleListField(PebbleField):
    """ """

    # Define the field type as a final literal (i.e. the field type cannot be changed)
    _field_type: Final[Literal["list"]] = LIST

    # Define the default value for this field
    default: list = None

    # Define if this field can be null
    nullable: bool = True


class PebbleNullField(PebbleField):
    """ """

    # Define the field type as a final literal (i.e. the field type cannot be changed)
    _field_type: Final[Literal["null"]] = NULL

    # Define the default value for this field
    default: None = None

    # Define if this field can be null
    nullable: bool = True


class PebblePathField(PebbleField):
    """ """

    # Define the field type as a final literal (i.e. the field type cannot be changed)
    _field_type: Final[Literal["path"]] = PATH

    # Define the default value for this field
    default: Path = CWD

    # Define if this field can be null
    nullable: bool = True


class PebbleStringField(PebbleField):
    """ """

    # Define the field type as a final literal (i.e. the field type cannot be changed)
    _field_type: Final[Literal["string"]] = STRING

    # Define the default value for this field
    default: str = None

    # Define if this field can be null
    nullable: bool = True


class PebbleTimeField(PebbleField):
    """ """

    # Define the field type as a final literal (i.e. the field type cannot be changed)
    _field_type: Final[Literal["time"]] = TIME

    # Define the default value for this field
    default: time = None

    # Define if this field can be null
    nullable: bool = True


class PebbleTupleField(PebbleField):
    """ """

    # Define the field type as a final literal (i.e. the field type cannot be changed)
    _field_type: Final[Literal["tuple"]] = TUPLE

    # Define the default value for this field
    default: tuple = None

    # Define if this field can be null
    nullable: bool = True


class PebbleUUIDField(PebbleField):
    """ """

    # Define the field type as a final literal (i.e. the field type cannot be changed)
    _field_type: Final[Literal["uuid"]] = UUID

    # Define the default value for this field
    default: UUID = None

    # Define if this field can be null
    nullable: bool = True


class PebbleFieldFactory:
    """ """

    pass


class PebbleFieldBuilder:
    """ """

    pass
