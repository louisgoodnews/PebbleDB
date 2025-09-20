"""
Author: Louis Goodnews
Date: 2025-09-13
"""

import uuid

from collections.abc import ItemsView, KeysView, ValuesView
from datetime import datetime
from pathlib import Path
from typing import Any, Final, Iterable, Iterator, Optional, Self, Union

from core.constants import CWD, PEBBLE_COMMIT_SERVICE
from core.files import read_file_if_not_exists
from core.table import PebbleTable, PebbleTableBuilder

from utils.utils import run_async

from datautils import DataConversionUtils
from logger import Logger


__all__: Final[list[str]] = [
    "PebbleDatabase",
    "PebbleDatabaseFactory",
    "PebbleDatabaseBuilder",
    "PebbleDatabaseLoader",
]


class PebbleDatabase:
    """
    A class that represents a table in a database.
    """

    def __init__(
        self,
        data: dict[str, Any],
        identifier: str,
        name: str,
        path: Path,
        created_at: Optional[datetime] = None,
        metadata: Optional[dict[str, Any]] = None,
        updated_at: Optional[datetime] = None,
    ) -> None:
        """
        Initialize the PebbleDatabase instance with the passed data dictionary, identifier string, and name string.

        Args:
            created_at (Optional[datetime]): The created at datetime to be stored in the PebbleDatabase instance.
            data (dict[str, Any]): The data dictionary to be stored in the PebbleDatabase instance.
            identifier (str): The identifier string to be stored in the PebbleDatabase instance.
            metadata (Optional[dict[str, Any]]): The metadata dictionary to be stored in the PebbleDatabase instance.
            name (str): The name string to be stored in the PebbleDatabase instance.
            path (Path): The path to the PebbleDatabase instance.
            updated_at (Optional[datetime]): The updated at datetime to be stored in the PebbleDatabase instance.

        Returns:
            None
        """

        # Check if the passed created_at value is None
        if created_at is None:
            # Update the created_at value with the current datetime
            created_at = datetime.now()

        # Set the '_created_at' date to the passed value or now
        self._created_at: Final[datetime] = created_at

        # Store the passed data dictionary in a final instance variable
        self._data: Final[dict[str, Any]] = data

        # Storet the passed identifier string in a final instance variable
        self._identifier: Final[str] = identifier

        # Initialize the Logger instance
        self._logger: Logger = Logger(name=self.__class__.__name__)

        # Check if the passed metadata is None
        if metadata is None:
            # Update the metadata with an empty dictionary
            metadata = {}

        # Store the passed metadata dictionary in a final instance variable
        self._metadata: Final[dict[str, Any]] = metadata

        # Store the passed name string in a final instance variable
        self._name: Final[str] = name

        # Store the passed path Path object in a final instance variable
        self._path: Final[Path] = path

        # Set the '_updated_at' date to the passed value or now
        self._updated_at: datetime = updated_at or datetime.now()

    def __contains__(
        self,
        key: str,
    ) -> bool:
        """
        Check if the passed key is contained in the data dictionary instance variable.

        Args:
            key (str): The key to be checked.

        Returns:
            bool: True if the key is contained in the data dictionary instance variable, False otherwise.
        """

        # Return True if the passed key is contained in the data dictionary instance variable
        return key in self._data["entries"]["values"]

    def __eq__(
        self,
        other: "PebbleDatabase",
    ) -> bool:
        """
        Check if the passed other object is not a PebbleDatabase instance

        Args:
            other (PebbleDatabase): The other object to be compared.

        Returns:
            bool: True if the passed other object is a PebbleDatabase instance and its identifier is identical to this instance's identifier, False otherwise.
        """

        # Check if the passed other object is not a PebbleDatabase instance
        if not isinstance(
            other,
            PebbleDatabase,
        ):
            # Return False as a comparison between non-identical classes is not supported
            return False

        # Return True if this and the other instance's identifiers are identical
        return self.identifier == other.identifier

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

        Raises:
            KeyError: If the passed key does not exist in the data dictionary instance variable.
        """

        # Return the value associated with the passed key.
        # Will raise a KeyError exception is the key does not exist
        return self._data["entries"]["values"][key]

    def __iter__(self) -> Iterable[Any]:
        """
        Return an iterator over the copy of the data dictionary instance variable.

        Returns:
            Iterable[Any]: An iterator over the copy of the data dictionary instance variable.
        """

        # Return an iterator over the copy of the data dictionary instance variable
        return iter(self._data["entries"]["values"].copy())

    def __len__(self) -> int:
        """
        Return the size of the data dictionary instance variable.

        Returns:
            int: The size of the data dictionary instance variable.
        """

        # Return the size of the data dictionary instance variable
        return len(self._data["entries"]["values"])

    def __repr__(self) -> str:
        """
        Return a string representation of this PebbleDatabase instance.

        Returns:
            str: A string representation of this PebbleDatabase instance.
        """

        # Return a string representation of this PebbleDatabase instance
        return f"<{self.__class__.__name__}(entries={self.total}, identifier={self.identifier}, metadata={self.metadata}, name={self.name}, path={self.path})>"

    def __setitem__(
        self,
        key: str,
        value: Any,
    ) -> Any:
        """
        Update the data dictionary instance variable with the passed value associated to the passed key.

        Args:
            key (str): The key to be checked.
            value (Any): The value to be associated with the passed key.

        Returns:
            Any: The value associated with the passed key.
        """

        # Update the data dictionary instance variable with the passed value associated to the passed key
        self._data["entries"]["values"][key] = value

    def __str__(self) -> str:
        """
        Return a string representation of the data dictionary instance variable.

        Returns:
            str: A string representation of the data dictionary instance variable.
        """

        # Return a string representation of the data dictionary instance variable
        return str(self._data)

    @property
    def created_at(self) -> datetime:
        """
        Return the created at datetime of the PebbleDatabase instance to the caller.

        Returns:
            datetime: The created at datetime of the PebbleDatabase instance to the caller.
        """

        # Return the created at datetime of the PebbleDatabase instance to the caller
        return self._created_at

    @property
    def entries(self) -> dict[str, Any]:
        """
        Return a copy of the dictionary to the caller.

        Returns:
            dict[str, Any]: A copy of the dictionary to the caller.
        """

        # Check if 'entries' exists in the data dictionary instance variable
        if "entries" not in self._data:
            # Initialize the 'entries' dictionary to a dictionary with a 'total' key and a 'values' key
            self._data["entries"] = {
                "total": 0,
                "values": {},
            }

        # Return a copy of the dictionary to the caller
        return self._data["entries"]["values"].copy()

    @property
    def identifier(self) -> str:
        """
        Return the identifier of the PebbleDatabase instance to the caller.

        Returns:
            str: The identifier of the PebbleDatabase instance to the caller.
        """

        # Return the identifier of the PebbleDatabase instance to the caller
        return self._identifier

    @property
    def metadata(self) -> dict[str, Any]:
        """
        Return a copy of the metadata dictionary instance variable to the caller.

        Returns:
            dict[str, Any]: A copy of the metadata dictionary instance variable to the caller.
        """

        # Return a copy of the metadata dictionary instance variable to the caller
        return self._metadata.copy()

    @metadata.setter
    def metadata(
        self,
        **kwargs,
    ) -> None:
        """
        Update the metadata dictionary instance variable with the passed value.

        Args:
            **kwargs (dict[str, Any]): The key-value pairs to update the metadata with.

        Returns:
            None
        """

        # Update the metadata dictionary instance variable with the passed value
        self._metadata.update(kwargs)

    @property
    def name(self) -> str:
        """
        Return the name of the PebbleDatabase instance to the caller.

        Returns:
            str: The name of the PebbleDatabase instance to the caller.
        """

        # Return the name of the PebbleDatabase instance to the caller
        return self._name

    @property
    def path(self) -> Path:
        """
        Return the path of the PebbleDatabase instance to the caller.

        Returns:
            Path: The path of the PebbleDatabase instance to the caller.
        """

        # Return the path of the PebbleDatabase instance to the caller
        return self._path

    @property
    def total(self) -> int:
        """
        Return the total count to the caller.

        Returns:
            int: The total count to the caller.
        """

        # Check if 'entries' exists in the data dictionary instance variable
        if "entries" not in self._data:
            # Initialize the 'entries' dictionary to a dictionary with a 'total' key and a 'values' key
            self._data["entries"] = {
                "total": 0,
                "values": {},
            }

        # Check if 'total' exists in the data dictionary instance variable
        if "total" not in self._data["entries"]:
            # Initialize the 'total' count to 0
            self._data["entries"]["total"] = 0
        else:
            # Update the 'total' count to the size of the 'values' dictionary
            self._data["entries"]["total"] = len(self._data["entries"]["values"])

        # Return the total count to the caller
        return self._data["entries"]["total"]

    @total.setter
    def total(
        self,
        value: int,
    ) -> None:
        """
        Update the total count with the passed value.

        Args:
            value (int): The value to be associated with the passed key.

        Returns:
            None
        """

        # Check if 'entries' exists in the data dictionary instance variable
        if "entries" not in self._data:
            # Initialize the 'entries' dictionary to a dictionary with a 'total' key and a 'values' key
            self._data["entries"] = {
                "total": 0,
                "values": {},
            }

        # Check if 'total' exists in the data dictionary instance variable
        if "total" not in self._data["entries"]:
            # Initialize the 'total' count to 0
            self._data["entries"]["total"] = 0

        # Update the total count with the passed value
        self._data["entries"]["total"] = value

    @property
    def updated_at(self) -> datetime:
        """
        Return the updated at datetime of the PebbleDatabase instance to the caller.

        Returns:
            datetime: The updated at datetime of the PebbleDatabase instance to the caller.
        """

        # Return the updated at datetime of the PebbleDatabase instance to the caller
        return self._updated_at

    @updated_at.setter
    def updated_at(
        self,
        value: datetime,
    ) -> None:
        """
        Update the updated at datetime of the PebbleDatabase instance with the passed value.

        Args:
            value (datetime): The value to be associated with the passed key.

        Returns:
            None
        """

        # Update the updated at datetime of the PebbleDatabase instance with the passed value
        self._updated_at = value

    def _get(
        self,
        identifier: str,
    ) -> Any:
        """
        Return the value associated with the passed key.
        Will raise a KeyError exception is the key does not exist.

        Args:
            identifier (str): The identifier to be checked.

        Returns:
            Any: The value associated with the passed key.
        """

        # Check if 'values' exists in the data dictionary instance variable
        if "values" not in self._data:
            # Initialize the 'values' dictionary to an empty dictionary
            self._data["entries"]["values"] = {}

        # Return the value associated with the passed key.
        # Will raise a KeyError exception is the key does not exist
        return self._data["entries"]["values"][identifier]

    def _get_in_bulk(
        self,
        identifiers: list[str],
    ) -> list[Any]:
        """
        Return the values associated with the passed identifiers.
        Will raise a KeyError exception is the key does not exist.

        Args:
            identifiers (list[str]): The identifiers to be checked.

        Returns:
            list[Any]: The values associated with the passed identifiers.
        """

        # Initialize the result to an empty list
        result: list[Any] = []

        # Initialize the errors list to an empty list
        errors: list[KeyError] = []

        # Check if 'values' exists in the data dictionary instance variable
        if "values" not in self._data["entries"]:
            # Initialize the 'values' dictionary to an empty dictionary
            self._data["entries"]["values"] = {}

        # Iterate over the passed idenfifiers
        for identifier in identifiers:
            try:
                # Attempt to append the value associated to the current identifier
                result.append(self._data["entries"]["values"][identifier])
            except KeyError as e:
                # Append the excepted KeyError exception to the errors list
                errors.append(e)

        # Check if the errors list is not empty
        if errors:
            # Raise a sinlge KeyError exception with all missing keys
            raise KeyError(*errors)

        # Return the result list to the caller
        return result

    def _insert(
        self,
        entry: dict[str, Any],
        is_bulk_operation: bool = False,
        timestamp: Optional[datetime] = None,
    ) -> int:
        """
        Insert the passed entry dictionary into the data dictionary instance variable.

        Args:
            entry (dict[str, Any]): The entry dictionary to be inserted.

        Returns:
            int: The identifier of the inserted entry.
        """

        # Check if 'entries' exists in the data dictionary instance variable
        if "entries" not in self._data:
            # Initialize the 'entries' dictionary to a dictionary with a 'total' key and a 'values' key
            self._data["entries"] = {
                "total": 0,
                "values": {},
            }

        # Get the current timestamp if the passed timestamp is None
        timestamp: datetime = timestamp or datetime.now()

        # Get the identifier that the passed entry shuld be associated with
        identifier: str = str(self.total)

        # Set the '_added_at' date to now
        entry["_added_at"] = timestamp.isoformat()

        # Check if 'values' exists in the data dictionary instance variable
        if "values" not in self._data["entries"]:
            # Initialize the 'values' dictionary to an empty dictionary
            self._data["entries"]["values"] = {}

        # Add the passed entry dictionary to the data dictionary instance variable
        self._data["entries"]["values"][identifier] = entry

        # Update the total count of the data dictionary instance variable
        self.total = self.total + 1

        # Check if the operation is not a bulk operation
        if not is_bulk_operation:
            # Update the updated at datetime of the PebbleDatabase instance with the passed value
            self.updated_at = timestamp

        # Return the identifier converted to an integer
        return int(identifier)

    def _insert_in_bulk(
        self,
        entries: list[dict[str, Any]],
    ) -> list[int]:
        """
        Insert the passed entries list into the data dictionary instance variable.

        Args:
            entries (list[dict[str, Any]]): The entries list to be inserted.

        Returns:
            list[int]: The identifiers of the inserted entries.
        """

        # Get the current timestamp
        timestamp: datetime = datetime.now()

        # Initialize the result to an empty list
        result: list[int] = []

        # Iterate over the passed entries
        for entry in entries:
            # Insert the current entry into the data dictionary instance variable
            result.append(self._insert(entry=entry, is_bulk_operation=True, timestamp=timestamp))

        # Update the updated at datetime of the PebbleDatabase instance with the passed value
        self.updated_at = timestamp

        # Return the result list to the caller
        return result

    def add_table(
        self,
        table: PebbleTable,
    ) -> int:
        """
        Add the passed table to the database.

        Args:
            table (PebbleTable): The table to be added.

        Returns:
            int: The identifier of the added table.
        """

        # Insert the table data into the data dictionary instance variable and return the entry's ID
        return self._insert(
            entry={
                "identifier": table.identifier,
                "name": table.name,
                "path": table.path,
            }
        )

    def add_tables(
        self,
        tables: list[PebbleTable],
    ) -> list[int]:
        """
        Add the passed tables to the database.

        Args:
            tables (list[PebbleTable]): The tables to be added.

        Returns:
            list[int]: The identifiers of the added tables.
        """

        # Get the current timestamp
        timestamp: str = DateUtil.now().isoformat()

        # Insert the table data into the data dictionary instance variable and return the entry's IDs
        return self._insert_in_bulk(
            entries=[
                {
                    "added_at": timestamp,
                    "identifier": table.identifier,
                    "name": table.name,
                    "path": table.path,
                }
                for table in tables
            ]
        )

    def all(self) -> list[dict[str, Any]]:
        """
        Return a list of the values contained in this PebbleDatabase instance.

        Returns:
            list[dict[str, Any]]: A list of the values contained in this PebbleDatabase instance.
        """

        # Return a list of the values contained in this PebbleDatabase instance
        return list(self.entries.values())

    def commit(self) -> None:
        """
        Commit the changes to the database.

        Returns:
            None
        """

        # Attempt to commit the database to a file
        PEBBLE_COMMIT_SERVICE.commit(database_or_table=self.to_dict())

    def create_table(
        self,
        data: dict[str, Any],
        name: str,
        identifier: Optional[str] = None,
        path: Optional[Path] = None,
    ) -> PebbleTable:
        """
        Create a new PebbleTable instance with the passed data dictionary, name string, and identifier string.

        This method will create a new PebbleTable instance and add it to the database.

        Args:
            data (dict[str, Any]): The data dictionary to be stored in the PebbleTable instance.
            identifier (Optional[str], optional): The identifier string to be stored in the PebbleTable instance. Defaults to None.
            name (str): The name string to be stored in the PebbleTable instance.
            path (Optional[Path], optional): The path to the PebbleTable instance. Defaults to None.

        Returns:
            PebbleTable: The newly created PebbleTable instance.
        """

        # Check if the passed identifier is None
        if identifier is None:
            # Update the identifier with a newly generated UUID
            identifier = uuid.uuid4().hex

        # Check if the passed identifier is None
        if path is None:
            # Update the identifier with a newly generated UUID
            path = CWD

        # Return the newly created PebbleTable instance to the caller
        table: PebbleTable = (
            PebbleTableBuilder()
            .with_data(value=data)
            .with_identifier(value=identifier)
            .with_name(value=name)
            .with_path(value=path)
            .build()
        )

        # Add the table to the database
        self.add_table(table=table)

        # Return the newly created PebbleTable instance to the caller
        return table

    def empty(self) -> bool:
        """
        Return True if the PebbleDatabase instance is empty otherwise False.

        Returns:
            bool: True if the PebbleDatabase instance is empty otherwise False.
        """

        # Return True if the PebbleDatabase instance is empty otherwise False
        return self.total == 0

    def get_metadata(
        self,
        key: str,
        default: Optional[Any] = None,
    ) -> Any:
        """
        Get the metadata associated with the passed key.

        Args:
            key (str): The key of the metadata to be fetched.
            default (Optional[Any], optional): The default value to be returned if the key is not found. Defaults to None.

        Returns:
            Any: The metadata associated with the passed key.
        """

        # Return the metadata associated with the passed key
        return self.metadata.get(
            key,
            default,
        )

    def get_table(
        self,
        identifier: int,
    ) -> PebbleTable:
        """
        Get the table associated with the passed identifier.

        Args:
            identifier (int): The identifier of the table to be fetched.

        Returns:
            PebbleTable: The table associated with the passed identifier.

        Raises:
            KeyError: If the table was not found.
        """

        # TODO:
        #   - implement loading the table file from disk if possible

        # Attempt to fetch the data associated with the passed identifier
        table: Optional[dict[str, Any]] = next(
            filter(
                lambda table: table["identifier"] == identifier,
                self.entries.values(),
            ),
            None,
        )

        # Check if the table was found
        if table is None:
            # Raise a KeyError exception if the table was not found
            raise KeyError(identifier)

        # Return the table associated with the passed identifier
        return (
            PebbleTableBuilder()
            .with_created_at(value=table.get("created_at", None))
            .with_data(value=table.get("data", {}))
            .with_database(value=self.name)
            .with_identifier(value=table.get("identifier", None))
            .with_metadata(value=table.get("metadata", {}))
            .with_name(value=table.get("name", None))
            .with_path(value=table.get("path", None))
            .with_updated_at(value=table.get("updated_at", None))
            .build()
        )

    def get_tables(
        self,
        identifiers: list[int],
    ) -> list[PebbleTable]:
        """
        Get the tables associated with the passed identifiers.

        Args:
            identifiers (list[int]): The identifiers of the tables to be fetched.

        Returns:
            list[PebbleTable]: The tables associated with the passed identifiers.

        Raises:
            KeyError: If the tables were not found.
        """

        # TODO:
        #   - implement loading the table file from disk if possible

        # Filter the entries to get the tables associated with the passed identifiers
        tables: list[dict[str, Any]] = list(
            filter(
                lambda table: table["identifier"] in identifiers,
                self.entries.values(),
            )
        )

        # Check if the tables were found
        if not tables:
            # Raise a KeyError exception if the tables were not found
            raise KeyError(identifiers)

        # Return the tables associated with the passed identifiers
        return [
            (
                PebbleTableBuilder()
                .with_created_at(value=table.get("created_at", None))
                .with_data(value=table.get("data", {}))
                .with_database(value=self.name)
                .with_identifier(value=table.get("identifier", None))
                .with_metadata(value=table.get("metadata", {}))
                .with_name(value=table.get("name", None))
                .with_path(value=table.get("path", None))
                .with_updated_at(value=table.get("updated_at", None))
                .build()
            )
            for table in tables
        ]

    def items(self) -> ItemsView[Any]:
        """
        Return the items of the PebbleDatabase's entries.

        Returns:
            ItemsView[Any]: The items of the PebbleDatabase's entries.
        """

        # Return the items of the PebbleDatabase's entries
        return self.entries.items()

    def keys(self) -> KeysView[Any]:
        """
        Return the keys of the PebbleDatabase's entries.

        Returns:
            KeysView[Any]: The keys of the PebbleDatabase's entries.
        """

        # Return the keys of the PebbleDatabase's entries
        return self.entries.keys()

    def remove(
        self,
        identifier: str,
        is_bulk_operation: bool = False,
        timestamp: Optional[datetime] = None,
    ) -> bool:
        """
        Remove the value associated with the passed identifier from the data dictionary instance variable.

        Args:
            identifier (str): The identifier to be removed.
            is_bulk_operation (bool, optional): Whether the removal is part of a bulk operation. Defaults to False.
            timestamp (Optional[datetime], optional): The timestamp to be associated with the removal. Defaults to None.

        Returns:
            bool: True if the value associated with the identifier was removed successfully otherwise False.
        """

        # Get the current timestamp if the passed timestamp is None
        timestamp: datetime = timestamp or datetime.now()

        # Set the result to True if the value associated with the identifier was removed successfully otherwise False
        result: bool = bool(self._data["entries"]["values"].pop(identifier, False))

        # Update the total count of the data dictionary instance variable
        self.total = self.total + 1

        # Check if the operation is not a bulk operation
        if not is_bulk_operation:
            # Update the updated at datetime of the PebbleDatabase instance with the passed value
            self.updated_at = timestamp

        # Return the result to the caller
        return result

    def remove_in_bulk(
        self,
        identifiers: list[str],
    ) -> bool:
        """
        Remove the values associated with the passed identifiers from the data dictionary instance variable.

        Args:
            identifiers (list[str]): The identifiers to be removed.

        Returns:
            bool: True if the values associated with the identifiers were removed successfully otherwise False.
        """

        # Get the current timestamp
        timestamp: datetime = datetime.now()

        # Initialize the total result to an empty list
        total_result: list[Any] = []

        # Initialize the errors list to an empty list
        errors: list[str] = []

        # Iterate over the passed idenfifiers
        for identifier in identifiers:
            # Attempt to remove the current identifier
            result: bool = self.remove(
                identifier=identifier,
                is_bulk_operation=True,
                timestamp=timestamp,
            )

            # Check if the removal was unsuccessfull
            if not result:
                errors.append(result)

            # Append the result to the total result list
            total_result.append(result)

        # Check if the errors list contains any False booleans
        if errors and not all(errors):
            # Raise a ValueError exception
            ValueError(
                f"Failed to remove keys '{', '.join(errors)}' from the data dictionary. Please review your code for any mistakes before trying again."
            )

        # Update the updated at datetime of the PebbleDatabase instance with the passed value
        self.updated_at = timestamp

        # Return the result list to the caller
        return all(total_result)

    def set_metadata(
        self,
        key: str,
        value: Any,
    ) -> None:
        """
        Set the metadata associated with the passed key with the passed value.

        Args:
            key (str): The key of the metadata to be set.
            value (Any): The value to be associated with the passed key.

        Returns:
            None
        """

        # Set the metadata associated with the passed key with the passed value
        self.metadata[key] = value

    def size(self) -> int:
        """
        Return the total count to the caller.

        Returns:
            int: The total count to the caller.
        """

        # Return the total count to the caller
        return self.total

    def to_dict(self) -> dict[str, Any]:
        """
        Return a dictionary representation of the PebbleDatabase instance.

        Returns:
            dict[str, Any]: A dictionary representation of the PebbleDatabase instance.
        """

        # Return a dictionary representation of the PebbleDatabase instance
        return {
            "created_at": self.created_at,
            "entries": {
                "total": self.total,
                "values": self.entries,
            },
            "identifier": self.identifier,
            "metadata": self.metadata,
            "name": self.name,
            "path": self.path,
            "updated_at": self.updated_at,
        }

    def update(
        self,
        entry: dict[str, Any],
        identifier: str,
        is_bulk_operation: bool = False,
        timestamp: Optional[datetime] = None,
    ) -> bool:
        """
        Update the value associated with the passed identifier with the passed entry.

        Args:
            entry (dict[str, Any]): The entry to be updated.
            identifier (str): The identifier to be updated.
            is_bulk_operation (bool, optional): Whether the update is part of a bulk operation. Defaults to False.
            timestamp (Optional[datetime], optional): The timestamp to be associated with the update. Defaults to None.

        Returns:
            bool: True if the value associated with the identifier was updated successfully otherwise False.
        """

        # Get the current timestamp if the passed timestamp is None
        timestamp: datetime = timestamp or datetime.now()

        # Check if the passed identifier is contained within the data dictionary instance variable
        if identifier not in self._data["entries"]["values"]:
            # Raise a KeyError exception if the passed identifier was not found in the data dictionary instance variable
            raise KeyError(identifier)

        # Update the value associated with the passed identifier with the passed entry
        self._data["entries"]["values"].update(entry)

        # Check if the operation is not a bulk operation
        if not is_bulk_operation:
            # Update the updated at datetime of the PebbleDatabase instance with the passed value
            self.updated_at = timestamp

        # Return True to the caller to indicate sucess
        return True

    def update_in_bulk(
        self,
        entries: list[dict[str, Any]],
        identifiers: list[str],
    ) -> bool:
        """
        Update the values associated with the passed identifiers with the passed entries.

        Args:
            entries (list[Anydict[str, Any]]): The entries to be updated.
            identifiers (list[str]): The identifiers to be updated.

        Returns:
            bool: True if the values associated with the identifiers were updated successfully otherwise False.
        """

        # Get the current timestamp
        timestamp: datetime = datetime.now()

        # Initialize the result to an empty list
        result: list[Any] = []

        # Initialize the errors list to an empty list
        errors: list[KeyError] = []

        # Iterate over the passed entries and idenfifiers
        for (
            entry,
            identifier,
        ) in zip(entries, identifiers):
            try:
                # Attempt to append the result of updating the value associated with the current identifier with the current value
                result.append(
                    self.update(
                        entry=entry,
                        identifier=identifier,
                        is_bulk_operation=True,
                        timestamp=timestamp,
                    )
                )
            except KeyError as e:
                # Append the excepted KeyError exception to the errors list
                errors.append(e)

        # Check if the errors list is not empty
        if errors:
            # Raise a sinlge KeyError exception with all missing keys
            raise KeyError(*errors)

        # Update the updated at datetime of the PebbleDatabase instance with the passed value
        self.updated_at = timestamp

        # Return True if all operations in the result list were successfull
        return all(result)

    def values(self) -> ValuesView[Any]:
        """
        Return the values of the PebbleDatabase's entries.

        Returns:
            ValuesView[Any]: The values of the PebbleDatabase's entries.
        """

        # Return the values of the PebbleDatabase's entries
        return self.entries.values()


class PebbleDatabaseFactory:
    """
    A factory class that creates new PebbleDatabase instances.
    """

    @classmethod
    def create(
        cls,
        data: dict[str, Any],
        name: str,
        created_at: Optional[datetime] = None,
        identifier: Optional[str] = None,
        metadata: Optional[dict[str, Any]] = None,
        path: Optional[Path] = None,
        updated_at: Optional[datetime] = None,
    ) -> PebbleDatabase:
        """
        Create a new PebbleDatabase instance with the passed data dictionary, name string, and identifier string.

        Args:
            created_at (Optional[datetime], optional): The created at datetime to be stored in the PebbleDatabase instance. Defaults to None.
            data (dict[str, Any]): The data dictionary to be stored in the PebbleDatabase instance.
            identifier (Optional[str], optional): The identifier string to be stored in the PebbleDatabase instance. Defaults to None.
            metadata (Optional[dict[str, Any]], optional): The metadata dictionary to be stored in the PebbleDatabase instance. Defaults to None.
            name (str): The name string to be stored in the PebbleDatabase instance.
            path (Optional[Path], optional): The path to the PebbleDatabase instance. Defaults to None.
            updated_at (Optional[datetime], optional): The updated at datetime to be stored in the PebbleDatabase instance. Defaults to None.

        Returns:
            PebbleDatabase: The newly created PebbleDatabase instance.
        """

        # Check if the passed identifier is None
        if identifier is None:
            # Update the identifier with a newly generated UUID
            identifier = uuid.uuid4().hex

        # Check if the passed metadata is None
        if metadata is None:
            # Update the metadata with an empty dictionary
            metadata = {}

        # Check if the passed identifier is None
        if path is None:
            # Update the identifier with a newly generated UUID
            path = CWD

        # Return the newly created PebbleDatabase instance to the caller
        return PebbleDatabase(
            created_at=created_at,
            data=data,
            identifier=identifier,
            metadata=metadata,
            name=name,
            path=path,
            updated_at=updated_at,
        )

    @classmethod
    def create_default(
        cls,
        name: str,
    ) -> PebbleDatabase:
        """
        Create a new PebbleDatabase instance with the passed name string.

        Args:
            name (str): The name string to be stored in the PebbleDatabase instance.

        Returns:
            PebbleDatabase: The newly created PebbleDatabase instance.
        """

        return PebbleDatabase(
            created_at=datetime.now(),
            data={},
            identifier=uuid.uuid4().hex,
            metadata={},
            name=name,
            path=CWD,
            updated_at=None,
        )


class PebbleDatabaseBuilder:
    """
    A builder class for creating new PebbleDatabase instances.
    """

    def __init__(self) -> None:
        """
        Initialize the PebbleDatabaseBuilder instance with an empty configuration dictionary instance variable.

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
        other: "PebbleDatabaseBuilder",
    ) -> bool:
        """
        Check if the passed other object is equal to the PebbleDatabaseBuilder instance.

        Args:
            other (PebbleDatabaseBuilder): The other object to be checked.

        Returns:
            bool: True if the passed other object is equal to the PebbleDatabaseBuilder instance, False otherwise.
        """

        # Check if the passed other object is not a PebbleDatabaseBuilder instance
        if not isinstance(
            other,
            PebbleDatabase,
        ):
            # Return False as a comparison between non-identical classes is not supported
            return False

        # Return True if the configuration dictionary instance variables of the two PebbleDatabaseBuilder instance are equal otherwise False
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
        Return a string representation of the PebbleDatabaseBuilder instance.

        Returns:
            str: A string representation of the PebbleDatabaseBuilder instance.
        """

        # Return a string representation of the PebbleDatabaseBuilder instance
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

    @property
    def configuration(self) -> dict[str, Any]:
        """
        Return a copy of the configuration dictionary instance variable to the caller.

        Returns:
            dict[str, Any]: A copy of the configuration dictionary instance variable.
        """

        # Return a copy of the configuration dictionary instance variable to the caller
        return self._configuration.copy()

    def build(self) -> PebbleDatabase:
        """
        Attempt to create and return the PebbleDatabase instance.

        Returns:
            PebbleDatabase: The newly created PebbleDatabase instance.
        """

        # Attempt to create and return the PebbleDatabase instance
        return PebbleDatabaseFactory.create(**self._configuration)

    def with_created_at(
        self,
        value: Optional[datetime] = None,
    ) -> Self:
        """
        Update the configuration with the passed value.

        Args:
            value (Optional[datetime], optional): The value to be updated. Defaults to None.

        Returns:
            Self: The builder.
        """

        # Check if the passed value is None
        if value is None:
            # Update the passed value with the current datetime
            value = datetime.now()

        # Update the configuration with the passed value
        self._configuration["created_at"] = value

        # Return the builder
        return self

    def with_data(
        self,
        value: dict[str, Any],
    ) -> Self:
        """
        Update the configuration with the passed value.

        Args:
            value (dict[str, Any]): The value to be updated.

        Returns:
            Self: The builder.
        """

        # Check if the passed value is an empty dictionary
        if not value:
            # Update the passed value with an empty dictionary
            value = {
                "entries": {
                    "total": 0,
                    "values": {},
                },
            }

        # Update the configuration with the passed value
        self._configuration["data"] = value

        # Update the 'total' keyword with the total number of entries
        self._configuration["data"]["entries"]["total"] = len(
            self._configuration["data"]["entries"]["values"]
        )

        # Return the builder
        return self

    def with_entries(
        self,
        values: Union[dict[str, Any], list[dict[str, Any]]],
    ) -> Self:
        """
        Update the configuration with the passed value.

        Args:
            values (Union[dict[str, Any], list[dict[str, Any]]]):
                The value to be added to the 'entries' key in the configuration.

        Returns:
            Self: The builder.
        """

        # Check if the 'data' key is not in the configuration dictionary
        if "data" not in self._configuration:
            # Update the 'data' key in the configuration with an empty dictionary
            self._configuration["data"] = {}

        # Check if the 'entries' key is not in the configuration dictionary
        if "entries" not in self._configuration["data"]:
            # Update the 'entries' key in the configuration with an empty dictionary
            self._configuration["data"]["entries"] = {
                "values": {},
                "total": 0,
            }

        # Check if the passed value is a dictionary
        if isinstance(
            values,
            dict,
        ):
            # Convert the passed value into a list
            values = list(values)

        # Iterate over the values
        for (
            index,
            value,
        ) in enumerate(
            iterable=values,
            start=len(self._configuration["data"]["entries"]["values"]),
        ):
            # Update the 'entries' key in the configuration with the passed value
            self._configuration["data"]["entries"]["values"][index] = value

        # Update the 'total' keyword with the total number of entries
        self._configuration["data"]["entries"]["total"] = len(
            self._configuration["data"]["entries"]["values"]
        )

        # Return the builder
        return self

    def with_identifier(
        self,
        value: Optional[str] = None,
    ) -> Self:
        """
        Update the configuration with the passed value.

        Args:
            value (Optional[str], optional): The value to be updated. Defaults to None.

        Returns:
            Self: The builder.
        """

        # Check if the passed identifier string value is None
        if value is None:
            # Initialize a new UUID and store it in the value
            value = uuid.uuid4().hex

        # Update the configuration with the passed value
        self._configuration["identifier"] = value

        # Return the builder
        return self

    def with_metadata(
        self,
        value: Optional[dict[str, Any]] = None,
    ) -> Self:
        """
        Update the configuration with the passed value.

        Args:
            value (Optional[dict[str, Any]], optional): The value to be updated. Defaults to None.

        Returns:
            Self: The builder.
        """

        # Check if the passed metadata dictionary value is None
        if value is None:
            # Update the passed value with an empty dictionary
            value = {}

        # Update the configuration with the passed value
        self._configuration["metadata"] = value

        # Return the builder
        return self

    def with_name(
        self,
        value: str,
    ) -> Self:
        """
        Update the configuration with the passed value.

        Args:
            value (str): The value to be updated.

        Returns:
            Self: The builder.
        """

        # Update the configuration with the passed value
        self._configuration["name"] = value

        # Return the builder
        return self

    def with_path(
        self,
        value: Optional[Path] = None,
    ) -> Self:
        """
        Update the configuration with the passed value.

        Args:
            value (Optional[Path], optional): The value to be updated. Defaults to None.

        Returns:
            Self: The builder.
        """

        # Check if the passed path Path object value is None
        if value is None:
            # Store the global 'CWD' variable in the passed value
            value = CWD

        # Check if a name has already been added to the configuration dictionary instance variable
        if (
            self._configuration.get(
                "name",
                None,
            )
            is not None
        ):
            # Update the configuration with the passed value
            value = Path(
                value,
                f"{self._configuration['name']}.json",
            )

        # Update the configuration with the passed value
        self._configuration["path"] = value

        # Return the builder
        return self

    def with_updated_at(
        self,
        value: datetime,
    ) -> Self:
        """
        Update the configuration with the passed value.

        Args:
            value (datetime): The value to be updated.

        Returns:
            Self: The builder.
        """

        # Update the 'updated_at' key in the configuration with the passed value
        self._configuration["updated_at"] = value

        # Return the builder
        return self


class PebbleDatabaseLoader:
    """
    A class that loads a PebbleDatabase instance from a file.
    """

    @classmethod
    def load(
        cls,
        path: Path,
    ) -> PebbleDatabase:
        """
        Load a PebbleDatabase instance from a file.

        Args:
            path (Path): The path to the file.

        Returns:
            PebbleDatabase: The loaded PebbleDatabase instance.
        """

        # Check if the path exists
        if not path.exists():
            # Raise a FileNotFoundError exception if the path does not exist
            raise FileNotFoundError(path)

        data: dict[str, Any] = DataConversionUtils.deserialize(
            value=run_async(
                function=read_file_if_not_exists,
                path=path,
            ),
        )

        # Return a new PebbleDatabase instance
        return PebbleDatabase(
            created_at=data.get("created_at", None),
            data={"entries": data.get("entries", {})},
            identifier=data.get("identifier", None),
            metadata=data.get("metadata", {}),
            name=data.get("name", ""),
            path=data.get("path", None),
            updated_at=data.get("updated_at", None),
        )
