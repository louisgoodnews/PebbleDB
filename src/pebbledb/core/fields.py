"""
Author: Louis Goodnews
Date: 2025-09-13
"""

import json

from typing import Any, Callable, Final, Iterator, Literal, Optional, Self, Type
from uuid import UUID

from core.constants import (
    BOOLEAN,
    CUSTOM,
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
    REGEX,
    SET,
    STRING,
    TIME,
    TUPLE,
    UUID,
)

from utils.utils import analyze_typing


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
    "PebbleRegexField",
    "PebbleSetField",
    "PebbleStringField",
    "PebbleTimeField",
    "PebbleTupleField",
    "PebbleUUIDField",
    "PebbleFieldFactory",
    "PebbleFieldBuilder",
]

from datautils import DataIdentificationUtils


class PebbleField:
    """
    A base class for all Pebble fields.
    """

    default: Optional[Any] = None

    name: str

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

        # Initialize the fields dictionary
        fields: dict[str, Any] = self.__field_definitions__ | kwargs

        # Iterate over the field field type pairs in the annotations
        for (
            key,
            value,
        ) in fields.items():
            # Check if the current field is contained in the keyword arguments
            if key in kwargs:
                # Get the value corresponding to the current field
                value = kwargs.get(key, MISSING)

                # Get the field type corresponding to the current field
                field_type: Type[Any] = value.__class__
            else:
                # Get the default value corresponding to the current field
                value = self.__field_definitions__.get(key, MISSING)

                # Get the field type corresponding to the current field
                field_type: Type[Any] = value[0]

                # Get the value corresponding to the current field
                value = value[1]

                # Analyze the field type in order to process typing-Module annotations
                field_type = analyze_typing(typing=field_type)

                print(field_type)

            # Check if the current field is missing (i.e. the generic missing value)
            if value is MISSING:
                # Raise a ValueError over the missing field
                raise ValueError(f"Missing required field: {key}")

            # Check if the current field's type corresponds to the current field type
            if not isinstance(
                value,
                field_type,
            ):
                # Raise a TypeError if the actual type does not match the annotated one
                raise TypeError(
                    f"Field '{key}' expected {field_type}, got '{value}' ({type(value)}) instead",
                )

            # Set the current key value pair as attributes of this instance
            setattr(
                self,
                f"_{key}",
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

        def make_property(
            field: str,
            field_type: Type[Any],
            default: Any,
        ) -> property:
            """
            Make a property.

            Args:
                default (Any): The default value of the field.
                field (str): The field to make a property for.
                field_type (Type): The type of the field.

            Returns:
                property: The property.
            """

            # Analyze the field type in order to process typing-Module annotations
            expected_type: Type = analyze_typing(typing=field_type)

            def deleter(
                self,
                key: str = field,
                default: Optional[Any] = default,
            ) -> None:
                """
                Delete the value associated with the passed key (i.e. the field).

                Args:
                    key (str, optional): The key to delete. Defaults to field.

                Returns:
                    None
                """

                # Check if the default value is not None and not MISSING
                if default is not None and default is not MISSING:
                    # Set the default value
                    setattr(
                        self,
                        f"_{key}",
                        default,
                    )

                    # Return
                    return

                # Delete the value associated with the passed key (i.e. the field)
                del self.__dict__[f"_{key}"]

            def getter(
                self,
                key: str = field,
                default=default,
            ) -> Any:
                """
                Return the value associated with the passed key (i.e. the field).

                Args:
                    key (str, optional): The key to retrieve. Defaults to field.

                Returns:
                    Any: The value associated with the passed key.
                """

                # Return the value associated with the passed key (i.e. the field)
                return self.__dict__.get(
                    f"_{key}",
                    default,
                )

            def setter(
                self,
                value: Any,
                key: str = field,
                type_: Type = expected_type,
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
                    raise TypeError(
                        f"Field {key} expected {type_}, got '{value}' ({type(value)}) instead",
                    )

                # Set the current key value pair as attributes of this instance
                setattr(
                    self,
                    f"_{key}",
                    value,
                )

            # Return the getter and setter as a property
            return property(
                fdel=deleter,
                fget=getter,
                fset=setter,
            )

        # Call the parent class' __init_subclass__ method
        super().__init_subclass__()

        # Initialize the field definitions dictionary
        cls.__field_definitions__: dict[str, tuple[Type[Any], Any]] = {}

        # Initialize the meta definitions dictionary
        cls.__meta_definitions__: dict[str, tuple[Type[Any], Any]] = {}

        # Iterate over the Parent classes
        for cls_ in reversed(cls.__mro__):
            # Check, if the current class has no annotations
            if not hasattr(
                cls_,
                "__annotations__",
            ):
                # Skip the current iteration
                continue

            # Iterate over the field field type pairs in the annotations
            for (
                field,
                field_type,
            ) in cls_.__annotations__.items():

                # Get the default value of the field
                default: Any = getattr(
                    cls,
                    field,
                    MISSING,
                )

                # Check if the current field is a private field
                if field.startswith("_"):
                    # Assuming the current field is meta field
                    cls.__meta_definitions__[field] = (
                        field_type,
                        default,
                    )

                    # Skip the current field
                    continue

                # Add the field and its type to the field definitions dictionary
                cls.__field_definitions__[field] = (
                    field_type,
                    default,
                )

                # Append the property to the subclass
                setattr(
                    cls,
                    field,
                    make_property(
                        default=default,
                        field=field,
                        field_type=field_type,
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
        return f"<{self.__class__.__name__}({', '.join(f'{key.lstrip("_")}={value}' for key, value in self.__dict__.items())})>"

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

    def validate(
        self,
        value: Any,
    ) -> bool:
        """
        Validate a value based on the field type.

        Args:
            value (Any): The value to validate.

        Returns:
            bool: True if the value is valid, False otherwise.

        Raises:
            KeyError: If the field type is not supported.
        """

        # Define the validators dictionary
        validators: dict[str, Callable[[Any], bool]] = {
            "boolean": DataIdentificationUtils.is_bool,
            "date": DataIdentificationUtils.is_date,
            "datetime": DataIdentificationUtils.is_datetime,
            "decimal": DataIdentificationUtils.is_decimal,
            "dictionary": DataIdentificationUtils.is_dict,
            "float": DataIdentificationUtils.is_float,
            "frozenset": DataIdentificationUtils.is_frozenset,
            "integer": DataIdentificationUtils.is_int,
            "list": DataIdentificationUtils.is_list,
            "nullable": DataIdentificationUtils.is_none,
            "set": DataIdentificationUtils.is_set,
            "string": DataIdentificationUtils.is_str,
            "tuple": DataIdentificationUtils.is_tuple,
            "uuid": DataIdentificationUtils.is_uuid,
        }

        # Return True if the passed value could be validated else False
        return validators[self._field_type](value=value)

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


class PebbleCustomField(PebbleField):
    """ """

    # Define the field type as a final literal (i.e. the field type cannot be changed)
    _field_type: Final[Literal["custom"]] = CUSTOM


class PebbleDateField(PebbleField):
    """ """

    # Define the field type as a final literal (i.e. the field type cannot be changed)
    _field_type: Final[Literal["date"]] = DATE


class PebbleDateTimeField(PebbleField):
    """ """

    # Define the field type as a final literal (i.e. the field type cannot be changed)
    _field_type: Final[Literal["datetime"]] = DATETIME


class PebbleDecimalField(PebbleField):
    """ """

    # Define the field type as a final literal (i.e. the field type cannot be changed)
    _field_type: Final[Literal["decimal"]] = DECIMAL


class PebbleDictionaryField(PebbleField):
    """ """

    # Define the field type as a final literal (i.e. the field type cannot be changed)
    _field_type: Final[Literal["dictionary"]] = DICTIONARY


class PebbleFloatField(PebbleField):
    """ """

    # Define the field type as a final literal (i.e. the field type cannot be changed)
    _field_type: Final[Literal["float"]] = FLOAT


class PebbleFrozendictField(PebbleField):
    """ """

    # Define the field type as a final literal (i.e. the field type cannot be changed)
    _field_type: Final[Literal["frozendict"]] = FROZENDICT


class PebbleFrozensetField(PebbleField):
    """ """

    # Define the field type as a final literal (i.e. the field type cannot be changed)
    _field_type: Final[Literal["frozenset"]] = FROZENSET


class PebbleIntegerField(PebbleField):
    """ """

    # Define the field type as a final literal (i.e. the field type cannot be changed)
    _field_type: Final[Literal["integer"]] = INTEGER


class PebbleListField(PebbleField):
    """ """

    # Define the field type as a final literal (i.e. the field type cannot be changed)
    _field_type: Final[Literal["list"]] = LIST


class PebbleNullField(PebbleField):
    """ """

    # Define the field type as a final literal (i.e. the field type cannot be changed)
    _field_type: Final[Literal["null"]] = NULL


class PebblePathField(PebbleField):
    """ """

    # Define the field type as a final literal (i.e. the field type cannot be changed)
    _field_type: Final[Literal["path"]] = PATH


class PebbleRegexField(PebbleField):
    """ """

    # Define the field type as a final literal (i.e. the field type cannot be changed)
    _field_type: Final[Literal["regex"]] = REGEX


class PebbleSetField(PebbleField):
    """ """

    # Define the field type as a final literal (i.e. the field type cannot be changed)
    _field_type: Final[Literal["set"]] = SET


class PebbleStringField(PebbleField):
    """ """

    # Define the field type as a final literal (i.e. the field type cannot be changed)
    _field_type: Final[Literal["string"]] = STRING


class PebbleTimeField(PebbleField):
    """ """

    # Define the field type as a final literal (i.e. the field type cannot be changed)
    _field_type: Final[Literal["time"]] = TIME


class PebbleTupleField(PebbleField):
    """ """

    # Define the field type as a final literal (i.e. the field type cannot be changed)
    _field_type: Final[Literal["tuple"]] = TUPLE


class PebbleUUIDField(PebbleField):
    """ """

    # Define the field type as a final literal (i.e. the field type cannot be changed)
    _field_type: Final[Literal["uuid"]] = UUID


class PebbleFieldFactory:
    """ """

    @classmethod
    def create(
        cls,
        field_type: Literal[
            "boolean",
            "date",
            "datetime",
            "decimal",
            "dictionary",
            "float",
            "frozenset",
            "integer",
            "list",
            "nullable",
            "regex",
            "set",
            "string",
            "tuple",
            "uuid",
        ],
        name: str,
    ) -> PebbleField:
        """
        Return a new instance of the PebbleField class.

        Args:
            field_type (Literal[
                "boolean",
                "date",
                "datetime",
                "decimal",
                "dictionary",
                "float",
                "frozenset",
                "integer",
                "list",
                "nullable",
                "regex",
                "set",
                "string",
                "tuple",
                "uuid",
            ]): The type of the field.
            name (str): The name of the field.

        Returns:
            PebbleField: A new instance of the PebbleField class.
        """

        # Define a dictionary of field types and their corresponding create methods
        create_: dict[str, Callable[[str], PebbleField]] = {
            "boolean": cls.create_boolean_field,
            "date": cls.create_date_field,
            "datetime": cls.create_datetime_field,
            "decimal": cls.create_decimal_field,
            "dictionary": cls.create_dictionary_field,
            "float": cls.create_float_field,
            "frozenset": cls.create_frozenset_field,
            "integer": cls.create_integer_field,
            "list": cls.create_list_field,
            "nullable": cls.create_null_field,
            "regex": cls.create_regex_field,
            "set": cls.create_set_field,
            "string": cls.create_string_field,
            "tuple": cls.create_tuple_field,
            "uuid": cls.create_uuid_field,
        }

        # Check if the field type is valid
        if field_type not in create_:
            # Raise a ValueError exception
            raise ValueError(f"Invalid field type: {field_type}")

        # Return a new instance of the PebbleField class
        return create_[field_type](name=name)

    @classmethod
    def create_boolean_field(
        cls,
        name: str,
    ) -> PebbleBooleanField:
        """
        Return a new instance of the PebbleBooleanField class.

        Args:
            name (str): The name of the field.

        Returns:
            PebbleBooleanField: A new instance of the PebbleBooleanField class.
        """

        # Return a new instance of the PebbleBooleanField class
        return PebbleBooleanField(name=name)

    @classmethod
    def create_date_field(
        cls,
        name: str,
    ) -> PebbleDateField:
        """
        Return a new instance of the PebbleDateField class.

        Args:
            name (str): The name of the field.

        Returns:
            PebbleDateField: A new instance of the PebbleDateField class.
        """

        # Return a new instance of the PebbleDateField class
        return PebbleDateField(name=name)

    @classmethod
    def create_datetime_field(
        cls,
        name: str,
    ) -> PebbleDateTimeField:
        """
        Return a new instance of the PebbleDateTimeField class.

        Args:
            name (str): The name of the field.

        Returns:
            PebbleDateTimeField: A new instance of the PebbleDateTimeField class.
        """

        # Return a new instance of the PebbleDateTimeField class
        return PebbleDateTimeField(name=name)

    @classmethod
    def create_decimal_field(
        cls,
        name: str,
    ) -> PebbleDecimalField:
        """
        Return a new instance of the PebbleDecimalField class.

        Args:
            name (str): The name of the field.

        Returns:
            PebbleDecimalField: A new instance of the PebbleDecimalField class.
        """

        # Return a new instance of the PebbleDecimalField class
        return PebbleDecimalField(name=name)

    @classmethod
    def create_dictionary_field(
        cls,
        name: str,
    ) -> PebbleDictionaryField:
        """
        Return a new instance of the PebbleDictionaryField class.

        Args:
            name (str): The name of the field.

        Returns:
            PebbleDictionaryField: A new instance of the PebbleDictionaryField class.
        """

        # Return a new instance of the PebbleDictionaryField class
        return PebbleDictionaryField(name=name)

    @classmethod
    def create_float_field(
        cls,
        name: str,
    ) -> PebbleFloatField:
        """
        Return a new instance of the PebbleFloatField class.

        Args:
            name (str): The name of the field.

        Returns:
            PebbleFloatField: A new instance of the PebbleFloatField class.
        """

        # Return a new instance of the PebbleFloatField class
        return PebbleFloatField(name=name)

    @classmethod
    def create_frozenset_field(
        cls,
        name: str,
    ) -> PebbleFrozensetField:
        """
        Return a new instance of the PebbleFrozensetField class.

        Args:
            name (str): The name of the field.

        Returns:
            PebbleFrozensetField: A new instance of the PebbleFrozensetField class.
        """

        # Return a new instance of the PebbleFrozensetField class
        return PebbleFrozensetField(name=name)

    @classmethod
    def create_integer_field(
        cls,
        name: str,
    ) -> PebbleIntegerField:
        """
        Return a new instance of the PebbleIntegerField class.

        Args:
            name (str): The name of the field.

        Returns:
            PebbleIntegerField: A new instance of the PebbleIntegerField class.
        """

        # Return a new instance of the PebbleIntegerField class
        return PebbleIntegerField(name=name)

    @classmethod
    def create_list_field(
        cls,
        name: str,
    ) -> PebbleListField:
        """
        Return a new instance of the PebbleListField class.

        Args:
            name (str): The name of the field.

        Returns:
            PebbleListField: A new instance of the PebbleListField class.
        """

        # Return a new instance of the PebbleListField class
        return PebbleListField(name=name)

    @classmethod
    def create_null_field(
        cls,
        name: str,
    ) -> PebbleNullField:
        """
        Return a new instance of the PebbleNullField class.

        Args:
            name (str): The name of the field.

        Returns:
            PebbleNullField: A new instance of the PebbleNullField class.
        """

        # Return a new instance of the PebbleNullField class
        return PebbleNullField(name=name)

    @classmethod
    def create_path_field(
        cls,
        name: str,
    ) -> PebblePathField:
        """
        Return a new instance of the PebblePathField class.

        Args:
            name (str): The name of the field.

        Returns:
            PebblePathField: A new instance of the PebblePathField class.
        """

        # Return a new instance of the PebblePathField class
        return PebblePathField(name=name)

    @classmethod
    def create_regex_field(
        cls,
        name: str,
    ) -> PebbleRegexField:
        """
        Return a new instance of the PebbleRegexField class.

        Args:
            name (str): The name of the field.

        Returns:
            PebbleRegexField: A new instance of the PebbleRegexField class.
        """

        # Return a new instance of the PebbleRegexField class
        return PebbleRegexField(name=name)

    @classmethod
    def create_set_field(
        cls,
        name: str,
    ) -> PebbleSetField:
        """
        Return a new instance of the PebbleSetField class.

        Args:
            name (str): The name of the field.

        Returns:
            PebbleSetField: A new instance of the PebbleSetField class.
        """

        # Return a new instance of the PebbleSetField class
        return PebbleSetField(name=name)

    @classmethod
    def create_string_field(
        cls,
        name: str,
    ) -> PebbleStringField:
        """
        Return a new instance of the PebbleStringField class.

        Args:
            name (str): The name of the field.

        Returns:
            PebbleStringField: A new instance of the PebbleStringField class.
        """

        # Return a new instance of the PebbleStringField class
        return PebbleStringField(name=name)

    @classmethod
    def create_time_field(
        cls,
        name: str,
    ) -> PebbleTimeField:
        """
        Return a new instance of the PebbleTimeField class.

        Args:
            name (str): The name of the field.

        Returns:
            PebbleTimeField: A new instance of the PebbleTimeField class.
        """

        # Return a new instance of the PebbleTimeField class
        return PebbleTimeField(name=name)

    @classmethod
    def create_tuple_field(
        cls,
        name: str,
    ) -> PebbleTupleField:
        """
        Return a new instance of the PebbleTupleField class.

        Args:
            name (str): The name of the field.

        Returns:
            PebbleTupleField: A new instance of the PebbleTupleField class.
        """

        # Return a new instance of the PebbleTupleField class
        return PebbleTupleField(name=name)

    @classmethod
    def create_uuid_field(
        cls,
        name: str,
    ) -> PebbleUUIDField:
        """
        Return a new instance of the PebbleUUIDField class.

        Args:
            name (str): The name of the field.

        Returns:
            PebbleUUIDField: A new instance of the PebbleUUIDField class.
        """

        # Return a new instance of the PebbleUUIDField class
        return PebbleUUIDField(name=name)


class PebbleFieldBuilder:
    """ """

    def __init__(self) -> None:
        """
        Initialize the PebbleFieldBuilder instance with an empty configuration dictionary instance variable.

        Returns:
            None
        """

        # Initialize the configuration dictionary instance variable
        self._configuration: dict[str, Any] = {}

    def __contains__(
        self,
        key: str,
    ) -> None:
        """
        Check if the passed key is contained in the configuration dictionary instance variable.

        Args:
            key (str): The key to be checked.

        Returns:
            bool: True if the key is contained in the configuration dictionary instance variable, False otherwise.
        """

        # Check if the passed key is contained in the configuration dictionary instance variable
        return key in self._configuration

    def __eq__(
        self,
        other: "PebbleFieldBuilder",
    ) -> bool:
        """
        Check if the passed other object is equal to the PebbleFieldBuilder instance.

        Args:
            other (PebbleFieldBuilder): The other object to be checked.

        Returns:
            bool: True if the passed other object is equal to the PebbleFieldBuilder instance, False otherwise.
        """

        # Check if the passed other object is not a PebbleFieldBuilder instance
        if not isinstance(
            other,
            PebbleFieldBuilder,
        ):
            # Return False as a comparison between non-identical classes is not supported
            return False

        # Return True if the configuration dictionary instance variables of the two PebbleFieldBuilder instance are equal otherwise False
        return self.configuration == other.configuration

    def __getitem__(
        self,
        key: str,
    ) -> Any:
        """
        Return the value associated with the passed key.
        Will raise a KeyError exception is the key does not exist.

        Args:
            key (str): The key to be checked.

        Returns:
            Any: The value associated with the passed key.
        """

        # Return the value associated with the passed key.
        # Will raise a KeyError exception is the key does not exist
        return self._configuration[key]

    def __iter__(self) -> Iterator[Any]:
        """
        Return an iterator over the configuration dictionary instance variable.

        Returns:
            Iterator[Any]: An iterator over the configuration dictionary instance variable.
        """

        # Return an iterator over the configuration dictionary instance variable
        return iter(self._configuration)

    def __len__(self) -> int:
        """
        Return the size of the configuration dictionary instance variable.

        Returns:
            int: The size of the configuration dictionary instance variable.
        """

        # Return the size of the configuration dictionary instance variable
        return len(self._configuration)

    def __repr__(self) -> str:
        """
        Return a string representation of the PebbleTableBuilder instance.

        Returns:
            str: A string representation of the PebbleTableBuilder instance.
        """

        # Return a string representation of the PebbleTableBuilder instance
        return f"<{self.__class__.__name__}(configuration={self.configuration})>"

    def __setitem__(
        self,
        key: str,
        value: Any,
    ) -> Any:
        """
        Update the configuration dictionary instance variable with the passed value associated to the passed key.

        Args:
            key (str): The key to be checked.
            value (Any): The value to be associated with the passed key.

        Returns:
            Any: The value associated with the passed key.
        """

        # Update the configuration dictionary instance variable with the passed value associated to the passed key
        self._configuration[key] = value

    def __str__(self) -> str:
        """
        Return a string representation of the configuration dictionary instance variable.

        Returns:
            str: A string representation of the configuration dictionary instance variable.
        """

        # Return a string representation of the configuration dictionary instance variable
        return str(self._configuration)

    def build(self) -> PebbleField:
        """
        Build a new instance of the PebbleField class.

        Returns:
            PebbleField: A new instance of the PebbleField class.
        """

        # Return a new instance of the PebbleField class
        return PebbleFieldFactory.create(**self._configuration)

    def with_field_type(
        self,
        value: Literal[
            "boolean",
            "date",
            "datetime",
            "decimal",
            "double",
            "float",
            "integer",
            "null",
            "path",
            "set",
            "string",
            "time",
            "tuple",
            "uuid",
        ],
    ) -> Self:
        """
        Set the field type of the field to be built.

        Args:
            value (Literal): The field type of the field to be built.

        Returns:
            Self: The current instance of the PebbleFieldBuilder class.
        """

        # Set the field type of the field to be built
        self._configuration["field_type"] = value

        # Return the current instance of the PebbleFieldBuilder class
        return self

    def with_name(
        self,
        value: str,
    ) -> Self:
        """
        Set the name of the field to be built.

        Args:
            value (str): The name of the field to be built.

        Returns:
            Self: The current instance of the PebbleFieldBuilder class.
        """

        # Set the name of the field to be built
        self._configuration["name"] = value

        # Return the current instance of the PebbleFieldBuilder class
        return self
