from collections import defaultdict


class ContextInstancesAnnotator(object):
    ANNOTATION_ATTRIBUTE = 'context_instances'

    def __init__(self, context_limit=200):
        self.context_limit = context_limit

    def annotate_data(self, word_list):
        current_index = 0
        while current_index < len(word_list):
            current_document_words = word_list[current_index].document
            self.annotate_document(current_document_words)
            current_index += len(current_document_words)

    def annotate_document(self, document_words):
        word_to_instances = defaultdict(lambda: list())
        for word in document_words:
            word_to_instances[word.text.lower()].append(word)

        for word in document_words:
            word_context_instances = \
                filter(lambda instance: 0 < abs(instance.document_index - word.document_index) <= self.context_limit,
                       word_to_instances[word.text.lower()])

            setattr(word, self.ANNOTATION_ATTRIBUTE, word_context_instances)
