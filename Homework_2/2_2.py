# Установить пакет для расчёта crc32
# sudo apt install libarchive-zip-perl
# Доработать проект, добавив тест команды расчёта хеша (h).
# Проверить, что хеш совпадает с рассчитанным командой crc32.

from checkers import checkout, getout

hm_2 = "/home/user/PycharmProjects/Autotests/hm_2_pytest/"

def test_7z_h():
    crc32_hash = getout(f'cd {hm_2}; crc32 checkers.py').upper()
    assert checkout(f'cd {hm_2}; 7z h checkers.py', crc32_hash), "test_h FAIL"