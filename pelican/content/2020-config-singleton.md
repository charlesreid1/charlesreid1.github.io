Title: A Singleton Configuration Class in Python
Date: 2020-04-28 16:00
Category: Python
Tags: python, programming, patterns, design patterns, registry, computer science

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

The location of the config file can be set in the constructor,
or can be provided via the `CONFIG_FILE` environment variable.
The config class also provides a method for accessing environment
variables that are required by the Config class, and raising a
custom exception if it is not present.

The constructor starts by checking that the configuration file exists, then loads
the configuration file into memory (at `Config._CONFIG` as a dictionary):

```python
class Config(object):

    #########################
    # Begin Singleton Section
    #########################

    _CONFIG_FILE: typing.Optional[str] = None
    _CONFIG: typing.Optional[dict] = None

    def __init__(self, config_file = None):
        if config_file is None:
            config_file = Config.get_required_env_var("CONFIG_FILE")

        # Check that specified config file exists
        assert os.path.exists(config_file)

        # Use singleton pattern to store config file location/load config once
        Config._CONFIG_FILE = config_file
        with open(config_file, 'r') as f:
            Config._CONFIG = json.load(f)

    @staticmethod
    def get_config_file() -> str:
        return Config._CONFIG_FILE

    @staticmethod
    def get_required_env_var(envvar: str) -> str:
        if envvar not in os.environ:
            raise ConfigException(f"Please set the {envvar} environment variable")
        return os.environ[envvar]
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
            raise Exception("Please set the {envvar} environment variable")
        return os.environ[envvar]

    @staticmethod
    def get_required_config_var(configvar: str) -> str:
        assert Config._CONFIG
        if configvar not in Config._CONFIG:
            raise Exception(f"Please set the {configvar} variable in the config file {Config._CONFIG_FILE}")
        return Config._CONFIG[configvar]
```

We saw the get_required_env_var()` function in action in the constructor.
The `get_required_config_var()` can be useful for config variables that
are dependent on other config variables.

# Config Functions

Continuing with the `Config` class defined above,
we now define methods that implement logic for specific 
configuration variables.

Here are two example config variables.

The variable `foo` is set using the configuration file.
The configuration file is a dictionary, meaning it consists
of key-value pairs, so the variable `foo` is set by the value
corresponding to the `foo` key in the config file.

For example, using the following simple configuration file:

```plain
{
    "foo": "hello world"
}
```

if the `Config` class is initialized with that configuration file,
`Config.get_foo_var()`  will return the string `hello world`.

Similarly, the `bar`variable is set using the environment variable `BAR`.
If the `BAR` variable is not set, the program will raise an exception
when `Config.get_bar_var()` is called.

```python
class Config(object):

    ...see singleton section above...

    #############################
    # Begin Configuration Section
    #############################

    _FOO: typing.Optional[str] = None
    _BAR: typing.Optional[str] = None

    @classmethod
    def get_foo_var(cls) -> str:
        """Example variable that is set in the config file (preferred)"""
        if cls._FOO is None:
            cls._FOO = Config.get_required_config_var('foo')
        return cls._FOO

    @classmethod
    def get_bar_var(cls) -> str:
        """Example variable that is set via env var (not preferred)"""
        if cls._BAR is None:
            cls._BAR = Config.get_required_env_var('BAR')
        return cls._BAR

    @classmethod
    def get_wuz(cls) -> str:
        if cls._WUZ is None:
            if 'wuz' not in cls._CONFIG:
                cls._WUZ = Config.get_required_env_var('WUZ')
            else:
                cls._WUZ = cls._CONFIG['wuz']
        if not os.path.isdir(cls._WUZ):
            raise Exception(f"Error: Path {cls._WUZ} is not a directory")
        return cls._WUZ
```

The `wuz` variable, in this example, is a variable that can be set with a config
file variable, or (if it is not present in the config file) with an environment
variable. The `wuz` variable msut also be a path, so there is logic for checking
whether the path exists.

# Reset method

It can be useful to clear out an existing config file in order to
load a new config file - specifically, when testing. Here we define a `reset()`
method that clears out variable values. We will show an example of how to
use the `reset()` method below.

```
    @classmethod
    def reset(cls) -> None:
        cls._CONFIG_FILE = None
        cls._CONFIG = None
        cls._FOO = None
        cls._BAR = None
        cls._WUZ = None
```

This could be done more gracefully by iterating over each attribute of the Config class
and only nullifying those attributes whose variable name matches the given pattern (start
with an underscore, only contain capital letters and underscores) using a regular expression.

# Creating a configuration context manager

To make tests more convenient, we define a context manager that takes
a dictionary as an input. The context manager creates a temporary file
with the contents of that dictionary, and resets the Config class using
the temporary file as the new config file. This allows tests to be written
using different configurations on the fly, very useful when testing
different configuration options:

```python
cfg = {"peanut_butter": "jelly"}
with TempConfig(cfg) as config_file:
    print(f"Temporary configuration file is at {config_file}")
    val = Config.get_required_config_var("peanut_butter")
    assert val=="jelly"
```

Here is the context manager class to temporarily replace the configuration
wrapped by the `Config` class:

```python
class TempConfig(object):
    """
    Temporarily patch the Config class to use the config
    dictionary specified in the constructor.
    """

    def __init__(self, config_dict, *args, **kwargs):
        """This is the step that's run when object constructed"""
        super().__init__()
        # This is the temp configuration the user specified
        self.config_dict = config_dict
        # Make a temp dir for our temp config file
        self.temp_dir = tempfile.mkdtemp()
        # Make a temp config file
        _, self.temp_json = tempfile.mkstemp(suffix=".json", dir=self.temp_dir)
        # Set the wuz variable to the temporary directory
        self.config_dict['wuz'] = self.temp_dir

    def __enter__(self, *args, **kwargs):
        """This is what's returned to the "as X" portion of the context manager"""
        self._write_config(self.temp_json, json.dumps(self.config_dict))
        # Re-init Config with new config file
        Config(self.temp_json)
        return self.temp_json

    def __exit__(self, *args, **kwargs):
        """
        Close the context and clean up; the *args are needed in case there is
        an exception (we don't deal with those here)
        """
        # Delete temp file
        os.unlink(self.temp_json)
        # Delete temp dir
        shutil.rmtree(self.temp_dir)
        # Reset all config variables
        Config.reset()

    def _write_config(self, target: str, contents: str):
        """Utility method: write string contents to config file"""
        with open(target, "w") as f:
            f.write(contents)
```

# Next steps

That's it for now. This singleton configuration class is being written into a
new version of [centillion](https://charlesreid1.github.io/centillion-a-document-search-engine.html),
which will be [centillion version 2.0](https://github.com/chmreid/centillion/pull/3).
This is still a pull request in a centillion fork, though, so it's a work in progress.
Stay tuned!
