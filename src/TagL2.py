import argparse
import logbook

from nertagger.parser import parse_conll_tagged, format_conll_tagged
from nertagger.word import parsed_documents_to_words, words_to_parsed_documents
from nertagger.annotators.all import annotate_data, annotate_prev_level_entities
from nertagger.features.all import L2_FEATURES
from nertagger.model import load_model, greedy_decoding
from nertagger.tag_scheme import BILOU

from nertagger.config import (L1_TAGGED_TEST_FILE_PATH, L2_MODEL_FILE_PATH, L2_CLASS_LEXICON_FILE_PATH,
                              L2_TAGGED_TEST_FILE_PATH)


logger = logbook.Logger('Tag_L2')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--test_file', default=L1_TAGGED_TEST_FILE_PATH, help='path to test file with l1 tags')
    parser.add_argument('-m', '--model_file', default=L2_MODEL_FILE_PATH, help='path to model parameters')
    parser.add_argument('-l', '--lexicon_file', default=L2_CLASS_LEXICON_FILE_PATH, help='path to label lexicon')
    parser.add_argument('-o', '--output_file', default=L2_TAGGED_TEST_FILE_PATH, help='path to output file')
    args = parser.parse_args()

    logger.info('Loading trained model.')
    trained_model, class_lexicon = load_model(args.model_file, args.lexicon_file)

    logger.info('Reading test file')
    with open(args.test_file, 'rb') as f:
        test_data = f.read()

    logger.info('Parsing test data.')
    parsed_documents_list = parse_conll_tagged(test_data)
    logger.info('Parse completed (%d documents).' % len(parsed_documents_list))

    logger.info('Building word list from test data.')
    test_words = parsed_documents_to_words(parsed_documents_list)

    logger.info('Annotate test words.')
    annotate_data(test_words)

    logger.info('Set tag as prev_level_tag for prev level aggregation features.')
    for word in test_words:
        word.prev_level_tag = word.tag

    logger.info('Annotate words with prev level entities.')
    annotate_prev_level_entities(test_words)

    logger.info('Start greedy decoding.')
    greedy_decoding(test_words, trained_model, class_lexicon, L2_FEATURES)

    logger.info('Convert tag scheme from BILOU to IOB.')
    BILOU.decode(test_words, tag_attr='tag')

    logger.info('Formatting output.')
    parsed_documents_list = words_to_parsed_documents(test_words)
    output_data = format_conll_tagged(parsed_documents_list)

    logger.info('Dumping output.')
    with open(args.output_file, 'wb') as f:
        f.write(output_data)


if __name__ == '__main__':
    main()
