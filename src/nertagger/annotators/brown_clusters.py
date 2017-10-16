import os


class BrownAnnotator(object):
    ANNOTATION_ATTRIBUTE = 'brown_prefixes'

    def __init__(self, clusters_dict, path_prefix_lengths=(4, 6, 10, 20), min_occur=5):
        self.clusters_dict = clusters_dict

        self.path_prefix_lengths = list(path_prefix_lengths)
        self.min_occur = min_occur

    def annotate_data(self, word_list):
        for word in word_list:
            self.annotate_word(word)

    def annotate_word(self, word):
        setattr(word, self.ANNOTATION_ATTRIBUTE, self.get_word_prefixes(word.text))

    def get_word_prefixes(self, word_text):
        brown_prefix_features = list()
        for cluster_name, cluster in self.clusters_dict.iteritems():
            if word_text in cluster:
                word_cluster_path, word_occur = cluster[word_text]

                if word_occur > self.min_occur:
                    cluster_prefix_list = self._generate_path_prefix_list(word_cluster_path)
                    cluster_prefix_features = map(lambda path_prefix: "%s_%s" % (cluster_name, path_prefix),
                                                  cluster_prefix_list)
                    brown_prefix_features.extend(cluster_prefix_features)

        return brown_prefix_features

    def _generate_path_prefix_list(self, brown_path):
        path_prefix_list = list()
        for prefix_len in self.path_prefix_lengths:
            path_prefix_list.append(brown_path[:prefix_len])
            if prefix_len >= len(brown_path):
                break
        return path_prefix_list


def parse_brown_clusters_directory(brown_clusters_dir_path):
    clusters_dict = dict()

    for cluster_name in os.listdir(brown_clusters_dir_path):
        cluster_path = os.path.join(brown_clusters_dir_path, cluster_name)
        with open(cluster_path, 'rb') as cluster_file:
            data = cluster_file.read()

        current_cluster_dict = dict()
        for line in data.splitlines():
            path, word, num_occur = line.split()
            current_cluster_dict[word] = (path, int(num_occur))

        clusters_dict[cluster_name] = current_cluster_dict
    return clusters_dict


def create_brwon_annotator(brown_clusters_dir_path):
    clusters_dict = parse_brown_clusters_directory(brown_clusters_dir_path)
    return BrownAnnotator(clusters_dict)
