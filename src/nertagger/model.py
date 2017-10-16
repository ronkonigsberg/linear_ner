import random

import logbook
import json

from ml import ml


logger = logbook.Logger('model')

# init random seed to get consistent results
random.seed(1)


def train(training_words, feature_list, num_iterations):
    logger.info('Extract training examples.')
    training_examples = extract_training_examples(training_words, feature_list)

    logger.info("Building class lexicon.")
    class_labels = set(map(lambda example: example[0], training_examples))
    label_to_class_mapping = dict()
    class_to_label_lexicon = dict()
    for class_, class_label in enumerate(class_labels):
        label_to_class_mapping[class_label] = class_
        class_to_label_lexicon[class_] = class_label
    logger.debug("Found %d class types." % len(label_to_class_mapping))

    logger.info("Starting model training.")
    trained_model_params = ml.MultitronParameters(len(label_to_class_mapping))
    for iteration in xrange(num_iterations):
        random.shuffle(training_examples)

        current_progress = 0
        for idx, current_example in enumerate(training_examples):
            trained_model_params.tick()

            class_label, features = current_example
            class_ = label_to_class_mapping[class_label]

            scores = trained_model_params.get_scores(features)
            predicted_class_key = max([(s, i) for i, s in scores.iteritems()])[1]
            if predicted_class_key != class_:
                trained_model_params.add(features, class_, 1)
                trained_model_params.add(features, predicted_class_key, -1)

            if ((idx+1)*100)/len(training_examples) > current_progress:
                current_progress += 1
                # logger.debug("completed %d percent..." % current_progress)

        logger.debug("Iteration %d done." % (iteration+1))

    return trained_model_params, class_to_label_lexicon


def save_model(model_params, model_params_file_path, class_lexicon, class_lexicon_file_path):
    logger.info("Dumping class lexicon.")
    with open(class_lexicon_file_path, 'wb') as f:
        json.dump(class_lexicon, f, indent=4)

    logger.info("Dumping model file")
    model_params.dump_fin(file(model_params_file_path, 'w'))


def load_model(model_params_file_path, class_lexicon_file_path):
    logger.debug('Loading model parameters.')
    trained_model = ml.MulticlassModel(model_params_file_path)

    logger.debug('Loading class lexicon.')
    with open(class_lexicon_file_path, 'rb') as f:
        class_lexicon = json.load(f)
    class_lexicon = dict(map(lambda (key, val): (int(key), str(val)), class_lexicon.iteritems()))

    return trained_model, class_lexicon


def greedy_decoding(word_list, model, class_lexicon, feature_list):
    logger.info('Starting greedy decoding.')
    for word in word_list:
        best_class, _ = model.predict(extract_features(word, feature_list))
        word.tag = class_lexicon[best_class]


def extract_training_examples(training_words, feature_list):
    training_examples = list()

    logger.debug("Extracting features for each training word (this can take up to a few minutes).")
    current_progress = 0
    for idx, word in enumerate(training_words):
        training_examples.append((word.gold_label, extract_features(word, feature_list)))

        if ((idx+1)*100)/len(training_words) > current_progress:
            current_progress += 1
            # logger.debug("completed %d percent..." % current_progress)
    return training_examples


def extract_features(word, feature_func_list):
    word_features = list()
    for feature_func in feature_func_list:
        word_features.extend(feature_func(word))
    return word_features
