from collections import defaultdict, namedtuple


Entity = namedtuple('Entity', ['type', 'start_index', 'end_index'])


def extract_entities_by_types(word_list, tag_attr='tag'):
    entities_by_type = defaultdict(set)

    open_entity_type = None
    open_entity_start_index = None
    for word_index, word in enumerate(word_list):
        word_tag = getattr(word, tag_attr)
        word_entity_type = None if word_tag == 'O' else word_tag[2:]

        if open_entity_type and (open_entity_type != word_entity_type or not word_tag.startswith('I-')):
            # close current entity
            new_entity = Entity(open_entity_type, open_entity_start_index, word_index)
            entities_by_type[open_entity_type].add(new_entity)
            entities_by_type['ALL'].add(new_entity)

            open_entity_type = None
            open_entity_start_index = None

        if word_entity_type and open_entity_type is None:
            # open new entity
            open_entity_type = word_entity_type
            open_entity_start_index = word_index

    if open_entity_type:
        # the last word was a part of an entity, close it
        new_entity = Entity(open_entity_type, open_entity_start_index, len(word_list))
        entities_by_type[open_entity_type].add(new_entity)
        entities_by_type['ALL'].add(new_entity)

    return dict(entities_by_type)


def get_stats(tagged_entities, gold_entities):
    entity_intersection = tagged_entities.intersection(gold_entities)
    if not entity_intersection:
        return 0, 0, 0

    precision = (100.0 * len(entity_intersection)) / len(tagged_entities)
    recall = (100.0 * len(entity_intersection)) / len(gold_entities)
    f1 = (2 * precision * recall) / (precision + recall)
    return precision, recall, f1
