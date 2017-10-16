import re
from functools import wraps

from nertagger.features.utils import feature_func


def text_feature_func(func):
    @feature_func
    @wraps(func)
    def call_function_with_word_text(word):
        return func(word.text)

    return call_function_with_word_text


@text_feature_func
def capitalized(word_text):
    return word_text.istitle()


@text_feature_func
def all_letters_capitalized(word_text):
    return word_text.isalpha() and word_text.isupper()


@text_feature_func
def all_digits(word_text):
    return word_text.isdigit()


@text_feature_func
def all_non_letters(word_text):
    for ch in word_text:
        if ch.isalpha():
            return False
    return True


@text_feature_func
def text(word_text):
    return word_text


@text_feature_func
def normalized_digits(word_text):
    #TODO: add date normalization
    #TODO: maybe return original string if no changes occured
    normalized_text = re.sub('[0-9]+', '*D*', word_text)
    if normalized_text != word_text:
        return normalized_text


@text_feature_func
def prefixes(word_text):
    prefix_list = list()
    for prefix_len in [3, 4]:
        if prefix_len <= len(word_text):
            prefix_list.append(word_text[:prefix_len])
    return prefix_list


@text_feature_func
def suffixes(word_text):
    suffix_list = list()
    for suffix_len in [1, 2, 3, 4]:
        if suffix_len <= len(word_text):
            suffix_list.append(word_text[len(word_text)-suffix_len:])
    return suffix_list
