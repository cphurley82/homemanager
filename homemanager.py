# -*- coding: utf-8 -*-
"""homemanger makes managing home computers easier.

Currently all this does is ping the host and shuts it down if it responds.

Example:
    $ python3 homemanager.py
"""
import paramiko
import ping3
import keyring
import commentjson


def get_host_names_from_config():
    """Returns a list of host names read from configuration file."""
    with open('config.json', encoding='utf-8') as file:
        return get_host_names_from_file(file)
    return None


def get_host_names_from_file(file):
    """Returns a list of host names read from a configuration file object."""
    return commentjson.load(file)['host_names']


def get_password():
    """Returns the password from the keyring."""
    return keyring.get_password('system', 'homemanager')


def ping_host(host_name):
    """Pings a host and returns True if it responds."""
    print(f'Pinging {host_name}...', end='')
    response = ping3.ping(dest_addr=host_name)
    if response in [False, None]:
        print('no response.')
        return False
    print(f'response in {response} secs')
    return True


def main():
    """Main function."""
    # For each host, ping it and shutdown if it responds.
    for host_name in get_host_names_from_config():
        if ping_host(host_name):
            # SSH into the host using the password saved in the keyring.
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname=host_name,
                           username='chris',
                           password=get_password())

            # Execute the shutdown command.
            stdin, stdout, stderr = client.exec_command(
                'sudo -S shutdown -h now')

            # Provide the password to sudo.
            stdin.write(get_password() + "\n")
            stdin.flush()

            # Print the output from the shutdown command.
            # Sometimes the connection gets killed before anything comes out
            # so it prints nothing but still shuts down.
            print(f'STDOUT: {stdout.read().decode("utf8")}')

            # Close the SSH connection.
            client.close()

            # Close file objects.
            stdin.close()
            stdout.close()
            stderr.close()


if __name__ == '__main__':
    main()
