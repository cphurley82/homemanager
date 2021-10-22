import paramiko
import ping3
import keyring
import commentjson


def get_host_names():
    with open('config.json') as f:
        data = commentjson.load(f)
    return data['host_names']


def get_password():
    return keyring.get_password('system', 'homeadmin')


def main():
    for host_name in get_host_names():
        print(f'Pinging {host_name}...', end='')
        response = ping3.ping(dest_addr=host_name)
        if response == False:
            print(f'no response.')
        else:
            print(f'resonse in {response} secs, shutting it down...')
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname=host_name,
                           username='chris',
                           password=get_password())
            stdin, stdout, stderr = client.exec_command(
                'sudo -S shutdown -h now')

            stdin.write(get_password() + "\n")
            stdin.flush()

            print(f'STDOUT: {stdout.read().decode("utf8")}')
            # print(f'STDERR: {stderr.read().decode("utf8")}')

            # Because they are file objects, they need to be closed
            stdin.close()
            stdout.close()
            stderr.close()

            client.close()


if __name__ == '__main__':
    main()
