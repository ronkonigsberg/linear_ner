from nertagger.parser import parse_conll_train, parse_conll_tagged


EXAMPLE_CONLL_TRAIN_FILE = \
"""-DOCSTART-\r -X- O O
\r\x20
EU\r NNP I-NP I-ORG
rejects\r VBZ I-VP O
German\r JJ I-NP I-MISC
call\r NN I-NP O
.\r . O O
\r\x20
Peter\r NNP I-NP I-PER
Blackburn\r NNP I-NP I-PER
\r\x20
It\r PRP I-NP O
brought\r VBD I-VP O
in\r IN I-PP O
imports\r NNS I-NP O
.\r . O O
\r\x20
-DOCSTART-\r -X- O O
\r\x20
Swansea\r NN I-NP I-ORG
1\r CD I-NP O
Lincoln\r NNP I-NP I-ORG
2\r CD I-NP O
\r\x20
"""

EXPECTED_PARSED_TRAIN_FILE_UNITE_DOCUMENTS = [
    [
        [
            {'text': 'EU',          'pos': 'NNP',   'chunk': 'I-NP',    'gold_label': 'I-ORG'},
            {'text': 'rejects',     'pos': 'VBZ',   'chunk': 'I-VP',    'gold_label': 'O'},
            {'text': 'German',      'pos': 'JJ',    'chunk': 'I-NP',    'gold_label': 'I-MISC'},
            {'text': 'call',        'pos': 'NN',    'chunk': 'I-NP',    'gold_label': 'O'},
            {'text': '.',           'pos': '.',     'chunk': 'O',       'gold_label': 'O'},
        ],

        [
            {'text': 'Peter',       'pos': 'NNP',   'chunk': 'I-NP',    'gold_label': 'I-PER'},
            {'text': 'Blackburn',   'pos': 'NNP',   'chunk': 'I-NP',    'gold_label': 'I-PER'},
        ],

        [
            {'text': 'It',          'pos': 'PRP',   'chunk': 'I-NP',    'gold_label': 'O'},
            {'text': 'brought',     'pos': 'VBD',   'chunk': 'I-VP',    'gold_label': 'O'},
            {'text': 'in',          'pos': 'IN',    'chunk': 'I-PP',    'gold_label': 'O'},
            {'text': 'imports',     'pos': 'NNS',   'chunk': 'I-NP',    'gold_label': 'O'},
            {'text': '.',           'pos': '.',     'chunk': 'O',       'gold_label': 'O'},
        ],

        [
            {'text': 'Swansea',     'pos': 'NN',    'chunk': 'I-NP',    'gold_label': 'I-ORG'},
            {'text': '1',           'pos': 'CD',    'chunk': 'I-NP',    'gold_label': 'O'},
            {'text': 'Lincoln',     'pos': 'NNP',   'chunk': 'I-NP',    'gold_label': 'I-ORG'},
            {'text': '2',           'pos': 'CD',    'chunk': 'I-NP',    'gold_label': 'O'},
        ]
    ]
]

EXPECTED_PARSED_TRAIN_FILE_SEPARATE_DOCUMENTS = [
    [
        [
            {'text': 'EU',          'pos': 'NNP',   'chunk': 'I-NP',    'gold_label': 'I-ORG'},
            {'text': 'rejects',     'pos': 'VBZ',   'chunk': 'I-VP',    'gold_label': 'O'},
            {'text': 'German',      'pos': 'JJ',    'chunk': 'I-NP',    'gold_label': 'I-MISC'},
            {'text': 'call',        'pos': 'NN',    'chunk': 'I-NP',    'gold_label': 'O'},
            {'text': '.',           'pos': '.',     'chunk': 'O',       'gold_label': 'O'},
        ],

        [
            {'text': 'Peter',       'pos': 'NNP',   'chunk': 'I-NP',    'gold_label': 'I-PER'},
            {'text': 'Blackburn',   'pos': 'NNP',   'chunk': 'I-NP',    'gold_label': 'I-PER'},
        ],

        [
            {'text': 'It',          'pos': 'PRP',   'chunk': 'I-NP',    'gold_label': 'O'},
            {'text': 'brought',     'pos': 'VBD',   'chunk': 'I-VP',    'gold_label': 'O'},
            {'text': 'in',          'pos': 'IN',    'chunk': 'I-PP',    'gold_label': 'O'},
            {'text': 'imports',     'pos': 'NNS',   'chunk': 'I-NP',    'gold_label': 'O'},
            {'text': '.',           'pos': '.',     'chunk': 'O',       'gold_label': 'O'},
        ],
    ],


    [
        [
            {'text': 'Swansea',     'pos': 'NN',    'chunk': 'I-NP',    'gold_label': 'I-ORG'},
            {'text': '1',           'pos': 'CD',    'chunk': 'I-NP',    'gold_label': 'O'},
            {'text': 'Lincoln',     'pos': 'NNP',   'chunk': 'I-NP',    'gold_label': 'I-ORG'},
            {'text': '2',           'pos': 'CD',    'chunk': 'I-NP',    'gold_label': 'O'},
        ]
    ]
]


EXAMPLE_CONLL_TAGGED_FILE = \
"""-DOCSTART-\r -X- O O

EU\r NNP I-NP I-ORG TAG1
rejects\r VBZ I-VP O TAG2
German\r JJ I-NP I-MISC TAG3
call\r NN I-NP O TAG4
.\r . O O TAG5

Peter\r NNP I-NP I-PER TAG6
Blackburn\r NNP I-NP I-PER TAG7

It\r PRP I-NP O TAG8
brought\r VBD I-VP O TAG9
in\r IN I-PP O TAG10
imports\r NNS I-NP O TAG11
.\r . O O TAG12

-DOCSTART-\r -X- O O

Swansea\r NN I-NP I-ORG TAG13
1\r CD I-NP O TAG14
Lincoln\r NNP I-NP I-ORG TAG15
2\r CD I-NP O TAG16

"""

EXPECTED_PARSED_TAGGED_FILE_UNITE_DOCUMENTS = [
    [
        [
            {'text': 'EU',          'pos': 'NNP',   'chunk': 'I-NP',    'gold_label': 'I-ORG',      'tag': 'TAG1'},
            {'text': 'rejects',     'pos': 'VBZ',   'chunk': 'I-VP',    'gold_label': 'O',          'tag': 'TAG2'},
            {'text': 'German',      'pos': 'JJ',    'chunk': 'I-NP',    'gold_label': 'I-MISC',     'tag': 'TAG3'},
            {'text': 'call',        'pos': 'NN',    'chunk': 'I-NP',    'gold_label': 'O',          'tag': 'TAG4'},
            {'text': '.',           'pos': '.',     'chunk': 'O',       'gold_label': 'O',          'tag': 'TAG5'},
        ],

        [
            {'text': 'Peter',       'pos': 'NNP',   'chunk': 'I-NP',    'gold_label': 'I-PER',      'tag': 'TAG6'},
            {'text': 'Blackburn',   'pos': 'NNP',   'chunk': 'I-NP',    'gold_label': 'I-PER',      'tag': 'TAG7'},
        ],

        [
            {'text': 'It',          'pos': 'PRP',   'chunk': 'I-NP',    'gold_label': 'O',          'tag': 'TAG8'},
            {'text': 'brought',     'pos': 'VBD',   'chunk': 'I-VP',    'gold_label': 'O',          'tag': 'TAG9'},
            {'text': 'in',          'pos': 'IN',    'chunk': 'I-PP',    'gold_label': 'O',          'tag': 'TAG10'},
            {'text': 'imports',     'pos': 'NNS',   'chunk': 'I-NP',    'gold_label': 'O',          'tag': 'TAG11'},
            {'text': '.',           'pos': '.',     'chunk': 'O',       'gold_label': 'O',          'tag': 'TAG12'},
        ],

        [
            {'text': 'Swansea',     'pos': 'NN',    'chunk': 'I-NP',    'gold_label': 'I-ORG',      'tag': 'TAG13'},
            {'text': '1',           'pos': 'CD',    'chunk': 'I-NP',    'gold_label': 'O',          'tag': 'TAG14'},
            {'text': 'Lincoln',     'pos': 'NNP',   'chunk': 'I-NP',    'gold_label': 'I-ORG',      'tag': 'TAG15'},
            {'text': '2',           'pos': 'CD',    'chunk': 'I-NP',    'gold_label': 'O',          'tag': 'TAG16'},
        ]
    ]
]

EXPECTED_PARSED_TAGGED_FILE_SEPARATE_DOCUMENTS = [
    [
        [
            {'text': 'EU',          'pos': 'NNP',   'chunk': 'I-NP',    'gold_label': 'I-ORG',      'tag': 'TAG1'},
            {'text': 'rejects',     'pos': 'VBZ',   'chunk': 'I-VP',    'gold_label': 'O',          'tag': 'TAG2'},
            {'text': 'German',      'pos': 'JJ',    'chunk': 'I-NP',    'gold_label': 'I-MISC',     'tag': 'TAG3'},
            {'text': 'call',        'pos': 'NN',    'chunk': 'I-NP',    'gold_label': 'O',          'tag': 'TAG4'},
            {'text': '.',           'pos': '.',     'chunk': 'O',       'gold_label': 'O',          'tag': 'TAG5'},
        ],

        [
            {'text': 'Peter',       'pos': 'NNP',   'chunk': 'I-NP',    'gold_label': 'I-PER',      'tag': 'TAG6'},
            {'text': 'Blackburn',   'pos': 'NNP',   'chunk': 'I-NP',    'gold_label': 'I-PER',      'tag': 'TAG7'},
        ],

        [
            {'text': 'It',          'pos': 'PRP',   'chunk': 'I-NP',    'gold_label': 'O',          'tag': 'TAG8'},
            {'text': 'brought',     'pos': 'VBD',   'chunk': 'I-VP',    'gold_label': 'O',          'tag': 'TAG9'},
            {'text': 'in',          'pos': 'IN',    'chunk': 'I-PP',    'gold_label': 'O',          'tag': 'TAG10'},
            {'text': 'imports',     'pos': 'NNS',   'chunk': 'I-NP',    'gold_label': 'O',          'tag': 'TAG11'},
            {'text': '.',           'pos': '.',     'chunk': 'O',       'gold_label': 'O',          'tag': 'TAG12'},
        ],
    ],


    [
        [
            {'text': 'Swansea',     'pos': 'NN',    'chunk': 'I-NP',    'gold_label': 'I-ORG',      'tag': 'TAG13'},
            {'text': '1',           'pos': 'CD',    'chunk': 'I-NP',    'gold_label': 'O',          'tag': 'TAG14'},
            {'text': 'Lincoln',     'pos': 'NNP',   'chunk': 'I-NP',    'gold_label': 'I-ORG',      'tag': 'TAG15'},
            {'text': '2',           'pos': 'CD',    'chunk': 'I-NP',    'gold_label': 'O',          'tag': 'TAG16'},
        ]
    ]
]


def test_parse_conll_train_unite_documents():
    parsed_document_list = parse_conll_train(EXAMPLE_CONLL_TRAIN_FILE, separate_to_documents=False)
    assert len(parsed_document_list) == 1
    assert parsed_document_list == EXPECTED_PARSED_TRAIN_FILE_UNITE_DOCUMENTS


def test_parse_conll_train_separate_documents():
    parsed_document_list = parse_conll_train(EXAMPLE_CONLL_TRAIN_FILE, separate_to_documents=True)
    assert len(parsed_document_list) == 2
    assert parsed_document_list == EXPECTED_PARSED_TRAIN_FILE_SEPARATE_DOCUMENTS


def test_parse_conll_test_unite_documents():
    parsed_document_list = parse_conll_tagged(EXAMPLE_CONLL_TAGGED_FILE, separate_to_documents=False)
    assert len(parsed_document_list) == 1
    assert parsed_document_list == EXPECTED_PARSED_TAGGED_FILE_UNITE_DOCUMENTS


def test_parse_conll_train_separate_documents():
    parsed_document_list = parse_conll_tagged(EXAMPLE_CONLL_TAGGED_FILE, separate_to_documents=True)
    assert len(parsed_document_list) == 2
    assert parsed_document_list == EXPECTED_PARSED_TAGGED_FILE_SEPARATE_DOCUMENTS
