import pytest

from nertagger.annotators.gazetteers import GazetteersAnnotator, parse_gazetteers_directory


GAZETTEERS_DICT = {
    'first.lst': set(['Hello', 'Hello Bye', 'Hello Bye Chau']),
    'second.lst': set(['other', 'stAm'])
}


LOWERCASE_GAZETTEERS_DICT = {
    'first.lst': set(['hello', 'hello bye', 'hello bye chau']),
    'second.lst': set(['other', 'stam'])
}


def test_parse_gazetteers_directory(tmpdir):
    # create gazetteers directory
    gazetteers_dir = tmpdir.join('gazetters_dir')
    for gazetteer_name, gazetteer_words in GAZETTEERS_DICT.iteritems():
        gazetteer_file = gazetteers_dir.join(gazetteer_name)
        gazetteer_file.ensure()
        gazetteer_file.write('\r\n'.join(gazetteer_words), mode='wb')

    gazetteers, lowercase_gazetteers = parse_gazetteers_directory(str(gazetteers_dir))
    assert gazetteers == GAZETTEERS_DICT
    assert lowercase_gazetteers == LOWERCASE_GAZETTEERS_DICT


@pytest.mark.parametrize("sentence_text, expected_word_annotations", [
    # U-tag in different positions
    ("Hello",               [["U-first.lst", "U-first.lst(lower)"]]),
    ("HEllo",               [["U-first.lst(lower)"]]),
    ("x Hello",             [[], ["U-first.lst", "U-first.lst(lower)"]]),
    ("x Hello y",           [[], ["U-first.lst", "U-first.lst(lower)"], []]),

    # two words expression separated and joint
    ("Hello x Bye",         [["U-first.lst", "U-first.lst(lower)"], [], []]),
    ("Hello Bye",           [["U-first.lst", "U-first.lst(lower)", "B-first.lst", "B-first.lst(lower)"],
                             ["L-first.lst", "L-first.lst(lower)"]]),

    # three word expression
    ("hello bye chau",      [["U-first.lst(lower)", "B-first.lst(lower)", "B-first.lst(lower)"],
                             ["L-first.lst(lower)", "I-first.lst(lower)"],
                             ["L-first.lst(lower)"]]),

    # expression from the second gazetteer
    ("Other",                 [["U-second.lst(lower)"]]),
    ("Other hello",           [["U-second.lst(lower)"],
                               ["U-first.lst(lower)"]]),

])
def test_gazetteers_annotate(document_text_to_words, sentence_text, expected_word_annotations):
    annotator = GazetteersAnnotator(GAZETTEERS_DICT, LOWERCASE_GAZETTEERS_DICT)
    sentence_words = document_text_to_words(sentence_text)

    annotator.annotate_data(sentence_words)
    for word, word_expected_gazetteers in zip(sentence_words, expected_word_annotations):
        assert getattr(word, annotator.ANNOTATION_ATTRIBUTE) == word_expected_gazetteers
