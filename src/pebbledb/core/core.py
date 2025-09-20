"""
Author: Louis Goodnews
Date: 2025-09-13
"""

from pathlib import Path
from typing import Final, Optional, Union

from core.database import (
    PebbleDatabase,
    PebbleDatabaseBuilder,
    PebbleDatabaseLoader,
)
from core.table import (
    PebbleTable,
    PebbleTableBuilder,
    PebbleTableLoader,
)


__all__: Final[list[str]] = ["Pebble"]


class Pebble:
    """
    The core class of the PebbleDB library.
    """

    # The database instance
    DATABASE: Optional[PebbleDatabase] = None

    # The table instance
    TABLE: Optional[PebbleTable] = None

    @classmethod
    def get_database_builder(cls) -> PebbleDatabaseBuilder:
        """
        Return a PebbleDatabaseBuilder instance.

        Returns:
            PebbleDatabaseBuilder: A PebbleDatabaseBuilder instance.
        """

        # Return a PebbleDatabaseBuilder instance
        return PebbleDatabaseBuilder()

    @classmethod
    def get_database_or_default(
        cls,
        name_or_path: Union[Path, str],
    ) -> PebbleDatabase:
        """
        Return a PebbleDatabase instance.

        This method creates or loads a database instance based on the passed name or path.

        Args:
            name_or_path (Union[Path, str]): The name or path of the database.

        Returns:
            PebbleDatabase: A PebbleDatabase instance.
        """

        # Check if a database already exists and if it matches the passed name_or_path
        if cls.DATABASE is not None and (
            cls.DATABASE.name == name_or_path or cls.DATABASE.path == name_or_path
        ):
            # Return the database object
            return cls.DATABASE

        # Check if the passed name_or_path is a Path object
        if isinstance(
            name_or_path,
            Path,
        ):
            # Check if the path exists
            if not name_or_path.exists():
                # Raise a FileNotFoundError exception if the path does not exist
                raise FileNotFoundError(name_or_path)

            # Load the database instance
            result: PebbleDatabase = PebbleDatabaseLoader.load(path=name_or_path)

            # Update the class variable
            cls.DATABASE = result

            # Return the database instance
            return result
        else:
            # Initialize the builder
            builder: PebbleDatabaseBuilder = PebbleDatabaseBuilder()

            # Update the builder with the passed name_or_path
            (
                builder.with_created_at(value=None)
                .with_data(value={})
                .with_identifier(value=None)
                .with_name(value=name_or_path)
                .with_path(value=None)
            )

            # Build the database instance
            result: PebbleDatabase = builder.build()

            # Update the class variable
            cls.DATABASE = result

            # Return the database instance
            return result

    @classmethod
    def get_table_builder(cls) -> PebbleTableBuilder:
        """
        Return a PebbleTableBuilder instance.

        Returns:
            PebbleTableBuilder: A PebbleTableBuilder instance.
        """

        # Return a PebbleTableBuilder instance
        return PebbleTableBuilder()

    @classmethod
    def get_table_or_default(
        cls,
        name_or_path: Union[Path, str],
    ) -> PebbleTable:
        """
        Return a PebbleTable instance.

        This method creates or loads a table instance based on the passed name or path.

        Args:
            name_or_path (Union[Path, str]): The name or path of the table.

        Returns:
            PebbleTable: A PebbleTable instance.
        """

        # Check if a table already exists and if it matches the passed name_or_path
        if cls.TABLE is not None and (
            cls.TABLE.name == name_or_path or cls.TABLE.path == name_or_path
        ):
            # Return the table object
            return cls.TABLE

        # Check if the passed name_or_path is a Path object
        if isinstance(
            name_or_path,
            Path,
        ):
            # Check if the path exists
            if not name_or_path.exists():
                # Raise a FileNotFoundError exception if the path does not exist
                raise FileNotFoundError(name_or_path)

            # Load the table instance
            result: PebbleTable = PebbleTableLoader.load(path=name_or_path)

            # Update the class variable
            cls.TABLE = result

            # Return the table instance
            return result
        else:
            # Initialize the builder
            builder: PebbleTableBuilder = PebbleTableBuilder()

            # Update the builder with the passed name_or_path
            (
                builder.with_created_at(value=None)
                .with_data(value={})
                .with_identifier(value=None)
                .with_name(value=name_or_path)
                .with_path(value=None)
            )

            # Build the table instance
            result: PebbleTable = builder.build()

            # Update the class variable
            cls.TABLE = result

            # Return the table instance
            return result

    @classmethod
    def load_database(
        cls,
        path: Union[Path, str],
    ) -> PebbleDatabase:
        """
        Load a database instance from a file.

        Args:
            path (Union[Path, str]): The path to the database file.

        Returns:
            PebbleDatabase: A PebbleDatabase instance.
        """

        # Load the database instance
        result: PebbleDatabase = PebbleDatabaseLoader.load(path=path)

        # Update the class variable
        cls.DATABASE = result

        # Return the database instance
        return result

    @classmethod
    def load_table(
        cls,
        path: Union[Path, str],
    ) -> PebbleTable:
        """
        Load a table instance from a file.

        Args:
            path (Union[Path, str]): The path to the table file.

        Returns:
            PebbleTable: A PebbleTable instance.
        """

        # Load the table instance
        result: PebbleTable = PebbleTableLoader.load(path=path)

        # Update the class variable
        cls.TABLE = result

        # Return the table instance
        return result
