import re
import spacy

from scripts import text_tools


def create_basic_facebook_data(file_path):
    file = open(file_path, "r", encoding="utf-8")
    text = file.read()

    # Find list of elements to scrape data from
    found = re.findall(r'<div class="kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x c1et5uql ii04i59q">(.*?)</div></div></span>|label="Lubię to!:(.*?)class|label="Super:(.*?)class|label="Trzymaj się:(.*?)class|label="Ha ha:(.*?)class|label="Wow:(.*?)class|label="Przykro mi:(.*?)class|label="Wrr:(.*?)class|<span class="pcp91wgn">(.*?)</span>|fe6kdd0r mau55g9w c8b282yb d3f4x2em iv3no6db jq4qci2q a3bd9o3v b1v8xokw m9osqain" dir="auto">(.*?)</span>', text)

    # Create list for every kind of reaction
    list_posts = []
    list_lubie_to = []
    list_super = []
    list_trzymaj_sie = []
    list_haha = []
    list_wow = []
    list_przykro_mi = []
    list_wrr = []
    list_all_reactions = []
    list_comments = []

    # Populate each list
    for i in range(len(found)):
        if found[i][0] != '':
            post = text_tools.clean_post(found[i][0])
            lubie_to = '0'
            superr = '0'
            trzymaj_sie = '0'
            haha = '0'
            wow = '0'
            przykro_mi = '0'
            wrr = '0'
            all_reactions = '0'
            comments = '0'
            j = 1
            while comments == '0':
                this_row = found[i + j]
                if this_row[1] != '':
                    lubie_to = this_row[1]
                elif this_row[2] != '':
                    superr = this_row[2]
                elif this_row[3] != '':
                    trzymaj_sie = this_row[3]
                elif this_row[4] != '':
                    haha = this_row[4]
                elif this_row[5] != '':
                    wow = this_row[5]
                elif this_row[6] != '':
                    przykro_mi = this_row[6]
                elif this_row[7] != '':
                    wrr = this_row[7]
                elif this_row[8] != '':
                    all_reactions = this_row[8]
                elif this_row[9] != '':
                    comments = this_row[9]
                j += 1

            list_posts.append(post)
            list_lubie_to.append(text_tools.clean_string_to_int(lubie_to))
            list_super.append(text_tools.clean_string_to_int(superr))
            list_trzymaj_sie.append(text_tools.clean_string_to_int(trzymaj_sie))
            list_haha.append(text_tools.clean_string_to_int(haha))
            list_wow.append(text_tools.clean_string_to_int(wow))
            list_przykro_mi.append(text_tools.clean_string_to_int(przykro_mi))
            list_wrr.append(text_tools.clean_string_to_int(wrr))
            list_all_reactions.append(text_tools.clean_string_to_int(all_reactions))
            list_comments.append(text_tools.clean_string_to_int(comments))

    # Return a dictionary containing data
    finished_dictionary = {
        'POSTS': list_posts,
        'LUBIE_TO': list_lubie_to,
        'SUPER': list_super,
        'TRZYMAJ_SIE': list_trzymaj_sie,
        'HAHA': list_haha,
        'WOW': list_wow,
        'PRZYKRO_MI': list_przykro_mi,
        'WRR': list_wrr,
        'ALL_REACTIONS': list_all_reactions,
        'COMMENTS': list_comments
    }

    return finished_dictionary


def combine_multiple_facebook_data(list_of_paths):
    list_of_dictionaries = []
    for path in list_of_paths:
        dictionary_for_file = create_basic_facebook_data(path)
        list_of_dictionaries.append(dictionary_for_file)

    final_dictionary = list_of_dictionaries[0]

    if len(list_of_dictionaries) == 1:
        return final_dictionary

    for i in range(1, len(list_of_dictionaries)):
        final_dictionary['POSTS'] += list_of_dictionaries[i]['POSTS']
        final_dictionary['LUBIE_TO'] += list_of_dictionaries[i]['LUBIE_TO']
        final_dictionary['SUPER'] += list_of_dictionaries[i]['SUPER']
        final_dictionary['TRZYMAJ_SIE'] += list_of_dictionaries[i]['TRZYMAJ_SIE']
        final_dictionary['HAHA'] += list_of_dictionaries[i]['HAHA']
        final_dictionary['WOW'] += list_of_dictionaries[i]['WOW']
        final_dictionary['PRZYKRO_MI'] += list_of_dictionaries[i]['PRZYKRO_MI']
        final_dictionary['WRR'] += list_of_dictionaries[i]['WRR']
        final_dictionary['ALL_REACTIONS'] += list_of_dictionaries[i]['ALL_REACTIONS']
        final_dictionary['COMMENTS'] += list_of_dictionaries[i]['COMMENTS']

    return final_dictionary


def get_list_of_preprocessed_posts(list_of_posts, nlp):
    list_preprocessed_posts = []

    for post in list_of_posts:
        doc = nlp(post)

        clean_text = " ".join(token.lemma_ for token in nlp(doc) if token.lemma_.lower() not in nlp.Defaults.stop_words and token.is_alpha)
        list_preprocessed_posts.append(clean_text)

    return list_preprocessed_posts


def get_list_of_polarity(list_of_posts, nlp):
    list_all_polarity = []

    for post in list_of_posts:
        doc = nlp(post)
        list_all_polarity.append(doc._.polarity)

    return list_all_polarity


def get_list_of_subjectivity(list_of_posts, nlp):
    list_all_subjectivity = []

    for post in list_of_posts:
        doc = nlp(post)
        list_all_subjectivity.append(doc._.subjectivity)

    return list_all_subjectivity






