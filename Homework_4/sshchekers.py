import paramiko
import yaml


def ssh_checkout(host, user, psswd, cmd, text, port=22):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=user, password=psswd, port=port)
    stdin, stdout, stderr = client.exec_command(cmd)
    exit_code = stdout.channel.recv_exit_status()
    out = (stdout.read() + stderr.read()).decode("utf-8")
    # print(out)
    client.close()
    if text in out and exit_code == 0:
        return True
    else:
        return False


def upload_files(host, user, psswd, local_path, remote_path, port=22):
    print(f"Загружаем {local_path} файл в каталог {remote_path}.")
    transport = paramiko.Transport((host, port))
    transport.connect(None, username=user, password=psswd)
    sftp = paramiko.SFTPClient.from_transport(transport)
    sftp.put(local_path, remote_path)
    if sftp:
        sftp.close()
    if transport:
        transport.close()


def ssh_getout(host, user, passwd, cmd, port=22):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=user, password=passwd, port=port)
    stdin, stdout, stderr = client.exec_command(cmd)
    out = (stdout.read() + stderr.read()).decode("utf-8")
    client.close()
    return out


def download_files(host, user, passwd, remote_path, local_path, port=22):
    print(f"Скачиваем файл {remote_path} в каталог {local_path}")
    transport = paramiko.Transport((host, port))
    transport.connect(None, username=user, password=passwd)
    sftp = paramiko.SFTPClient.from_transport(transport)
    sftp.get(remote_path, local_path)
    if sftp:
        sftp.close()
    if transport:
        transport.close()


if __name__ == "__main__":
    with open('folders.yaml') as f:
        data = yaml.safe_load(f)

    download_files(data["ip"], data["user"], data["pswd"], f"{data['stat_file_dir']}/stat.txt",
                   "stat.txt" )