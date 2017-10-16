from nertagger.features.utils import feature_func


@feature_func
def sentence_start(word):
    return word.sentence_index == 0
