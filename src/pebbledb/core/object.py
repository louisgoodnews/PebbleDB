"""
Author: Louis Goodnews
Date: 2025-09-20
"""

from typing import Any, Final, TypeVar

from core.constants import MISSING


__all__: Final[list[str]] = ["PebbleObject"]


T = TypeVar("T")


class PebbleObject:
    """ """

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
        Return a string representation of the PebbleObject instance.

        Returns:
            str: A string representation of the PebbleObject instance.
        """

        # Return a string representation of the PebbleObject instance
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
        Return a string representation of the PebbleObject instance.

        Returns:
            str: A string representation of the PebbleObject instance.
        """

        # Return a string representation of the PebbleObject instance
        return self.__repr__()

    def delete(self) -> None:
        """
        Delete the PebbleObject instance from a file.

        Args:
            None

        Returns:
            None
        """

        pass

    @classmethod
    def load(
        cls,
        identifier: str,
    ) -> "PebbleObject":
        """
        Load the PebbleObject instance from a file.

        Args:
            identifier (str): The identifier of the object to load.

        Returns:
            PebbleObject: The loaded PebbleObject instance.
        """

        pass

    def save(self) -> None:
        """
        Save the PebbleObject instance to a file.

        Args:
            None

        Returns:
            None
        """

        pass

    def to_dict(self) -> dict[str, Any]:
        """
        Return a dictionary representation of the PebbleObject instance.

        Returns:
            dict[str, Any]: A dictionary representation of the PebbleObject instance.
        """

        # Return a dictionary representation of the PebbleObject instance
        return self.__dict__.copy()

    def update(self) -> None:
        """
        Update the PebbleObject instance.

        Args:
            None

        Returns:
            None
        """

        pass
