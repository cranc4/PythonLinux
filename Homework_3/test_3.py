from chekers import checkout, getout
import yaml
import pytest


with open('folders.yaml', encoding='utf-8') as f:
    data = yaml.safe_load(f)


class TestPositive:
    def test_step4(self, make_folder, make_file):
        # архивировать папку
        assert checkout(f"cd {data['folder_in']}; 7z a {data['folder_out']}arh -t{data['type']}", "Everything is Ok"), \
            "test4 FAIL"


    def test_step5(self, make_folder, make_file):
        # удалить папку/файл
        assert checkout(f"cd {data['folder_out']}; 7z d ./arh.{data['type']} file1.txt", "Everything is Ok"), "test5 FAIL"


    def test_step6(self, make_folder, make_file):
        # показать файлы в папке не запуская
        assert checkout(f"cd {data['folder_out']}; 7z l ./arh.{data['type']}", "Listing archive: ./arh.7z"), "test6 FAIL"


    def test_step7(self, make_folder, make_file):
        # проверить, что хеш совпадает с рассчитанным командой crc32
        res = checkout(f"cd {data['folder_in']}; 7 h file1.txt", "Everything is Ok")
        crc32_h = getout(f"cd {data['folder_in']}; crc32 test1.txt").upper()
        res2 = checkout(f"cd {data['folder_in']}; 7z h file1.txt", crc32_h)
        assert res and res2, "test7 FAIL"


    def test_step8(self, make_folder, make_file):
        # разархивировать файлы из папки
        assert checkout(f"cd {data['folder_ext']}; 7z x {data['folder_out']} -y", "Everything is Ok"), \
            "test8 FAIL"


if __name__ == '__main__':
    pytest.main(['-vv'])