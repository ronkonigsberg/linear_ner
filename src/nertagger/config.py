import os


PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
RESOURCES_DIR = os.path.join(PROJECT_DIR, 'resources')
DATA_DIR = os.path.join(PROJECT_DIR, 'data')
MODELS_DIR = os.path.join(PROJECT_DIR, 'models')


BROWN_CLUSTERS_DIR_PATH = os.path.join(RESOURCES_DIR, 'brown-clusters')
GAZETTEERS_DIR_PATH = os.path.join(RESOURCES_DIR, 'gazetteers')

L1_TRAIN_FILE_PATH = os.path.join(DATA_DIR, 'eng.train')
L1_CLASS_LEXICON_FILE_PATH = os.path.join(MODELS_DIR, 'class_lexicon.l1')
L1_MODEL_FILE_PATH = os.path.join(MODELS_DIR, 'model.l1')

L1_TAG_TRAIN_MODEL_FILE_PATH = os.path.join(MODELS_DIR, 'model.l1.kfold')
L1_TAG_TRAIN_K_FOLD_PARAM = 1

L2_TRAIN_FILE_PATH = os.path.join(DATA_DIR, 'my_eng.train.l2')
L2_CLASS_LEXICON_FILE_PATH = os.path.join(MODELS_DIR, 'class_lexicon.l2')
L2_MODEL_FILE_PATH = os.path.join(MODELS_DIR, 'model.l2')

TEST_FILE_PATH = os.path.join(DATA_DIR, 'eng.testa')
L1_TAGGED_TEST_FILE_PATH = os.path.join(DATA_DIR, 'my_eng.testa.l1')
L2_TAGGED_TEST_FILE_PATH = os.path.join(DATA_DIR, 'my_eng.testa.l2')

NUM_TRAIN_ITERATIONS = 12


BROWN_PREFIX_TO_LEN_FILE_PATH = os.path.join(RESOURCES_DIR, 'brown_prefix_to_len.json')
