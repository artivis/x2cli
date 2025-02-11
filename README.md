# x2cli

`x2cli` is a template, and its accompanying script,
to kickstart creating Python3 cli tools.
The template is based off [ros2cli](https://github.com/ros2/ros2cli).

## Install

Install it from the snap store:

```bash
snap install x2cli
```

or from source,

```bash
python3 -m pip install .
```

## Use

To kick a new project called `map` (standing for 'My Awesome Project'),
issue the command:

```bash
x2cli map
```

This creates the `mapcli` project in the current directory,
which is ready to use:

```bash
$ python3 -m pip install ./mapcli
$
$ mapcli -h
usage: mapcli [--use-python-default-buffering] [-v] [-h] Call `mapcli <command> -h` for more detailed usage. ...

mapcli is an extensible command-line tool for .

options:
  --use-python-default-buffering
                        Do not force line buffering in stdout and instead use the python default buffering, which might be affected by PYTHONUNBUFFERED/-u and depends on whatever stdout is interactive or not
  -v, --verbose         Increase verbosity.
  -h, --help            Show this help message and exit.

Commands:

  Call `mapcli <command> -h` for more detailed usage.
```

### Help

```bash
usage: x2cli [-h] [-o OUTPUT_DIR] [--no-suffix] project_name

positional arguments:
  project_name          The project name.

options:
  -h, --help            show this help message and exit
  -o OUTPUT_DIR, --output-dir OUTPUT_DIR
                        The output directory for the project. Default to current path.
  --no-suffix           Do not add the 'cli' suffix to the project name.
```

Happy tooling !
