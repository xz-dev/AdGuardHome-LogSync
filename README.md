# AdGuardHome-LogSync

A Python tool to synchronize AdGuard Home query logs between multiple instances.

## Description

[AdGuardHome-LogSync](https://pypi.org/project/adguardhome-logsync/) allows you to merge and synchronize query logs from multiple AdGuard Home instances. This is useful when you're running multiple AdGuard Home instances and want to maintain a unified query log.

## Features

- Backup existing query logs
- Merge multiple query log files
- Safe atomic replacement of original logs
- Command-line interface for easy automation

## Installation

### Using pipx (Recommended)

Install from PyPI:
```bash
pipx install adguardhome-logsync
```

Install from Git repository:
```bash
pipx install git+https://github.com/xz-dev/AdGuardHomeLogSync.git
```

### Using pip

Install from PyPI:
```bash
pip install adguardhome-logsync
```

Install from Git repository:
```bash
pip install git+https://github.com/xz-dev/AdGuardHomeLogSync.git
```

## Usage

```bash
adguardhome-logsync --name <instance-name> --path <querylog-path> --backup <backup-directory>
```

### Parameters

- `--name`: Current instance nickname (required)
- `--path`: Path to the query log file (required)  
- `--backup`: Path to backup directory (required)

### Example

```bash
adguardhome-logsync --name genx --path ~/adg/workdir/data/querylog.json --backup ~/adg/workdir/data/backup
```

### Example Output

```
Starting log synchronization for instance: genx
Backing up querylog...
Searching for querylog files...
Found 3 querylog files
Merging querylogs...
Writing merged querylog...
Moving to updated querylog at /tmp/tmp2eqv7rdc.json...
Log synchronization completed successfully
```

## Development

### Prerequisites

- Python 3.8+
- [uv](https://github.com/astral-sh/uv) (for development)

### Running from Source

Clone the repository:
```bash
git clone https://github.com/xz-dev/AdGuardHomeLogSync.git
cd AdGuardHomeLogSync
```

Run with uv:
```bash
uv run main.py --name genx --path ~/adg/workdir/data/querylog.json --backup ~/adg/workdir/data/backup
```

### Project Structure

```
AdGuardHomeLogSync/
├── main.py                 # Main entry point
├── utils/
│   ├── querylog_copy.py   # Backup and file operations
│   └── querylog_merge.py  # Log merging logic
├── pyproject.toml         # Project configuration
└── README.md             # This file
```

## How It Works

1. **Backup**: Creates a backup of the current query log with instance name
2. **Discovery**: Searches for all query log files in the backup directory
3. **Merge**: Combines all found query logs into a single unified log
4. **Replace**: Safely replaces the original query log with the merged version

## Requirements

- AdGuard Home instances with JSON format query logs
- Write access to query log files and backup directory
- Python 3.8 or higher

## License

BSD-3-Clause

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Issues

Please report issues at: https://github.com/xz-dev/AdGuardHomeLogSync/issues
