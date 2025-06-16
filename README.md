# AdGuardHome-LogSync

A Python tool to synchronize AdGuard Home query logs between multiple instances with automatic log rotation.

## Description

[AdGuardHome-LogSync](https://pypi.org/project/adguardhome-logsync/) allows you to merge and synchronize query logs from multiple AdGuard Home instances while automatically managing log retention. This is useful when you're running multiple AdGuard Home instances and want to maintain a unified query log with configurable retention policies.

## Features

- Backup existing query logs
- Merge multiple query log files
- Automatic log rotation with configurable retention time
- Safe atomic replacement of original logs
- Asynchronous processing for better performance
- Memory-efficient streaming for large log files
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
adguardhome-logsync --name <instance-name> --path <querylog-path> --backup <backup-directory> [--retention <seconds>]
```

### Parameters

- `--name`: Current instance nickname (required)
- `--path`: Path to the query log file (required)  
- `--backup`: Path to backup directory (required)
- `--retention`: Log retention time in seconds (optional, default: 604800 = 7 days)

### Examples

#### Basic usage with default 24-hour retention
```bash
adguardhome-logsync --name genx --path ~/adg/workdir/data/querylog.json --backup ~/adg/workdir/data/backup
```

#### Keep logs for 7 days (604800 seconds)
```bash
adguardhome-logsync --name genx --path ~/adg/workdir/data/querylog.json --backup ~/adg/workdir/data/backup --retention 604800
```

#### Keep logs for 12 hours (43200 seconds)
```bash
adguardhome-logsync --name genx --path ~/adg/workdir/data/querylog.json --backup ~/adg/workdir/data/backup --retention 43200
```

#### Keep logs for 1 hour only (3600 seconds)
```bash
adguardhome-logsync --name genx --path ~/adg/workdir/data/querylog.json --backup ~/adg/workdir/data/backup --retention 3600
```

### Common Retention Values

| Period | Seconds | Example Usage |
|--------|---------|---------------|
| 1 hour | 3600 | `--retention 3600` |
| 6 hours | 21600 | `--retention 21600` |
| 12 hours | 43200 | `--retention 43200` |
| 1 day | 86400 | `--retention 86400` |
| 3 days | 259200 | `--retention 259200` |
| 1 week | 604800 | `--retention 604800` (default) |
| 1 month | 2592000 | `--retention 2592000` |

### Example Output

```
Starting log synchronization for instance: genx
Log retention: 604800 seconds (168.0 hours)
Logs older than 2025-01-09 22:41:58 will be removed
Backing up querylog...
Searching for querylog files...
Found 3 querylog files
Merging querylogs...
Writing merged querylog...
Moving to updated querylog at /tmp/tmp2eqv7rdc.json...
Log synchronization completed successfully
```

## Automation

> Take care! it's from AI (If you have a tested version, please new PR for that, thanks a lot!)

### Systemd Timer (Linux)

Create a systemd service file `/etc/systemd/system/adguard-logsync.service`:

```ini
[Unit]
Description=AdGuard Home Log Sync
After=network.target

[Service]
Type=oneshot
ExecStart=/usr/local/bin/adguardhome-logsync --name server1 --path /opt/adguard/querylog.json --backup /opt/adguard/backup --retention 604800
User=adguard
Group=adguard
```

Create a timer file `/etc/systemd/system/adguard-logsync.timer`:

```ini
[Unit]
Description=Run AdGuard Home Log Sync every 5 minutes
Requires=adguard-logsync.service

[Timer]
OnCalendar=*:0/5
Persistent=true

[Install]
WantedBy=timers.target
```

Enable and start:
```bash
sudo systemctl enable adguard-logsync.timer
sudo systemctl start adguard-logsync.timer
```

### Cron Job

```bash
# Run every 5 minutes, keep logs for 1 week
*/5 * * * * /usr/local/bin/adguardhome-logsync --name server1 --path /opt/adguard/querylog.json --backup /opt/adguard/backup --retention 604800

# Run every hour, keep logs for 1 day
0 * * * * /usr/local/bin/adguardhome-logsync --name server1 --path /opt/adguard/querylog.json --backup /opt/adguard/backup --retention 86400
```

## Development

### Prerequisites

- Python 3.9+
- [uv](https://github.com/astral-sh/uv) (for development)

### Running from Source

Clone the repository:
```bash
git clone https://github.com/xz-dev/AdGuardHomeLogSync.git
cd AdGuardHomeLogSync
```

Run with uv:
```bash
uv run main.py --name genx --path ~/adg/workdir/data/querylog.json --backup ~/adg/workdir/data/backup --retention 604800
```

### Project Structure

```
AdGuardHomeLogSync/
├── main.py                 # Main entry point
├── utils/
│   ├── querylog_copy.py   # Backup and file operations
│   └── querylog_merge.py  # Asynchronous log merging with retention
├── pyproject.toml         # Project configuration
└── README.md             # This file
```

## How It Works

1. **Backup**: Creates a backup of the current query log with instance name
2. **Discovery**: Searches for all query log files in the backup directory
3. **Merge**: Combines all found query logs into a single unified log
4. **Filter**: Removes logs older than the specified retention time
5. **Replace**: Safely replaces the original query log with the merged and filtered version

## Performance Features

- **Asynchronous Processing**: Multiple log files are processed concurrently
- **Streaming**: Large files are processed in chunks to minimize memory usage
- **Efficient Sorting**: Uses SortedList for optimal insertion performance
- **Memory Management**: Configurable chunk sizes prevent memory spikes

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
