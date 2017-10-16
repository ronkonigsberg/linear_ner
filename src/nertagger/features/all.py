from functools import partial

from nertagger.features.utils import window_feature, joint_feature

from nertagger.features import simple_features
from nertagger.features import text_features
from nertagger.features import annotation_features
from nertagger.features import tag_features


_JOINT_FEATURES = (
    simple_features.sentence_start,

    text_features.prefixes,
    text_features.suffixes,
    partial(window_feature, feature_func=text_features.text),
    partial(window_feature, feature_func=text_features.capitalized),
    partial(window_feature, feature_func=text_features.normalized_digits),
    partial(window_feature, feature_func=text_features.all_letters_capitalized),
    partial(window_feature, feature_func=text_features.all_non_letters),
    partial(window_feature, feature_func=text_features.all_digits),

    partial(window_feature, feature_func=annotation_features.gazetteers),
    partial(window_feature, feature_func=annotation_features.brown_paths),

    annotation_features.context_text,
    # annotation_features.context_case,
    # annotation_features.context_brown,
    # tag_features.context_prev_tag,

    tag_features.prev_tag,
    tag_features.prev_prev_tag,
    tag_features.prev_tag_pattern,

    partial(joint_feature,
            left_feature_func=tag_features.prev_tag,
            right_feature_func=partial(window_feature, feature_func=text_features.text)),
)

_L1_ONLY_FEATURES = ()

_L2_ONLY_FEATURES = (
    annotation_features.prev_level_aggregation,
)


L1_FEATURES = _JOINT_FEATURES + _L1_ONLY_FEATURES

L2_FEATURES = _JOINT_FEATURES + _L2_ONLY_FEATURES
