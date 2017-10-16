import argparse

from collections import defaultdict, Counter


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('train_file', help="training file path")
    parser.add_argument('test_file', help="test file path")
    parser.add_argument('output_file', help="output file path")
    args = parser.parse_args()

    with open(args.train_file, 'rb') as f:
        train_data = f.read()
    train_lines = train_data.split('\n')
    phrase_to_type = train_tagger(train_lines)

    with open(args.test_file, 'rb') as f:
        test_data = f.read()
    test_lines = test_data.split('\n')
    test_tag_list = tag_file(phrase_to_type, test_lines)

    output_lines = list()
    for test_line, line_tag in zip(test_lines, test_tag_list):
        if line_tag:
            output_lines.append("%s %s" % (test_line, line_tag))
        else:
            output_lines.append("")
    output_data = '\n'.join(output_lines)
    with open(args.output_file, 'wb') as f:
        f.write(output_data)


def train_tagger(train_lines):
    """
    trains ner tagger model based on the given train data
    :param train_lines: the CoNLL2003 training file lines
    :return: phrase to type dict and
    """
    phrase_to_type_count = defaultdict(lambda: Counter())

    phrase_type = None
    phrase_words = []
    for line in train_lines:
        word, tag = _get_train_word_and_tag(line)

        # if expression end
        if tag == 'O' or tag.startswith('B-'):
            if phrase_words:
                phrase = ' '.join(phrase_words)
                phrase_to_type_count[phrase].update([phrase_type])

            phrase_type = None
            phrase_words = []

        if tag != 'O':
            phrase_type = tag.split('-', 1)[1]
            phrase_words.append(word)

    phrase_to_type = dict()
    for phrase, phrase_type_count in phrase_to_type_count.iteritems():
        phrase_to_type[phrase] = phrase_type_count.most_common(1)[0][0]
    return phrase_to_type


def tag_file(phrase_to_type, test_lines):
    """
    tags the given test data using the model learnt from the training data
    :param phrase_to_type: tagger model, dict mapping between seen training phrases to their most common type
    :param test_lines: the lines of the given test file
    :return: a list containing a tag for each line
    """
    prefix_set = _build_prefix_set(phrase_to_type.keys())
    test_words = map(lambda line: _get_test_word(line), test_lines)

    test_tag_list = list()

    i = 0
    while i < len(test_words):
        phrase = ""
        phrase_len = 0
        while phrase in prefix_set:
            if (i + phrase_len) < len(test_words) and test_words[i + phrase_len] is not None:
                phrase_len += 1
                phrase = ' '.join(test_words[i:i+phrase_len])
            else:
                break

        phrase = ' '.join(test_words[i:i+phrase_len])
        while phrase and phrase not in phrase_to_type:
            phrase_len -= 1
            phrase = ' '.join(test_words[i:i+phrase_len])

        if phrase:
            phrase_type = phrase_to_type[phrase]
            phrase_tag_list = ['B-' + phrase_type] + ['I-' + phrase_type] * (phrase_len-1)
            test_tag_list.extend(phrase_tag_list)
            i += phrase_len
        else:
            if test_words[i]:
                test_tag_list.append('O')
            else:
                test_tag_list.append(None)
            i += 1

    return test_tag_list


def _get_train_word_and_tag(train_line):
    line_parts = train_line.split()
    if line_parts:
        word = line_parts[0]
        tag = line_parts[-1]
    else:
        word = '-X-'
        tag = 'O'
    return word, tag


def _get_test_word(test_line):
    line_parts = test_line.split()
    return line_parts[0] if line_parts else None


def _build_prefix_set(phrase_list):
    prefix_set = set()
    for phrase in phrase_list:
        phrase_words = phrase.split(' ')
        for i in xrange(len(phrase_words)):
            current_phrase_prefix = ' '.join(phrase_words[:i])
            prefix_set.add(current_phrase_prefix)
    return prefix_set


if __name__ == '__main__':
    main()
