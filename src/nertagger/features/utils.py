from itertools import product
from functools import wraps


def feature_func(func):
    @wraps(func)
    def ret_value_to_feature_list(*args, **kwargs):
        func_name = func.__name__
        ret_value = func(*args, **kwargs)
        if ret_value is None:
            return []

        elif type(ret_value) is bool:
            if ret_value:
                return [func_name]
            else:
                return []

        elif type(ret_value) is str:
            return ["%s_%s" % (func_name, ret_value)]

        elif type(ret_value) is list:
            feature_list = list()
            for feature_value in ret_value:
                if type(feature_value) is not str:
                    raise RuntimeError("Unsupported type 'list(%s)'" % type(feature_value))
                feature_list.append("%s_%s" % (func_name, feature_value))
            return feature_list

        else:
            raise RuntimeError("Unsupported type '%s'" % type(ret_value))

    return ret_value_to_feature_list


def window_feature(word, feature_func, window=(-2, -1, 0, 1, 2)):
    window_feature_list = list()
    for offset in window:
        offset_index = word.sentence_index + offset
        if 0 <= offset_index < len(word.sentence):
            offset_feature_list = feature_func(word.sentence[offset_index])
            if offset != 0:
                offset_feature_list = map(lambda feature: "%d_%s" % (offset, feature), offset_feature_list)
            window_feature_list.extend(offset_feature_list)
    return window_feature_list


def joint_feature(word, left_feature_func, right_feature_func):
    left_feature_list = left_feature_func(word)
    right_feature_list = right_feature_func(word)
    joint_feature_list = list()
    for (left_feature, right_feature) in product(left_feature_list, right_feature_list):
        joint_feature_list.append("%s_%s" % (left_feature, right_feature))
    return joint_feature_list
