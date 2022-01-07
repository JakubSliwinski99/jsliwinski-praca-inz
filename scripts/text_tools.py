import re
from typing import List


def clean_post(dirty_post: str) -> str:
    found_garbage = re.findall(r"<(.*?)>", dirty_post)
    sorted_garbage = sorted(found_garbage, key=len, reverse=True)

    clean_post = remove_multiple_strings(dirty_post, sorted_garbage)
    pattern1 = re.compile('[^a-zA-ZąĄćĆęĘłŁńŃóÓśŚżŻźŹ1234567890.,!@:?()/ ]')
    pattern2 = re.compile(' +')
    pattern3 = re.compile('/')

    first_clean = pattern1.sub('', clean_post)
    second_clean = pattern2.sub(' ', first_clean)
    third_clean = pattern3.sub(' ', second_clean)

    return third_clean


def remove_multiple_strings(cur_string: str, replace_list: List[str]) -> str:
    for cur_word in replace_list:
        cur_string = cur_string.replace('<' + cur_word + '>', ' ')
    return cur_string


def clean_string_to_int(string_with_numbers: str) -> int:
    pattern = re.compile('[^1234567890]')
    number = pattern.sub('', string_with_numbers)
    return int(number)