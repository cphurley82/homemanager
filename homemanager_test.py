import homemanager
import io
import keyring


def test_get_host_names():
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
    assert homemanager.ping_host('localhost') == True
    assert homemanager.ping_host('not.a.real.host') == False