import logging
import logging.config

from app.settings import Settings

log = logging.getLogger("service")

current_settings = Settings()

##############################################################################
# Apply log settings from Settings
##############################################################################
# Set the log level
try:
    level = logging.getLevelName(current_settings.log_level.upper())
    log.setLevel(level)
except ValueError:
    log.error("Unknown log level from settings, leaving log at default level")
