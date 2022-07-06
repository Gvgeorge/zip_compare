'''
Запуск: python compare_zip.py zipfile1.zip zipfile2.zip
'''

import sys
from typing import NamedTuple
from zipfile import ZipFile, ZipInfo, BadZipFile


class ZippedFileInfo(NamedTuple):
    full_name: str
    CRC: int


def _get_zip_item_set(zipfile_name: str) -> set[ZippedFileInfo]:
    result = set()
    with ZipFile(zipfile_name) as zfile:
        for item in zfile.namelist():
            if ZipInfo(item).is_dir():
                continue
            file_info = zfile.getinfo(item)
            result.add(ZippedFileInfo(file_info.filename, file_info.CRC))
    return result


def compare_zip_item_sets(first_zipfile_name: str, second_zipfile_name: str) -> None:
    '''
    Файлы выводятся в случайном порядке, так как иного не требовалось.
    '''
    first_item_set = _get_zip_item_set(first_zipfile_name)
    second_item_set = _get_zip_item_set(second_zipfile_name)

    identical_items = first_item_set.intersection(second_item_set)
    if not identical_items:
        print('No identical items.')
    else:
        print('Identical:')
        for item in identical_items:
            print(item.full_name)

    print()

    unique_set_first = first_item_set.difference(second_item_set)
    if not unique_set_first:
        print(f'No unique files in {first_zipfile_name}')
    else:
        print(f'Unique for {first_zipfile_name}:')
        for item in unique_set_first:
            print(item.full_name)

    print()

    unique_set_second = second_item_set.difference(first_item_set)
    if not unique_set_second:
        print(f'No unique files in {second_zipfile_name}')
    else:
        print(f'Unique for {second_zipfile_name}:')
        for item in unique_set_second:
            print(item.full_name)


if __name__ == '__main__':
    try:
        first_zipfile_name = sys.argv[1]
        second_zipfile_name = sys.argv[2]
    except IndexError:
        print('Неправильный формат вызова скрипта.')
        print('Правильный: python compare_zip.py file_name_1 file_name_2')
        sys.exit()
    try:
        compare_zip_item_sets(first_zipfile_name, second_zipfile_name)
    except FileNotFoundError:
        print('Не удалось найти один из файлов, возможно вы забыли добавить',
              'окончание .zip?')
        sys.exit()
    except BadZipFile:
        print('Не удалось обработать один из файлов')
    except:
        print('Что-то пошло не так')
        sys.exit()