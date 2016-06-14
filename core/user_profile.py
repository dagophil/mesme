import logging


class UserProfile(object):
    """
    The UserProfile class stores user specific data, for example the location of the database file.
    """

    @staticmethod
    def from_dict(d):
        """
        Create a user profile from the given dict.
        :param d: The dict.
        :return: Returns the user profile.
        """
        profile = UserProfile()
        for key, value in d.items():
            profile[key] = value
        return profile

    def __init__(self):
        """
        Create a user profile with uninitialized fields.
        """
        self.settings = {
            "database_user_id": "",
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
            raise IndexError("Invalid profile setting: " + name)

    def __str__(self):
        """
        Convert the settings dict to a string.
        :return: Returns the string representation of the settings dict.
        """
        return str(self.settings)

    def to_dict(self):
        """
        Convert the user profile to a dict.
        :return: The profile dict.
        """
        return self.settings


class UserProfileCollection(object):
    """
    The UserProfileCollection can load and save user profiles.
    """

    @staticmethod
    def from_dict(d):
        """
        Create a UserProfileCollection from the given dict.
        :param d: The dict.
        :return: Returns the created UserProfileCollection.
        """
        assert isinstance(d, dict)
        profiles = UserProfileCollection()
        for name, value in d.items():
            if isinstance(value, UserProfile):
                profiles[name] = value
            elif isinstance(value, dict):
                profiles[name] = UserProfile.from_dict(value)
            else:
                raise TypeError("Value has invalid type: " + value.__class__.__name__)
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
        if isinstance(value, UserProfile):
            self.user_profiles[key] = value
        else:
            raise TypeError("The UserProfileCollection can only store UserProfile objects.")

    def __delitem__(self, key):
        """
        Remove the user profile with the given name.
        :param key: The profile name.
        """
        del self.user_profiles[key]

    def to_dict(self):
        """
        Convert the profile collection to a dict.
        :return: The profile collection dict.
        """
        return self.user_profiles

    def items(self):
        """
        Return (name, profile) pairs of the stored profiles.
        :return:
        """
        return self.user_profiles.items()

    def names(self):
        """
        Return a list of the existing user names.
        :return: Returns a list of the existing user names.
        """
        return list(self.user_profiles.keys())

    def db_locations(self):
        """
        Return a list of the existing database locations.
        :return: Returns a list of the existing database locations.
        """
        return [profile["database_location"] for profile in self.user_profiles.values()]
