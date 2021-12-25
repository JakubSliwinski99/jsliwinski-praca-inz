import re
import csv
import string
from typing import List


def get_list_of_dirty_posts_with_reactions_likendin(file_name: str):
    file = open(file_name, "r", encoding="utf-8")
    text = file.read()
    found = re.findall(r'<span dir="ltr">(.*?)</span>|social-proof-fallback-number">(.*?)</span>|counts__reactions-count">(.*?)</span>', text)

    posts_with_reactions = []
    for i in range(len(found) - 1):
        if found[i][0] != '':
            if found[i + 1][1] != '':
                posts_with_reactions.append((found[i][0], found[i + 1][1]))
            if found[i + 1][2] != '':
                posts_with_reactions.append((found[i][0], found[i + 1][2]))

    return posts_with_reactions


def get_ready_list_of_posts_with_reactions_linkedin(file_name: str):
    dirty_list_of_posts_with_reactions = get_list_of_dirty_posts_with_reactions_likendin(file_name)

    final_list_of_posts_with_reactions = []

    for i in range(len(dirty_list_of_posts_with_reactions)):
        final_list_of_posts_with_reactions.append((clean_post(dirty_list_of_posts_with_reactions[i][0]), dirty_list_of_posts_with_reactions[i][1]))

    return final_list_of_posts_with_reactions


def get_ready_list_of_posts_and_indexes_facebook(file_name: str):
    file = open(file_name, "r", encoding="utf-8")
    text = file.read()

    found = re.findall(r'<div class="kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x c1et5uql ii04i59q">(.*?)</div></div></span>|<span class="pcp91wgn">(.*?)</span>|fe6kdd0r mau55g9w c8b282yb d3f4x2em iv3no6db jq4qci2q a3bd9o3v b1v8xokw m9osqain" dir="auto">(.*?)</span>', text)

    posts_reactions_comments = []

    for i in range(len(found) - 2):
        if found[i][0] != '' and found[i + 1][1] != '' and found[i + 2][2] != '':
            posts_reactions_comments.append([clean_post(found[i][0]), found[i + 1][1], clean_comment(found[i + 2][2])])

    return posts_reactions_comments


def clean_post(dirty_post: str) -> str:
    found_garbage = re.findall(r"<(.*?)>", dirty_post)
    sorted_garbage = sorted(found_garbage, key=len, reverse=True)
    #print(sorted_garbage)

    clean_post = remove_multiple_strings(dirty_post, sorted_garbage)
    pattern = re.compile('[^a-zA-ZąĄćĆęĘłŁńŃóÓśŚżŻźŹ1234567890.,!@:?() ]')

    return pattern.sub('', clean_post)


def clean_comment(comment: str) -> str:
    pattern = re.compile('[^1234567890]')
    return pattern.sub('', comment)


def remove_multiple_strings(cur_string: str, replace_list: List[str]) -> str:
    for cur_word in replace_list:
        cur_string = cur_string.replace('<' + cur_word + '>', ' ')
    return cur_string


final_list = get_ready_list_of_posts_with_reactions_linkedin("data_linkedin/linkedin_niebezpiecznik.txt")
for elem in final_list:
    print(elem)

print(len(final_list))
