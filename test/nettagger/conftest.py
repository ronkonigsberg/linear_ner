import pytest

from nertagger.word import parsed_documents_to_words


@pytest.fixture
def document_text_to_words():
    def _document_text_to_words(document_text):
        parsed_document_mock = list()
        for sentence_text in document_text.splitlines():
            parsed_sentence_mock = map(lambda word_text: {'text': word_text}, sentence_text.split())
            parsed_document_mock.append(parsed_sentence_mock)
        return parsed_documents_to_words([parsed_document_mock])

    return _document_text_to_words
