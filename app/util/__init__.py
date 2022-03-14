def get_service_version() -> str:
    """
    Get the version of this service

    Returns:
        A version string
    """
    try:
        with open("/version", encoding="utf-8") as version_file:
            version = version_file.read().strip()
    except (IOError, OSError):
        version = "99.99.99"
    return version
