from mock import Mock

from nertagger.annotators.prev_level_aggregator import (Entity, ANNOTATION_ATTRIBUTE, QUANTIZATION,
                                                        _extract_document_entities, _get_word_features,
                                                        annotate_prev_level_entities)


def test_extract_document_entities(document_text_to_words):
    document_text = "Mike visited London with Jack and John Doe\n" \
                    "Jack loves Paris New York and Moscow more than London"
    document_labels = ['I-PER', 'O', 'I-LOC', 'O', 'I-PER', 'O', 'I-PER', 'I-PER',
                       'B-PER', 'O', 'I-LOC', 'B-LOC', 'I-LOC', 'O', 'I-LOC', 'O', 'O', 'I-LOC']

    expected_entities = [('Mike', 'PER'), ('London', 'LOC'), ('Jack', 'PER'), ('John Doe', 'PER'),
                         ('Jack', 'PER'), ('Paris', 'LOC'), ('New York', 'LOC'), ('Moscow', 'LOC'), ('London', 'LOC')]
    expected_entity_index_by_word_index = [0, None, 1, None, 2, None, 3, 3,
                                           4, None, 5, 6, 6, None, 7, None, None, 8]

    document_words = document_text_to_words(document_text)
    for word, label in zip(document_words, document_labels):
        word.prev_level_tag = label

    assert (_extract_document_entities(document_words) ==
            (expected_entities, expected_entity_index_by_word_index))


def test_annotate_word_no_entity():
    entity_list = \
        [Entity('Mike', 'PER'), Entity('mike', 'LOC'), Entity('No Match', 'LOC'), Entity('mike L', 'LOC'),
         Entity('the Mike', 'ORG'), Entity('No Match', 'LOC'), Entity('a Mike Chang Sr.', 'ORG')]
    left_entities_indexes = set([0, 1, 2, 3])
    right_entities_indexes = set([4, 5, 6])

    word = Mock(text='Mike')
    feature_list = _get_word_features(word, None, entity_list, left_entities_indexes, right_entities_indexes)
    assert feature_list == ['L_UnLabeledToken_match_PER', 'L_UnLabeledToken_match_ic_LOC',
                            'L_UnLabeledToken_starts_ic_LOC', 'R_UnLabeledToken_ends_ORG',
                            'R_UnLabeledToken_substring_ORG']


def test_annotate_word_with_entity():
    entity_list = \
        [Entity('Mike Chang', 'PER'), Entity('Mike chang', 'LOC'), Entity('NoMatch', 'LOC'), Entity('Mike L', 'LOC'),
         Entity('Mike Chang', 'PER'),
         Entity('Mike Chang Sr.', 'ORG'), Entity('a Mike Chang Sr.', 'ORG'), Entity('a Mike Chang', 'LOC')]
    left_entities_indexes = set([0, 1, 2, 3])
    right_entities_indexes = set([5, 6, 7])

    word = Mock(text="Mike")
    feature_list = _get_word_features(word, 4, entity_list, left_entities_indexes, right_entities_indexes)
    assert feature_list == ['L_NE_match_PER', 'L_NE_match_ic_LOC', 'L_LabeledToken_starts_LOC',
                            'R_NE_starts_ORG', 'R_NE_substring_ORG', 'R_NE_ends_LOC']


def test_annotate_prev_level_entities(document_text_to_words):
    document_text = "Mike Chang Mike chang NoMatch Mike L\n" \
                    "Mike Chang\n" \
                    "Mike Chang Sr. a Mike Chang Sr. a Mike Chang"
    document_words = document_text_to_words(document_text)

    document_labels = ['I-PER', 'I-PER', 'I-LOC', 'I-LOC', 'B-LOC', 'B-LOC', 'I-LOC',
                       'I-PER', 'I-PER',
                       'I-ORG', 'I-ORG', 'I-ORG', 'B-ORG', 'I-ORG', 'I-ORG', 'I-ORG', 'I-LOC', 'I-LOC', 'I-LOC']
    for word, label in zip(document_words, document_labels):
        word.prev_level_tag = label

    annotate_prev_level_entities(document_words)

    expected_annotations_format = ['L_NE_match_PER_%d', 'L_NE_match_ic_LOC_%d', 'L_LabeledToken_starts_LOC_%d',
                                   'R_NE_starts_ORG_%d', 'R_NE_substring_ORG_%d', 'R_NE_ends_LOC_%d']
    expected_annotations = [annotation % QUANTIZATION for annotation in expected_annotations_format]
    assert set(getattr(document_words[7], ANNOTATION_ATTRIBUTE)) == set(expected_annotations)
