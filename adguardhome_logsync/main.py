import time
from argparse import ArgumentParser
from pathlib import Path
from tempfile import NamedTemporaryFile

from .utils.querylog_copy import backup_querylog, move_new_querylog
from .utils.querylog_merge import merge_querylogs


async def main():
    arg_parser = ArgumentParser(
        prog="adguardhome-logsync",
        description="Synchronize AdGuard Home Log between multi-instances",
    )

    # Add command line arguments
    arg_parser.add_argument(
        "--name",
        type=str,
        help="Current instance nicename",
        required=True,
    )

    arg_parser.add_argument(
        "--path",
        type=str,
        help="Path to querylog",
        required=True,
    )

    arg_parser.add_argument(
        "--backup",
        type=str,
        help="Path to backup querylog",
        required=True,
    )

    arg_parser.add_argument(
        "--retention",
        type=int,
        help="Log retention time in seconds (logs older than this will be removed)",
        default=7 * 24 * 60 * 60,  # 7 days by default
    )

    args = arg_parser.parse_args()

    try:
        # Validate input paths
        querylog_path = Path(args.path)
        backup_path = Path(args.backup)

        if not querylog_path.exists():
            raise FileNotFoundError(f"Querylog file not found: {querylog_path}")
        if not backup_path.exists():
            raise FileNotFoundError(f"Backup directory not found: {backup_path}")

        # Calculate active_time (current time - retention seconds)
        current_time = time.time()
        active_time = current_time - args.retention

        print(f"Starting log synchronization for instance: {args.name}")
        print(
            f"Log retention: {args.retention} seconds ({args.retention / 3600:.1f} hours)"
        )
        print(
            f"Logs older than {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(active_time))} will be removed"
        )

        # Copy the querylog to backup path
        print("Backing up querylog...")
        backup_querylog(
            str(querylog_path),
            str(backup_path),
            args.name,
        )

        # Get the logs paths from backup dir
        print("Searching for querylog files...")
        logs_paths = list(backup_path.glob("querylog-*.json"))

        print(f"Found {len(logs_paths)} querylog files")

        # Merge the querylogs with retention policy
        tmp_file = NamedTemporaryFile(delete=False, suffix=".json")
        tmp_file_path = tmp_file.name
        print(f"Merging querylogs into temporary file: {tmp_file_path}")
        await merge_querylogs(
            logs_paths=logs_paths,
            active_time=active_time,
            new_log_path=tmp_file_path,
        )

        # Move the new querylog to the original path
        print(f"Moving to updated querylog at {tmp_file_path}...")
        move_new_querylog(tmp_file_path, str(querylog_path))

        print("Log synchronization completed successfully")

    except Exception as e:
        print(f"Error during log synchronization: {e}")
        raise
