import mock
from nertagger.annotators.brown_clusters import parse_brown_clusters_directory, BrownAnnotator


BROWN1_FILE_DATA = \
"""0001\tRon\t5
0010\tDraper\t6
"""

BROWN2_FILE_DATA = \
"""0100\tDon\t7
1000\tDraper\t8
"""

EXPECTED_CLUSTERS_DICT = {
    'brown1':       {'Ron':     ('0001', 5),
                      'Draper':  ('0010', 6)},

    'brown2.txt':   {'Don':     ('0100', 7),
                     'Draper':  ('1000', 8)}
}


def test_parse_brown_clusters_directory(tmpdir):
    # create gazetteers directory
    brown_cluster_dir = tmpdir.join('brown_cluster_dir')

    brown1_file = brown_cluster_dir.join('brown1')
    brown1_file.ensure()
    brown1_file.write(BROWN1_FILE_DATA)

    brown2_file = brown_cluster_dir.join('brown2.txt')
    brown2_file.ensure()
    brown2_file.write(BROWN2_FILE_DATA)

    clusters = parse_brown_clusters_directory(str(brown_cluster_dir))
    assert clusters == EXPECTED_CLUSTERS_DICT


def test_brown_get_word_prefixes():
    brown_annotator = BrownAnnotator(EXPECTED_CLUSTERS_DICT, path_prefix_lengths=[4])

    brown_annotator.min_occur = 5
    assert brown_annotator.get_word_prefixes('Ron') == []
    brown_annotator.min_occur = 4
    assert brown_annotator.get_word_prefixes('Ron') == ['brown1_0001']

    brown_annotator.path_prefix_lengths = [2, 4]
    assert brown_annotator.get_word_prefixes('Ron') == ['brown1_00', 'brown1_0001']
    brown_annotator.path_prefix_lengths = [2, 5]
    assert brown_annotator.get_word_prefixes('Ron') == ['brown1_00', 'brown1_0001']

    brown_annotator.path_prefix_lengths = [4]

    brown_annotator.min_occur = 5
    assert brown_annotator.get_word_prefixes('Don') == ['brown2.txt_0100']

    brown_annotator.min_occur = 8
    assert brown_annotator.get_word_prefixes('Draper') == []
    brown_annotator.min_occur = 6
    assert brown_annotator.get_word_prefixes('Draper') == ['brown2.txt_1000']
    brown_annotator.min_occur = 5
    assert brown_annotator.get_word_prefixes('Draper') == ['brown1_0010', 'brown2.txt_1000']


def test_brown_annotate(monkeypatch):
    brown_annotator = BrownAnnotator(EXPECTED_CLUSTERS_DICT, path_prefix_lengths=[4])

    get_prefixes_mock = mock.Mock()
    monkeypatch.setattr(brown_annotator, 'get_word_prefixes', get_prefixes_mock)
    get_prefixes_mock.return_value = ['foo', 'bar']

    word_mock = mock.Mock(text="zoo")
    brown_annotator.annotate_data([word_mock])

    assert getattr(word_mock, brown_annotator.ANNOTATION_ATTRIBUTE) == ['foo', 'bar']
    get_prefixes_mock.assert_called_once_with(word_mock.text)
