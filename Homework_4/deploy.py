from sshcheckers import ssh_checkout, upload_files
import yaml


with open("folders.yaml", encoding='utf-8') as f:
    data = yaml.safe_load(f)


def deploy():
    res = []
    upload_files(f"{data['ip']}", f"{data['user']}", f"{data['pswd']}",
                 f"/home/user/tests/{data['pkgname']}.deb",
                 f"/home/user2/{data['pkgname']}.deb")
    res.append(ssh_checkout(f"{data['ip']}", f"{data['user']}", f"{data['pswd']}",
                 f"echo {data['pswd']} | sudo -S dpkg -i /home/user2/{data['pkgname']}.deb",
                            "Настраивается пакет"))
    res.append(ssh_checkout(f"{data['ip']}", f"{data['user']}", f"{data['pswd']}",
                            f"echo {data['pswd']} | sudo -S dpkg -s {data['pkgname']}",
                            "Status: install ok installed"))

    return all(res)


if deploy():
    print("Деплой успешен")
else:
    print("Ошибка деплоя")