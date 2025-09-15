# PebbleDB

PebbleDB is a lightweight, high-performance key-value store written in Python, inspired by RocksDB and built on top of the powerful Pebble storage engine. It's designed for applications that require fast, reliable, and persistent storage with a simple API.

## Features

- **High Performance**: Optimized for fast read and write operations
- **Simple API**: Easy-to-use interface for common database operations
- **Persistent Storage**: Data is safely stored on disk
- **Thread-Safe**: Designed for concurrent access
- **Lightweight**: Minimal dependencies and small footprint

## Installation

```bash
git clone https://github.com/louisgoodnews/PebbleDB.git
cd PebbleDB
python -m pip install -e .
```

## Quick Start

```python
from pebble_db import PebbleDB

# Open a database (creates if it doesn't exist)
db = PebbleDB("my_database")

# Store data
db.put(b"key1", b"value1")

# Retrieve data
value = db.get(b"key1")
print(value)  # b'value1'

# Delete data
db.delete(b"key1")

# Close the database
db.close()
```

## Documentation

For detailed documentation, please visit our [documentation site](https://pebbledb.readthedocs.io/).

## Contributing

We welcome contributions! Please see our [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute to this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Code of Conduct

Please note that this project is released with a [Code of Conduct](CODE_OF_CONDUCT.md). By participating in this project you agree to abide by its terms.
