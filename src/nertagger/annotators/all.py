import logbook

from nertagger.config import BROWN_CLUSTERS_DIR_PATH, GAZETTEERS_DIR_PATH

from nertagger.annotators.brown_clusters import create_brwon_annotator
from nertagger.annotators.gazetteers import create_gazetteers_annotator
from nertagger.annotators.context_instances import ContextInstancesAnnotator


logger = logbook.Logger('Annotators')


def annotate_data(word_list):
    logger.info('Loading brown clusters.')
    brown_annotator = create_brwon_annotator(BROWN_CLUSTERS_DIR_PATH)
    logger.info('Annotating data with brown clusters.')
    brown_annotator.annotate_data(word_list)

    logger.info('Loading gazetteers.')
    gazetteer_annotator = create_gazetteers_annotator(GAZETTEERS_DIR_PATH)
    logger.info('Annotating data with gazetteers.')
    gazetteer_annotator.annotate_data(word_list)

    context_annotator = ContextInstancesAnnotator()
    logger.info('Annotating data with context instances.')
    context_annotator.annotate_data(word_list)
