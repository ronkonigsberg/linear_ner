from nertagger.annotators.context_instances import ContextInstancesAnnotator
from nertagger.annotators.brown_clusters import BrownAnnotator
from nertagger.annotators.gazetteers import GazetteersAnnotator
from nertagger.annotators.prev_level_aggregator import ANNOTATION_ATTRIBUTE as PREV_LEVEL_ANNOTATION_ATTRIBUTE

from nertagger.features.utils import feature_func


@feature_func
def brown_paths(word):
    word_brown_paths = getattr(word, BrownAnnotator.ANNOTATION_ATTRIBUTE, None)
    if word_brown_paths is None:
        raise RuntimeError("This feature requires using Brown annotator")
    return word_brown_paths


@feature_func
def gazetteers(word):
    word_gazetteers = getattr(word, GazetteersAnnotator.ANNOTATION_ATTRIBUTE, None)
    if word_gazetteers is None:
        raise RuntimeError("This feature requires using gazetteers annotator")
    return word_gazetteers


@feature_func
def context_case(word):
    context_instances = getattr(word, ContextInstancesAnnotator.ANNOTATION_ATTRIBUTE, None)
    if context_instances is None:
        raise RuntimeError("This feature requires using context annotator")

    context_case_list = list()
    for instance in context_instances:
        if instance.text.islower():
            instance_case = 'lower'
        else:
            if instance.sentence_index == 0:
                # TODO: maybe handle also after '.'?
                instance_case = 'upper_start_sentence'
            else:
                instance_case = 'upper_middle_sentence'
        context_case_list.append(instance_case)
    return context_case_list


@feature_func
def context_brown(word):
    context_instances = getattr(word, ContextInstancesAnnotator.ANNOTATION_ATTRIBUTE, None)
    if context_instances is None:
        raise RuntimeError("This feature requires using context annotator")

    context_brown_list = list()
    for instance in context_instances:
        for offset in xrange(-2, 3):
            instance_offset_index = instance.document_index + offset
            if 0 <= instance_offset_index < len(word.document):
                instance_offset_word = word.document[instance_offset_index]

                brown_prefixes = getattr(instance_offset_word, BrownAnnotator.ANNOTATION_ATTRIBUTE, None)
                if brown_prefixes is None:
                    raise RuntimeError("This feature requires using Brown annotator")

                if len(brown_prefixes) > 0:
                    context_brown_list.append("%d_%s" % (offset, brown_prefixes[0]))
    return context_brown_list


@feature_func
def context_text(word):
    context_instances = getattr(word, ContextInstancesAnnotator.ANNOTATION_ATTRIBUTE, None)
    if context_instances is None:
        raise RuntimeError("This feature requires using context annotator")

    context_text_list = list()
    for instance in context_instances:
        for offset in (-1, 0, 1):
            instance_offset_index = instance.document_index + offset
            if 0 <= instance_offset_index < len(word.document):
                instance_offset_word = word.document[instance_offset_index]
                context_text_list.append("%d_%s" % (offset, instance_offset_word.text))
    return context_text_list


@feature_func
def prev_level_aggregation(word):
    word_prev_level_aggregation = getattr(word, PREV_LEVEL_ANNOTATION_ATTRIBUTE, None)
    if word_prev_level_aggregation is None:
        raise RuntimeError("This feature requires using prev level aggregation annotator")
    return word_prev_level_aggregation
