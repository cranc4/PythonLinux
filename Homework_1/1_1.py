# Написать функцию на Python, которой передаются в качестве параметров команда и текст.
# Функция должна возвращать True, если команда успешно выполнена и текст найден в её выводе
# и False в противном случае. Передаваться должна только одна строка, разбиение вывода использовать не нужно.

import subprocess


def is_command_successful(command, text_to_find):
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    print(result.stdout)
    return text_to_find in result.stdout


command_example = "ls -l"
text_example = "README.md"
result = is_command_successful(command_example, text_example)

print(result)