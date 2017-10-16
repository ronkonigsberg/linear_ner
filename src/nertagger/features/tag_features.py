from collections import Counter

from nertagger.features.utils import feature_func


@feature_func
def prev_tag(word):
    if word.sentence_index >= 1:
        return word.sentence[word.sentence_index-1].tag


@feature_func
def prev_prev_tag(word):
    if word.sentence_index >= 2:
        return word.sentence[word.sentence_index-2].tag


@feature_func
def prev_tag_pattern(word):
    sentence = word.sentence

    if word.sentence_index >= 2:
        if sentence[word.sentence_index-1].tag == 'O':
            if sentence[word.sentence_index-2].tag != 'O':
                return (sentence[word.sentence_index-2].tag[2:] + "_" +
                        sentence[word.sentence_index-1].text)
            elif word.sentence_index >= 3 and sentence[word.sentence_index-3].tag != 'O':
                return (sentence[word.sentence_index-3].tag[2:] + "_" +
                        sentence[word.sentence_index-2].text + "_" +
                        sentence[word.sentence_index-1].text)


@feature_func
def context_prev_tag(word):
    document = word.document

    window = list()
    window.append((word, list()))
    if (word.document_index+1) < len(document):
        window.append((document[word.document_index+1], list()))
    if (word.document_index+2) < len(document):
        window.append((document[word.document_index+2], list()))

    context_start_index = max(0, word.document_index-1000)
    for i in xrange(context_start_index, word.document_index):
        current_word = document[i]
        for (window_word, tag_list) in window:
            if window_word.text == current_word.text:
                tag_list.append(current_word.tag)

    feature_list = list()
    for offset, (window_word, tag_list) in enumerate(window):
        tag_counter = Counter(tag_list)
        for tag, count in tag_counter.iteritems():
            tag_freq_category = int(3*float(count) / len(tag_list))
            feature = "%d_%s_%d" % (offset, tag, tag_freq_category)
            feature_list.append(feature)
    return feature_list
