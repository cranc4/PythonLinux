import random
import string
import yaml
import pytest as pytest
from sshcheckers import ssh_checkout, ssh_getout
from datetime import datetime

with open('folders.yaml') as f:
    data = yaml.safe_load(f)


@pytest.fixture()
def make_folder():
    return ssh_checkout(f'{data["ip"]}', data["user"], data["pswd"],
                        f'mkdir -p {data["folder_in"]} {data["folder_out"]} {data["folder_ext"]} '
                        f'{data["stat_file_dir"]}',
                        "")


@pytest.fixture()
def clear_folder():
    return ssh_checkout(data["ip"], data["user"], data["pswd"],
                        f'rm -rf {data["folder_in"]}/* {data["folder_out"]}/* {data["folder_ext"]}/* ',
                        "")



@pytest.fixture()
def make_files():
    list_files = []
    for i in range(data['count']):
        file_name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
        ssh_checkout(data["ip"], data["user"], data["pswd"], f'cd {data["folder_in"]}; dd if=/dev/urandom '
                                                             f'of={file_name} bs={data["bs"]} count=1 iflag=fullblock',
                     '')
        list_files.append(file_name)

    return list_files


@pytest.fixture()
def make_subfolder():
    subfolder_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    subfile_name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
    if not ssh_checkout(data["ip"], data["user"], data["pswd"], f'cd {data["folder_in"]}; mkdir {subfolder_name}',
                        ''):
        return None, None
    if not ssh_checkout(data["ip"], data["user"], data["pswd"], f'cd {data["folder_in"]}/{subfolder_name}; '
                    f'dd if=/dev/urandom of={subfile_name} bs={data["bs"]} count=1 iflag=fullblock', ''):
        return subfolder_name, None
    return subfolder_name, subfile_name


@pytest.fixture(autouse=True)
def print_time():
    print("Start: {}".format(datetime.now().strftime("%H:%M:%S.%f")))
    yield
    print(f'Finish: {datetime.now().strftime("%H:%M:%S.%f")}')


@pytest.fixture(autouse=True)
def stat_fixture():
    pass
    yield
    time_stamp = datetime.now().strftime("%H:%M:%S.%f")
    files_count = data["count"]
    file_size = data["bs"]
    cpu_stat = ssh_getout(data["ip"], data["user"], data["pswd"], f"cat /proc/loadavg")
    ssh_checkout(data["ip"], data["user"], data["pswd"], f'cd {data["stat_file_dir"]}; echo "time = {time_stamp}, '
                                                         f'files_count = {files_count}, file_size = {file_size}, '
                                                         f'cpu_stat = {cpu_stat}" >> stat.txt', '')


@pytest.fixture()
def start_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")