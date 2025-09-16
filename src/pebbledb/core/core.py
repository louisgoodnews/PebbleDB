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
    def get_database(
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
    def get_table(
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
