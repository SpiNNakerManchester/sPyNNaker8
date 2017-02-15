from ConfigParser import ConfigParser

import os
import os.path
import appdirs
import string
import logging

from spynnaker8.utilities import log


def _add_section(parser, section_name, defaults):
    parser.add_section(section_name)
    for key, value in defaults.iteritems():
        parser.set(section_name, key,
                   "None" if value is None else str(value))


def read_config(file_names=None):
    """Attempt to read local configuration files to determine client
    settings.
    Parameters
    ----------
    file_names : [str, ...]
        Filenames to attempt to read. Later config file have higher priority.
    Returns
    -------
    ConfigParser
        The configuration loaded.
    """
    parser = ConfigParser()

    # The application name to use in config file names
    _name = "spynnaker_8_0.cfg"

    # Standard config file names/locations
    default_params_cfg_file = os.path.join(
        os.path.dirname(__file__), "spynnaker8.cfg")
    system_config_cfg_file = os.path.join(
        appdirs.site_config_dir(), ".spynnaker8.cfg")
    user_config_cfg_file = os.path.join(
        appdirs.user_config_dir(), ".spynnaker8.cfg")
    current_directory_cfg_file = os.path.join(os.curdir, ".{}".format(_name))

    # Search path for config files (lowest to highest priority)
    search_paths = [
        default_params_cfg_file,
        system_config_cfg_file,
        user_config_cfg_file,
        current_directory_cfg_file,
    ]

    # handle default parameters
    if file_names is None:
        file_names = search_paths

    _add_section(parser, "Stuff",
                 {"realtime_proportion": 1.0,
                  "convert_direct_connections": True,
                  "generate_connections_on_chip": True,
                  "stop_on_spinnaker": True,
                  "stop_after_loader": False,
                  "disable_software_watchdog": False,
                  "allocation_fudge_factor": 1.6})

    # Attempt to read from each possible file location in turn
    for filename in file_names:
        try:
            with open(filename, "r") as f:
                parser.readfp(f, filename)
        except (IOError, OSError):
            # File did not exist, keep trying
            pass

    if parser.has_option("Machine", "machine_spec_file"):
        machine_spec_file_path = parser.get("Machine", "machine_spec_file")
        if machine_spec_file_path != "None":
            with open(machine_spec_file_path, "r") as extra_config_file:
                parser.readfp(extra_config_file)

    # Create the root logger with the given level
    # Create filters based on logging levels
    try:
        if parser.getboolean("Logging", "instantiate"):
            logging.basicConfig(level=0)

        for handler in logging.root.handlers:
            handler.addFilter(log.ConfiguredFilter(parser))
            handler.setFormatter(log.ConfiguredFormatter(parser))
    except ConfigParser.NoSectionError:
        pass
    except ConfigParser.NoOptionError:
        pass

    # Log which config files we read
    logger = logging.getLogger(__name__)
    logger.info("Read config files: %s" % string.join(search_paths, ", "))

    return parser
