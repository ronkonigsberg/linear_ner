from nertagger.annotators.context_instances import ContextInstancesAnnotator


def test_context_annotate_big_limit(document_text_to_words):
    document_text = '\n'.join(['Ron visited the beach .',
                               'The lifeguard called Ron from the shore .',
                               'Ron came as soon as possible .'])
    document_words = document_text_to_words(document_text)

    first_ron = document_words[0]
    second_ron = document_words[8]
    third_ron = document_words[13]

    context_annotator = ContextInstancesAnnotator(context_limit=200)
    context_annotator.annotate_data(document_words)

    assert getattr(first_ron, ContextInstancesAnnotator.ANNOTATION_ATTRIBUTE) == [second_ron, third_ron]
    assert getattr(second_ron, ContextInstancesAnnotator.ANNOTATION_ATTRIBUTE) == [first_ron, third_ron]
    assert getattr(third_ron, ContextInstancesAnnotator.ANNOTATION_ATTRIBUTE) == [first_ron, second_ron]


def test_context_annotate_small_limit(document_text_to_words):
    document_text = '\n'.join(['Ron visited the beach .',
                               'The lifeguard called Ron from the shore .',
                               'Ron came as soon as possible .'])
    document_words = document_text_to_words(document_text)

    first_ron = document_words[0]
    second_ron = document_words[8]
    third_ron = document_words[13]

    context_annotator = ContextInstancesAnnotator(context_limit=8)
    context_annotator.annotate_data(document_words)

    assert getattr(second_ron, ContextInstancesAnnotator.ANNOTATION_ATTRIBUTE) == [first_ron, third_ron]
    assert getattr(first_ron, ContextInstancesAnnotator.ANNOTATION_ATTRIBUTE) == [second_ron]
    assert getattr(third_ron, ContextInstancesAnnotator.ANNOTATION_ATTRIBUTE) == [second_ron]
