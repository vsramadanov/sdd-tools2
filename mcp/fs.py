from langchain_core.tools import tool
import logging
from pathlib import Path


@tool
def write_file(filename: str, content: str) -> str:
    """Write text content to a file, creating parent directories if needed.

    Use this tool when the task requires saving generated code, specs,
    review reports, or any text artifact to disk. The file is overwritten
    if it already exists. Parent directories are created automatically.

    Args:
        filename: Path to the target file, relative to the current working
            directory or absolute. Must include the file extension.
        content: Full text to write. Must be UTF-8 encodable. For source
            code, pass the code exactly as it should appear on disk, without
            markdown fences.

    Returns:
        A short status string. On success: "OK: wrote <N> bytes to <path>".
        On failure: "ERROR: <reason>". Never raises.
    """

    log_content = content[:10] + '...' if len(content) > 10 else content
    logging.debug(f"write_file(filename={filename}, content={log_content})")

    try:
        path = Path(filename)
        path.parent.mkdir(parents=True, exist_ok=True)
        data = content.encode("utf-8")
        path.write_bytes(data)
        return f"OK: wrote {len(data)} bytes to {path}"
    except OSError as e:
        return f"ERROR: {e}"


@tool
def read_file(filename: str) -> str:
    """Read the full text content of a UTF-8 file from disk.

    Use this tool when the task requires reading source code, specs, review
    reports, logs, or any text file. Do not use for binary files or
    directories. Returns the file contents as a string, or an error message
    prefixed with "ERROR:".

    Args:
        filename: Path to the file, relative to the current working directory
            or absolute. Must include the file extension. Must not be a
            directory.

    Returns:
        The file content on success. On failure: "ERROR: <reason>". Never
        raises.
    """
    try:
        path = Path(filename)

        if not path.exists():
            return f"ERROR: file not found: {path}"

        if path.is_dir():
            return f"ERROR: path is a directory, not a file: {path}"

        if not path.is_file():
            return f"ERROR: path is not a regular file: {path}"

        return path.read_text(encoding="utf-8")
    except PermissionError as e:
        return f"ERROR: permission denied: {path} ({e})"
    except UnicodeDecodeError as e:
        return f"ERROR: file is not valid UTF-8: {path} ({e})"
    except OSError as e:
        return f"ERROR: cannot read {path}: {e}"
