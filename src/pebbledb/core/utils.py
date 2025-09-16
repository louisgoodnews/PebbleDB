"""
Author: Louis Goodnews
Date: 2025-09-13
"""

from pathlib import Path
from typing import Any, Final, Optional

from core.files import read_file_if_not_exists, write_file_if_not_exists

from utils.utils import merge_dicts, run_async

from datautils import DataConversionUtils
from logger import Logger

__all__: Final[list[str]] = []


class PebbleCommitError(Exception):
    """
    Exception raised when a commit fails.
    """


class PebbleCommitService:
    """
    A class that represents a commit service.
    """

    _shared_instance: Optional["PebbleCommitService"] = None

    def __new__(cls) -> "PebbleCommitService":
        """
        Create a new instance of the PebbleCommitService class.

        Returns:
            PebbleCommitService: A new instance of the PebbleCommitService class.
        """

        if cls._shared_instance is None:
            cls._shared_instance = super(PebbleCommitService, cls).__new__(cls)
            cls._shared_instance.init()
        return cls._shared_instance

    def init(self) -> None:
        """ """

        self._logger: Final[Logger] = Logger.get_logger(name=self.__class__.__name__)

    def commit(
        self,
        database_or_table: dict[str, Any],
    ) -> None:
        """
        Commit the changes to the database or table.

        Args:
            database_or_table (dict[str, Any]): The database or table to commit.

        Returns:
            None
        """
        try:
            # Attempt to read the database or table from a file
            string: str = run_async(
                function=read_file_if_not_exists,
                path=Path(database_or_table["path"]),
            )

            # Check if the read data is an empty string
            if string == "":
                # Attempt to write the database or table to a file
                run_async(
                    content=DataConversionUtils.serialize(value=database_or_table),
                    function=write_file_if_not_exists,
                    path=Path(database_or_table["path"]),
                )

                # Return early
                return

            # Deserialize the read data
            old: dict[str, Any] = DataConversionUtils.deserialize(value=string)

            # Merge the old and new data
            merged: dict[str, Any] = merge_dicts(new=database_or_table, old=old)

            # Serialize the merged data
            serialized: str = DataConversionUtils.serialize(value=merged)

            # Create a temporary file
            temporary: Path = Path(
                database_or_table["path"].replace(
                    ".json",
                    "_tmp.json",
                )
            )

            # Attempt to write the merged data to a file
            run_async(
                content=serialized,
                function=write_file_if_not_exists,
                path=temporary,
            )

            # Rename the temporary file to the database or table file
            temporary.rename(database_or_table["path"])

            # Log the success
            self._logger.info(
                message=f"Database or table '{database_or_table['name']}' committed successfully",
            )
        except Exception as e:
            # Log the exception
            self._logger.exception(
                exception=e,
                message=f"Failed to commit database or table '{database_or_table['name']}' to file: {e}",
            )

            # Raise a PebbleCommitError exception
            raise PebbleCommitError(
                f"Failed to commit database or table '{database_or_table['name']}' to file: {e}",
            )
