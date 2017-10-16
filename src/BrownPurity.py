import json
import argparse
import logbook

from collections import Counter, defaultdict

from nertagger.config import L1_TRAIN_FILE_PATH, BROWN_CLUSTERS_DIR_PATH, BROWN_PREFIX_TO_LEN_FILE_PATH
from nertagger.parser import parse_conll_train
from nertagger.word import parsed_documents_to_words

from nertagger.annotators.brown_clusters import parse_brown_clusters_directory


logger = logbook.Logger('BrownPurity')


def build_path_histogram(brown_cluster, training_words, offset=0):
    path_to_type_list = defaultdict(lambda: list())

    word_index = 0
    while word_index < len(training_words):
        current_sentence = training_words[word_index].sentence
        if offset >= 0:
            sentence_cluster_words = current_sentence[offset:]
            sentence_type_words = current_sentence
        else:
            sentence_cluster_words = current_sentence
            sentence_type_words = current_sentence[-offset:]

        for cluster_word, type_word in zip(sentence_cluster_words, sentence_type_words):
            if cluster_word.text in brown_cluster:
                brown_path = brown_cluster[cluster_word.text][0]
                ner_type = 'O' if type_word.gold_label == 'O' else type_word.gold_label.split('-')[1]
                path_to_type_list[brown_path].append(ner_type)

        word_index += len(current_sentence)

    path_to_type_histogram = dict()
    for path, type_list in path_to_type_list.iteritems():
        path_to_type_histogram[path] = Counter(type_list)
    return path_to_type_histogram


def build_prefix_histogram(path_to_type_histogram):
    prefix_to_type_histogram = defaultdict(lambda: Counter())
    for path, path_type_histogram in path_to_type_histogram.iteritems():
        for prefix_len in xrange(1, len(path)+1):
            prefix = path[:prefix_len]
            prefix_to_type_histogram[prefix].update(path_type_histogram)
    return prefix_to_type_histogram


def get_path_to_prefix_len(path_to_type_histogram, prefix_to_type_histogram):
    path_to_prefix_len = dict()
    for path, path_type_histogram in path_to_type_histogram.iteritems():
        path_to_prefix_len[path] = len(path)

        path_common_type = path_type_histogram.most_common(1)[0][0]
        for prefix_len in xrange(len(path)-1, 0, -1):
            prefix = path[:prefix_len]
            prefix_histogram = prefix_to_type_histogram[prefix]
            prefix_common_type = prefix_histogram.most_common(1)[0][0]

            if prefix_common_type == path_common_type:
                prefix_purity = prefix_histogram.most_common(1)[0][1] / float(sum(prefix_histogram.values()))
                if prefix_purity > 0.9:
                    path_to_prefix_len[path] = prefix_len
    return path_to_prefix_len


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--train_file', default=L1_TRAIN_FILE_PATH, help='path to training file')
    parser.add_argument('-b', '--brown_dir', default=BROWN_CLUSTERS_DIR_PATH, help='path to brown cluster directory')
    args = parser.parse_args()

    logger.info('Reading train data.')
    with open(args.train_file, 'rb') as f:
        train_data = f.read()

    logger.info('Parsing train data.')
    parsed_document_list = parse_conll_train(train_data)
    logger.info('Parse completed (%d documents).' % len(parsed_document_list))

    logger.info('Building word list from train data.')
    training_words = parsed_documents_to_words(parsed_document_list)

    logger.info('Parsing Brown clusters directory.')
    all_clusters_dict = parse_brown_clusters_directory(args.brown_dir)

    logger.info('Calculating prefix len for each path.')
    cluster_to_path_histogram_by_offset = dict()
    cluster_to_prefix_histogram_by_offset = dict()
    cluster_to_prefix_to_len_by_offset = dict()
    for corpus_name, cluster_dict in all_clusters_dict.iteritems():
        path_histogram_by_offset = dict()
        prefix_histogram_by_offset = dict()
        path_to_len_by_offset = dict()

        for offset in (-2, -1, 0, 1, 2):
            path_to_type_histogram = build_path_histogram(cluster_dict, training_words, offset)
            path_histogram_by_offset[offset] = path_to_type_histogram

            prefix_to_type_histogram = build_prefix_histogram(path_to_type_histogram)
            prefix_histogram_by_offset[offset] = prefix_to_type_histogram

            path_to_len = get_path_to_prefix_len(path_to_type_histogram, prefix_to_type_histogram)
            path_to_len_by_offset[offset] = path_to_len

        cluster_to_path_histogram_by_offset[corpus_name] = path_histogram_by_offset
        cluster_to_prefix_histogram_by_offset[corpus_name] = prefix_histogram_by_offset
        cluster_to_prefix_to_len_by_offset[corpus_name] = path_to_len_by_offset

    logger.info('Dumping result to file.')
    with open(BROWN_PREFIX_TO_LEN_FILE_PATH, 'wb') as f:
        json.dump(cluster_to_prefix_to_len_by_offset, f, indent=4)


if __name__ == '__main__':
    main()
