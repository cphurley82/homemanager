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


def get_host_names():
    """Returns a list of host names read from configuration file."""
    with open('config.json', encoding='utf-8') as file:
        data = commentjson.load(file)
    return data['host_names']


def get_password():
    """Returns the password from the keyring."""
    return keyring.get_password('system', 'homemanager')


def main():
    """Main function."""
    # For each host, ping it and shutdown if it responds.
    for host_name in get_host_names():
        print(f'Pinging {host_name}...', end='')
        response = ping3.ping(dest_addr=host_name)
        if response in [False, None]:
            print('no response.')
        else:
            print(f'response in {response} secs, shutting it down...')

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
