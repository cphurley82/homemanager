# -*- coding: utf-8 -*-
"""homemanager unit tests."""

import io

import homemanager


def test_get_host_names():
    """Ensure get_host_names() can extract names from a json file object."""
    assert homemanager.get_host_names_from_file(file=io.StringIO('''
        {
        "host_names": [
            // Domain names or IP addresses of the hosts being managed.
            "computer1.local",
            "192.168.42.42"
        ]
        }
        ''')) == ['computer1.local', '192.168.42.42']


def test_ping_host():
    """Ensure ping_host() returns True is host is pingable and Falso if not."""
    assert homemanager.ping_host('localhost') is True
    assert homemanager.ping_host('not.a.real.host') is False
