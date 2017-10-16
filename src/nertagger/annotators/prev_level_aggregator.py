from collections import Counter, namedtuple


Entity = namedtuple('Entity', ['text', 'type'])


ANNOTATION_ATTRIBUTE = 'prev_level_aggregation'
QUANTIZATION = 3


def annotate_prev_level_entities(word_list, window_size=1000):
    current_index = 0
    while current_index < len(word_list):
        current_document_words = word_list[current_index].document
        _annotate_document(current_document_words, window_size)
        current_index += len(current_document_words)


def _annotate_document(document_words, window_size):
    entity_list, entity_index_by_word_index = _extract_document_entities(document_words)
    for word in document_words:
        word_entity_index = entity_index_by_word_index[word.document_index]

        left_window_start = max(0, word.document_index - window_size)
        left_entities_indexes = entity_index_by_word_index[left_window_start: word.document_index]
        left_entities_indexes = set(left_entities_indexes) - set([None, word_entity_index])

        right_window_end = min(len(document_words), word.document_index + 1 + window_size)
        right_entities_indexes = entity_index_by_word_index[word.document_index + 1: right_window_end]
        right_entities_indexes = set(right_entities_indexes) - set([None, word_entity_index])

        word_feature_list = _get_word_features(word, word_entity_index, entity_list, left_entities_indexes,
                                               right_entities_indexes)

        word_feature_counts = Counter(word_feature_list)
        max_count = max(word_feature_counts.values()) if len(word_feature_counts) > 0 else 0
        normalized_feature_list = map(lambda (feature, count): '%s_%d' % (feature, int((QUANTIZATION*count)/max_count)),
                                      word_feature_counts.iteritems())

        setattr(word, ANNOTATION_ATTRIBUTE, normalized_feature_list)


def _get_word_features(word, word_entity_index, entity_list, left_entities_indexes, right_entities_indexes):
    word_entity = None if word_entity_index is None else entity_list[word_entity_index]

    feature_list = list()
    for direction, entities_indexes in [('L', left_entities_indexes), ('R', right_entities_indexes)]:
        for entity_index in entities_indexes:
            current_entity = entity_list[entity_index]
            word_entity_relation = \
                _get_word_to_entity_relation(word, word_entity, current_entity)
            if word_entity_relation:
                feature_list.append('%s_%s' % (direction, word_entity_relation))
    return feature_list


def _get_word_to_entity_relation(word, word_entity, other_entity):
    relation = None

    if word_entity and len(word_entity.text) > 3:
        relation_type = _get_string_relation(other_entity.text, word_entity.text)
        if relation_type:
            token_type = 'NE'
            relation = '%s_%s_%s' % (token_type, relation_type, other_entity.type)

    if relation is None and len(word.text) > 3:
        relation_type = _get_string_relation(other_entity.text, word.text)
        if relation_type:
            token_type = 'UnLabeledToken' if word_entity is None else 'LabeledToken'
            relation = '%s_%s_%s' % (token_type, relation_type, other_entity.type)

    return relation


def _get_string_relation(base_string, partial_string):
    if base_string == partial_string:
        return 'match'
    if base_string.startswith(partial_string):
        return 'starts'
    if base_string.endswith(partial_string):
        return 'ends'
    if base_string.find(partial_string) != -1:
        return 'substring'

    base_string_low = base_string.lower()
    partial_string_low = partial_string.lower()
    if base_string_low == partial_string_low:
        return 'match_ic'
    if base_string_low.startswith(partial_string_low):
        return 'starts_ic'
    if base_string_low.endswith(partial_string_low):
        return 'ends_ic'
    if base_string_low.find(partial_string_low) != -1:
        return 'substring_ic'

    return None


def _extract_document_entities(document_words):
    entity_list = list()
    entity_index_by_word_index = list()

    current_index = 0
    while current_index < len(document_words):
        current_sentence_words = document_words[current_index].sentence

        entity_text = None
        for word in current_sentence_words:
            if entity_text and word.prev_level_tag == expected_tag:
                entity_index_by_word_index.append(len(entity_list))
                entity_text += ' ' + word.text
            else:
                if entity_text:
                    entity_list.append(Entity(text=entity_text, type=entity_type))
                entity_text = None

                if word.prev_level_tag != 'O':
                    entity_index_by_word_index.append(len(entity_list))

                    entity_text = word.text
                    entity_type = word.prev_level_tag.split('-')[1]
                    expected_tag = 'I-' + entity_type
                else:
                    entity_index_by_word_index.append(None)
        if entity_text:
            entity_list.append(Entity(entity_text, entity_type))

        current_index += len(current_sentence_words)

    return entity_list, entity_index_by_word_index
