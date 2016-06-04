import appdirs
import json
import os
import logging


class UserProfile(object):
    """
    The UserProfile class stores user specific data, for example the location of the database file.
    """

    @staticmethod
    def from_json(json_str):
        """
        Create a user profile from the given json string.
        :param json_str: The json string.
        :return: Returns the user profile.
        """
        profile = UserProfile()
        json_dict = json.loads(json_str)
        for key, value in json_dict.items():
            profile[key] = value
        return profile

    @staticmethod
    def from_dict(d):
        """
        Create a user profile from the given dict.
        :param d: The dict.
        :return: Returns the user profile.
        """
        profile = UserProfile()
        for key, value in d:
            profile[key] = value
        return profile

    def __init__(self):
        """
        Create a user profile with uninitialized fields.
        """
        self.settings = {
            "database_location": ""
        }

    def __getitem__(self, name):
        """
        Return the value of the given profile setting.
        :param name: Name of the setting.
        :return: Returns the value of the setting.
        """
        return self.settings[name]

    def __setitem__(self, name, value):
        """
        Set the value of the given profile setting.
        :param name: Name of the setting. Only valid setting names are accepted.
        :param value: Value of the setting.
        """
        if name in self.settings:
            self.settings[name] = value
        else:
            raise IndexError

    def __str__(self):
        """
        Convert the settings dict to a string.
        :return: Returns the string representation of the settings dict.
        """
        return str(self.settings)


class UserProfileCollection(object):
    """
    The UserProfileCollection can load and save user profiles.
    """

    @staticmethod
    def default_location():
        """
        Return the filename of the default profile collection file.
        :return: Returns the filename of the default profile collection file.
        """
        dirs = appdirs.AppDirs("mesme", version="0.0.1")
        filename = os.path.join(dirs.user_config_dir, "config.json")
        return filename

    @staticmethod
    def from_file(filename):
        """
        Load a UserProfileCollection from the given file.
        :param filename: The filename.
        :return: Returns the loaded UserProfileCollection.
        """
        profiles = UserProfileCollection()
        with open(filename, "r") as f:
            json_dict = json.load(f)
            assert isinstance(json_dict, dict)
            if "users" in json_dict:
                for name, profile in json_dict["users"].items():
                    profiles[name] = UserProfile.from_dict(profile)
        return profiles

    def __init__(self):
        """
        Create an empty profile collection.
        """
        self.user_profiles = {}  # empty collection

    def __getitem__(self, key):
        """
        Return the user profile with the given key.
        :param key: The profile name.
        :return: Returns the user profile.
        """
        return self.user_profiles[key]

    def __setitem__(self, key, value):
        """
        Store a user profile with the given name.
        :param key: The profile name.
        :param value: The user profile.
        """
        self.user_profiles[key] = value

    def __delitem__(self, key):
        """
        Remove the user profile with the given name.
        :param key: The profile name.
        """
        del self.user_profiles[key]

    def items(self):
        """
        Return (name, profile) pairs of the stored profiles.
        :return:
        """
        return self.user_profiles.items()

    def to_json(self):
        """
        Convert the profile collection to a json string.
        :return: Returns the profile collection as a json string.
        """
        d = {name: profile.to_json() for name, profile in self.user_profiles.items()}
        return json.dumps(d)

    def save(self, filename):
        """
        Save the profile collection to the given file. If the file already exists it will be overwritten.
        :param filename: The filename.
        """
        # Create the folder structure if necessary.
        folder = os.path.dirname(filename)
        if not os.path.isdir(folder):
            os.makedirs(folder)

        # Create the file.
        json_str = self.to_json()
        with open(filename, "w") as f:
            f.write(json_str)
