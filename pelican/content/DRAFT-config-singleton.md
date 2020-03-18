Title: A Singleton Config Class in Python
Date: 2020-03-10 22:00
Category: Python
Tags: python, programming, patterns, design patterns, registry, computer science
Status: draft

[TOC]

# Overview

In this post we cover a strategy for managing configurations for programs using
a Singleton pattern to create a static `Config` class.

This allows the user to create an instance of the `Config` class, pointing it
to a specific config file, which it loads into memory.

The `Config` class provides several static methods for accessing configuration
options from the config file. Here's an example of its usage:

```
Config('/path/to/config.json')

if Config.get_foo() == "bar":
    do_stuff()
```

The principle is to **define one configuration file location, and be done with it.**
The configuration file is JSON formatted, but the pattern can be adapted to use
any format.

The `Config` class can also be used to wrap and process both variables in the configuration
file _and_ environment variables.

The `Config` class implements a **separation of concerns** by only processing top-level
configuration variable options, and leaving more detailed configuration file parsing
to the classes that need it. This allows for more flexible config files.

# The Singleton Pattern

The Singleton pattern involves the use of instance variables, which the variables
`_CONFIG_FILE` and `_CONFIG` are. These are shared across all instances of class
`Config` and can be accessed via `Config._CONFIG_FILE`, etc.

The constructor starts by checking that the configuration file exists, then loads
the configuration file into memory (at `Config._CONFIG` as a dictionary):

```python
class Config(object):
    _CONFIG_FILE: typing.Optional[str] = None
    _CONFIG: typing.Optional[dict] = None

    def __init__(self, config_file = None):
        if config_file is None:
            config_file = Config.get_required_env_var("CENTILLION_CONFIG")

        # Check that specified config file exists
        assert os.path.exists(config_file)

        # Use singleton pattern to store config file location/load config once
        Config._CONFIG_FILE = config_file
        with open(config_file, 'r') as f:
            Config._CONFIG = json.load(f)

    @staticmethod
    def get_config_file() -> str:
        return Config._CONFIG_FILE
```

Aside from the constructor, every method in the `Config` class is a
`@staticmethod` or a `@classmethod`.

# Get Variable Functions

We add two additional methods to get configuration variables: one to get variables
from the config file, one to get environment variables. Here they are:

```python
class Config(object):

    ...

    @staticmethod
    def get_required_env_var(envvar: str) -> str:
        if envvar not in os.environ:
            raise CentillionConfigException("Please set the {envvar} environment variable")
        return os.environ[envvar]

    @staticmethod
    def get_required_config_var(configvar: str) -> str:
        assert Config._CONFIG
        if configvar not in Config._CONFIG:
            raise CentillionConfigException(f"Please set the {configvar} variable in the config file {Config._CONFIG_FILE}")
        return Config._CONFIG[configvar]
```

# Config Functions






