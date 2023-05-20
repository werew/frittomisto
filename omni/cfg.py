"""
Module to manage config files
"""
from typing import Any, Dict, Optional, TextIO, Union, List
from pathlib import Path
import toml

class Omnicfg:
    """
    Class to manage the omni config files.
    The config file is a TOML file, and the default name is omni.toml and it 
    is searched for in the current directory and its parents.

    The API of this class is similar to the one of python Dicts: 
    - cfg['key'] has a similar effect to dict['key']
    - cfg.get('key', default) has a similar effect to dict.get('key', default)

    It is possible to modify the behaviour of this class by calling the
    "set_" methods. For example, to set the config file to use, call 
    set_config_file('path/to/config.toml').
    """
    def __init__(self):
        self._config : Dict[str, Any] = None
        self._config_names : List[str] = ['omni.toml']
        self._config_file = None
        self._should_monitor = False
        self._last_modified = None

    def set_config_file(self, config_file: str) -> None:
        """
        Set the config file to use
        """
        self._config_file = config_file

    def set_config_names(self, config_names: Union[str, list]):
        """
        Set the config names to search for, in order of priority.
        The default is ['omni.toml']
        """
        if not config_names:
            raise ValueError("config_names must be a non-empty string or list")
        elif isinstance(config_names, str):
            config_names = [config_names]

        self._config_names = config_names

    def get_config_names(self) -> List[str]:
        """
        Get the config names to search for, in order of priority.
        The default is ['omni.toml']
        """
        return self._config_names

    def set_should_monitor(self, should_monitor: bool) -> None:
        """
        Set whether the config file should be monitored for changes
        """
        self._should_monitor = should_monitor

    def reload(self):
        """
        Reload the config from the config file
        """
        self._config = self._reload_config()

    def get(self, key, default=None):
        """
        Get a config value
        """
        return self._get_config().get(key, default)
    
    def __getitem__(self, __name: str) -> Any:
        """
        Get a config value
        """
        return self._get_config()[__name]

    def __setitem__(self, __name: str, __value: Any) -> None:
        raise NotImplementedError("Setting config values is not yet implemented")
    
    def _get_config(self) -> Dict[str, Any]:

        # Find the config file if it hasn't been found yet
        if self._config_file is None:
            self._config_file = self._find_config()

        # Reload the config if it should be monitored
        if self._should_monitor:
            raise NotImplementedError("Monitoring config file for changes is not yet implemented")

        if self._config is None:
            self._config = self._reload_config()

        return self._config

    def _reload_config(self) -> Dict[str, Any]:
        with open(self._config_file) as f:
            config = toml.load(f)
        return config

    def _find_config(self) -> str:
        """
        Find config file in the current directory or its parents
        """
        for directory in [Path("."), *Path(".").absolute().parents]:
            for name in self._config_names:
                if (directory / name).exists():
                    return str(directory / name)

        raise FileNotFoundError(f"Could not find config file in current directory or its parents")
    
cfg = Omnicfg()