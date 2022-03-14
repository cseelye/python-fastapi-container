import subprocess

from app.util.log import log


def execute_command(command: str, timeout: int = 300, host: bool = True) -> tuple:
    """
    Execute a shell command and wait for it to complete.
    This function does not throw on command errors; it will still return the return code and output from the command.

    Args:
        command:    the command to run, in shell form
        timeout:    timeout for the command, in seconds
        host:       run the command in the host environment instead of in the container

    Returns:
        A tuple of return code, stdout, stderr
    """
    if host:
        cmd = "nsenter -t 1 -m -u -n -i {}".format(command)
    else:
        cmd = command

    log.debug(f"Executing command [{cmd}]")
    result = subprocess.run(
        cmd,
        timeout=timeout,
        shell=True,
        executable="/usr/bin/bash",
        check=False,
        capture_output=True,
        encoding="utf-8",
    )
    log.debug(f"retcode=[{result.returncode}] stdout=[{result.stdout}] stderr=[{result.stderr}]")

    return result.returncode, result.stdout, result.stderr
