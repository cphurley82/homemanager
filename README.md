# homemanager

![Pylint](https://github.com/cphurley82/homemanager/actions/workflows/pylint.yml/badge.svg)

Makes managing technology at home easier.

Currently all this does is ping a list of hosts and shuts them down if they
respond.

## Setup

homemanager requires Python 3.6 or above and [some packages](requirements.txt)
which can be installed with pip like so:

```bash
pip install --requirement requirements.txt
```

homemanager is configured by creating a file called `config.json` in the working
directory. It looks like this:

```json
{
    "host_names": [
        // Domain names or IP addresses of the hosts being managed.
        "computer1.local",
        "192.168.42.42"
    ]
}
```

homemanager requires a password to be stored in the system keyring like so:

```bash
python -m keyring set system homemanager
```

Run homemanager like so:

```bash
python3 homemanager.py
```
