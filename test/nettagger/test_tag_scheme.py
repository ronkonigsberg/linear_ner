import pytest
import mock

from nertagger.tag_scheme import BIO, BILOU


@pytest.mark.parametrize("input_tag_list, expected_tag_list", [
    (['I-PER'], ['B-PER']),
    (['I-PER', 'I-LOC'], ['B-PER', 'B-LOC']),
    (['I-PER', 'O', 'I-LOC'], ['B-PER', 'O', 'B-LOC']),

    (['I-PER', 'I-PER'], ['B-PER', 'I-PER']),
    (['I-PER', 'B-PER'], ['B-PER', 'B-PER']),
])
def test_bio(input_tag_list, expected_tag_list):
    sentence = list()
    for tag in input_tag_list:
        word_mock = mock.Mock(random_tag_attr=tag, sentence=sentence)
        sentence.append(word_mock)

    BIO.encode(sentence, tag_attr='random_tag_attr')
    for word, expected_tag in zip(sentence, expected_tag_list):
        assert word.random_tag_attr == expected_tag

    BIO.decode(sentence, tag_attr='random_tag_attr')
    for word, initial_atg in zip(sentence, input_tag_list):
        assert word.random_tag_attr == initial_atg


@pytest.mark.parametrize("input_tag_list, expected_tag_list", [
    (['I-PER'], ['U-PER']),
    (['I-PER', 'O', 'I-LOC'], ['U-PER', 'O', 'U-LOC']),
    (['I-PER', 'I-LOC'], ['U-PER', 'U-LOC']),
    (['I-PER', 'B-PER'], ['U-PER', 'U-PER']),


    (['I-PER', 'I-PER'], ['B-PER', 'L-PER']),
    (['I-PER', 'B-PER', 'I-PER'], ['U-PER', 'B-PER', 'L-PER']),
    (['I-PER', 'I-PER', 'I-PER'], ['B-PER', 'I-PER', 'L-PER']),
    (['I-PER', 'I-PER', 'I-PER', 'B-PER', 'I-PER'], ['B-PER', 'I-PER', 'L-PER', 'B-PER', 'L-PER']),
])
def test_bilou(input_tag_list, expected_tag_list):
    sentence = list()
    for tag in input_tag_list:
        word_mock = mock.Mock(random_tag_attr=tag, sentence=sentence)
        sentence.append(word_mock)

    BILOU.encode(sentence, tag_attr='random_tag_attr')
    for word, expected_tag in zip(sentence, expected_tag_list):
        assert word.random_tag_attr == expected_tag

    BILOU.decode(sentence, tag_attr='random_tag_attr')
    for word, initial_atg in zip(sentence, input_tag_list):
        assert word.random_tag_attr == initial_atg
