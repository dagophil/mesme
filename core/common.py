import json
import logging
import os
import sys

import appdirs


def log_current_error():
    """
    Log the current exception.
    """
    ex_type = sys.exc_info()[0]
    ex = sys.exc_info()[1]
    if ex_type is None:
        logging.warning("Called log_current_error(), but there is no error.")
    else:
        logging.error("Unexpected error: %s %s " % (ex_type, ex))


def log_exceptions(f):
    """
    This decorator wraps a function with try / except. If an exception occurs, it is logged and reraised.
    Since the exceptions that occur in PyQt slots are silenced, it is useful to wrap all slots with @log_exceptions.
    If decorated slots are called in chains, the exception might be logged multiple times.
    :param f: The function.
    :return: The wrapped function.
    """
    def wrapped(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except:
            log_current_error()
            raise
    return wrapped


class SettingsEncoder(json.JSONEncoder):
    """
    JSON encoder that also looks for a to_dict() method.
    """

    def default(self, obj):
        """
        Try to call the to_dict() method of the given object.
        :param obj: The object.
        :return: Returns obj.to_dict().
        """
        if hasattr(obj, "to_dict"):
            return obj.to_dict()
        else:
            return super(SettingsEncoder, self).default(obj)


class Settings(object):
    """
    The settings object.
    """

    def __init__(self, dirs):
        self.dirs = dirs
        self.config_file = os.path.join(self.dirs.user_config_dir, "config.json")
        self.database_dir = os.path.join(self.dirs.user_data_dir, "databases")

    def __setitem__(self, name, value):
        """
        Store the setting (name=value) in the configuration file.
        :param name: The setting name.
        :param value: The setting value.
        """
        # Create the folder structure if necessary.
        filename = self.config_file
        folder = os.path.dirname(filename)
        os.makedirs(folder, exist_ok=True)

        # Read the current configuration.
        config = {}
        if os.path.isfile(filename):
            with open(filename, "r") as f:
                config = json.load(f)

        # Save the setting.
        config[name] = value
        s = json.dumps(config, indent=2, cls=SettingsEncoder)
        with open(filename, "w") as f:
            f.write(s)

    def __getitem__(self, name):
        """
        Read the setting from the config file and return it.
        If the config file does not exist or if a setting with the given name does not exist,
        a KeyError is raised.
        :param name: The setting name.
        :return: Returns the setting value.
        """
        filename = self.config_file
        if os.path.isfile(filename):
            with open(filename, "r") as f:
                config = json.load(f)
            return config[name]
        else:
            raise KeyError("Could not find settings file.")


# The global settings object.
global_settings = Settings(appdirs.AppDirs("mesme", version="0.0.1"))
