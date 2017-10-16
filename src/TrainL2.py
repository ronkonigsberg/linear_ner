import argparse
import logbook

from nertagger.parser import parse_conll_tagged
from nertagger.word import parsed_documents_to_words
from nertagger.annotators.all import annotate_data, annotate_prev_level_entities
from nertagger.tag_scheme import BILOU
from nertagger.model import train, save_model
from nertagger.features.all import L2_FEATURES
from nertagger.config import L2_TRAIN_FILE_PATH, L2_MODEL_FILE_PATH, L2_CLASS_LEXICON_FILE_PATH, NUM_TRAIN_ITERATIONS


logger = logbook.Logger('Train_L2')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--train_file', default=L2_TRAIN_FILE_PATH, help='path to training file with l1 tags')
    parser.add_argument('-m', '--model_file', default=L2_MODEL_FILE_PATH, help='path to save trained model parameters')
    parser.add_argument('-l', '--lexicon_file', default=L2_CLASS_LEXICON_FILE_PATH, help='path to save label lexicon')
    args = parser.parse_args()

    logger.info('Reading train data.')
    with open(args.train_file, 'rb') as f:
        train_data = f.read()

    logger.info('Parsing train data.')
    parsed_document_list = parse_conll_tagged(train_data)
    logger.info('Parse completed (%d documents).' % len(parsed_document_list))

    logger.info('Building word list from train data.')
    training_words = parsed_documents_to_words(parsed_document_list)

    logger.info('Annotate training data.')
    annotate_data(training_words)

    logger.info('Set tag as prev_level_tag for prev level aggregation features.')
    for word in training_words:
        word.prev_level_tag = word.tag

    logger.info('Annotate words with prev level entities.')
    annotate_prev_level_entities(training_words)

    logger.info('Convert gold label tag scheme from IOB to BILOU.')
    BILOU.encode(training_words, tag_attr='gold_label')

    logger.info('Set gold label as tag (for model tag features).')
    for word in training_words:
        word.tag = word.gold_label

    logger.info('Train model.')
    trained_model_params, class_lexicon = train(training_words, L2_FEATURES, NUM_TRAIN_ITERATIONS)
    save_model(trained_model_params, args.model_file, class_lexicon, args.lexicon_file)


if __name__ == '__main__':
    main()
