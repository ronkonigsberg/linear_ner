import sys

from nertagger.parser import parse_conll_tagged
from nertagger.word import parsed_documents_to_words
from nertagger.config import L1_TAGGED_TEST_FILE_PATH

from nertagger.eval import extract_entities_by_types, get_stats


def main():
    tagged_file_path = L1_TAGGED_TEST_FILE_PATH if len(sys.argv) == 1 else sys.argv[1]

    # parse word list from tagged file
    raw_data = open(tagged_file_path, 'rb').read()
    word_list = parsed_documents_to_words(parse_conll_tagged(raw_data))

    # extract tagged and gold entities (per entity type)
    tagged_entities_by_type = extract_entities_by_types(word_list, tag_attr='tag')
    gold_entities_by_type = extract_entities_by_types(word_list, tag_attr='gold_label')

    # print stats per entity type
    for group in sorted(gold_entities_by_type.keys()):
        precision, recall, f1 = get_stats(tagged_entities_by_type[group], gold_entities_by_type[group])
        print "%15s" % group,
        print 'prec: %.2f' % precision,
        print 'recall: %.2f' % recall,
        print 'f1: %.2f' % f1,
        print len(tagged_entities_by_type[group])


if __name__ == '__main__':
    main()
