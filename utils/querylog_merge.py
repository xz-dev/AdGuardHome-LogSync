from sortedcontainers import SortedList
import aiofiles
import orjson
import asyncio


async def merge_querylog_streaming(
    full_querylogs: SortedList[tuple[str, bytes]],
    log_file_path: str,
    chunk_size: int = 10000,  # 每1万行插入一次
    lock: asyncio.Lock = None,
):
    """
    Stream process a single querylog file and insert records in chunks to reduce memory pressure.

    Args:
        full_querylogs: A SortedList that stores all query logs as (timestamp, log_data) tuples
        log_file_path: Path to the querylog file to process
        chunk_size: Number of records to buffer before inserting into the SortedList
        lock: Optional asyncio Lock for thread safety when used with concurrent processing

    Returns:
        None: Records are inserted directly into the provided full_querylogs SortedList
    """
    chunk_buffer = []
    line_count = 0

    async with aiofiles.open(log_file_path, "rb") as file:
        async for line in file:
            line = line.strip()
            if line:
                try:
                    querylog_json = orjson.loads(line)
                    chunk_buffer.append((querylog_json["T"], line))
                    line_count += 1

                    # Insert batch when chunk_size is reached
                    if len(chunk_buffer) >= chunk_size:
                        if lock:
                            async with lock:
                                full_querylogs.update(chunk_buffer)
                        else:
                            full_querylogs.update(chunk_buffer)
                        chunk_buffer = []

                except orjson.JSONDecodeError:
                    continue

    # Process remaining data
    if chunk_buffer:
        if lock:
            async with lock:
                full_querylogs.update(chunk_buffer)
        else:
            full_querylogs.update(chunk_buffer)


async def merge_querylogs(logs_paths: list[str]) -> bytes:
    """
    Merge multiple querylog files using streaming approach with concurrent processing.

    This function supports large files by processing them in chunks and inserting
    into a SortedList incrementally to reduce memory spikes.

    Args:
        logs_paths: List of paths to querylog files to merge

    Returns:
        bytes: Merged and sorted querylog content as bytes
    """
    full_querylogs = SortedList()
    lock = asyncio.Lock()

    # Process all files concurrently
    tasks = [
        merge_querylog_streaming(
            full_querylogs, log_file_path, chunk_size=10000, lock=lock
        )
        for log_file_path in logs_paths
    ]

    await asyncio.gather(*tasks)

    # Generate result
    return b"\n".join(querylog[1] for querylog in full_querylogs)
