import shutil
from pathlib import Path


def backup_querylog(log_file_path: str, backup_file_path: str, host_name: str):
    """
    Backup a querylog file by copying it to a new location.

    Args:
        log_file_path: Path to the original querylog file
        backup_file_path: Path where the backup will be stored
    """

    # copy derectly even if the backup file exists
    log_file_path = Path(log_file_path)
    backup_file_path = Path(backup_file_path) / f"querylog-{host_name}.json"
    shutil.copy2(log_file_path, backup_file_path)


def move_new_querylog(log_file_path: str, new_log_file_path: str) -> None:
    """
    Move a querylog file to a new location.

    Args:
        log_file_path: Path to the original querylog file
        new_log_file_path: Path where the querylog file will be moved
    """

    # move the log file to the new location
    shutil.move(log_file_path, new_log_file_path)
