import pytest
import yaml
from chekers import checkout, getout
from datetime import datetime


with open('folders.yaml', encoding='utf-8') as f:
    data = yaml.safe_load(f)


@pytest.fixture()
def make_folder():
    yield checkout(f"mkdir -p {data['folder_in']} {data['folder_out']} {data['folder_ext']}", "")


@pytest.fixture()
def make_file():
    return checkout(f"cd {data['folder_in']}; touch file1.txt, file2.txt, file3.txt", "")


@pytest.fixture()
def del_folder():
    yield checkout(f"mkdir -p {data['folder_in']} {data['folder_out']} {data['folder_ext']}", "")
    checkout(f"rm -r {data['folder_in']} {data['folder_out']} {data['folder_ext']}", "")


@pytest.fixture(autouse=True)
def print_string():
    yield
    stat = stat = getout("cat /proc/loadavg")
    checkout(f"echo 'time: {datetime.now().strftime('%H:%M:%S.%f')} count:{data['count']} size: {data['bs']} "
             f"load: {stat}'>> stat.txt", "")