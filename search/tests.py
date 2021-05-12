from unittest import TestCase

from .utils import document_pre_processing, clean_paragraph_words, rank_top_ten_paragraph, \
    create_inverted_index_dict, get_paragraph_list, get_search_results


class TestDocumentPreProcessing(TestCase):

    def setUp(self) -> None:
        self.document = 'This is one.\n\n Is this a two.\n\n Three is this.\n'

    def test_pre_processing_correct(self):
        item = {
            1: 'this is one.',
            2: 'is this a two.',
            3: 'three is this.'
        }
        modified_indexed_para, original_indexed_para = document_pre_processing(self.document)
        self.assertDictEqual(modified_indexed_para, item)

    def test_pre_processing_incorrect_space(self):
        item = {
            1: 'this is one.',
            2: ' is this a two.',
            3: ' three is this.'
        }
        modified_indexed_para, original_indexed_para = document_pre_processing(self.document)
        self.assertNotEqual(modified_indexed_para, item)

    def test_pre_processing_incorrect_case(self):
        item = {
            1: 'This is one.',
            2: 'Is this a two.',
            3: 'Three is this.'
        }
        modified_indexed_para, original_indexed_para = document_pre_processing(self.document)
        self.assertNotEqual(modified_indexed_para, item)


class TestCleanParagraphWords(TestCase):

    def setUp(self) -> None:
        self.document = "Adam's apple.\n\n Adam, Sam & I is a two.\n\n He is Adam.\n"

    def test_clean_paragraph_words_correct(self):
        expected_list = ['Adam', 's',  'apple', 'Adam', 'Sam', 'I', 'is',
                         'a', 'two', 'He', 'is', 'Adam']
        self.assertListEqual(clean_paragraph_words(self.document),
                             expected_list)

    def test_clean_paragraph_words_incorrect(self):
        expected_list = ["Adam's", 'apple.', 'Adam,', 'Sam', '&', 'I', 'is',
                         'a', 'two.', 'He', 'is', 'Adam.']
        self.assertNotEqual(clean_paragraph_words(self.document),
                            expected_list)


class TestRankTopTenParagraph(TestCase):
    def setUp(self) -> None:
        self.paragraph_index_list = [1, 3]
        self.indexed_paragraphs_dict = {
            1: "adam s apple",
            2: "he is ",
            3: "adam, sam   adam is a two",
        }
        self.input_word = 'adam'

    def test_rank_top_ten_paragraph_correct(self):
        expected_list = [3, 1]
        self.assertListEqual(
            rank_top_ten_paragraph(self.paragraph_index_list,
                                   self.indexed_paragraphs_dict,
                                   self.input_word),
            expected_list)

    def test_rank_top_ten_paragraph_incorrect(self):
        expected_list = [1, 3]
        self.assertNotEqual(
            rank_top_ten_paragraph(self.paragraph_index_list,
                                   self.indexed_paragraphs_dict,
                                   self.input_word),
            expected_list)


class TestCreateInvertedIndexDict(TestCase):

    def setUp(self) -> None:
        self.indexed_paras = {
            1: "adam s apple",
            2: "he is ",
            3: "adam  sam   adam is a two",
        }

    def test_rank_top_ten_paragraph_correct(self):
        expected_result = {
            'adam': [1, 3],
            's': [1],
            'apple': [1],
            'he': [2],
            'is': [2, 3],
            'sam': [3],
            'a': [3],
            'two': [3]
        }
        actual_result = create_inverted_index_dict(self.indexed_paras)
        self.assertDictEqual(expected_result, actual_result)


class TestGetParagraphList(TestCase):
    def setUp(self) -> None:
        self.inverted_index_dict = {
            'adam': [1, 3],
            's': [1],
            'apple': [1],
            'he': [2],
            'is': [2, 3],
            'sam': [3],
            'a': [3],
            'two': [3]
        }
        self.search_key = 'adam'
        self.indexed_paras = {
            1: "adam s apple",
            2: "he is ",
            3: "adam  sam   adam is a two",
        }

    def test_get_paragraph_list_correct(self):
        expected_result = [
            {
                'index': 3,
                'paragraph': "adam  sam   adam is a two"
            },
            {
                'index': 1,
                'paragraph': "adam s apple"
            },

        ]
        actual_result = get_paragraph_list(self.inverted_index_dict,
                                           self.search_key,
                                           self.indexed_paras)
        self.assertListEqual(expected_result, actual_result)


class TestGetSearchResults(TestCase):
    def setUp(self) -> None:
        self.document = "Adam's apple.\n\n Adamm, Sam & I is a two.\n\n He is Adam.\n"
        self.search_key = 'adam'

    def test_get_search_results_correct(self):
        expected_result = {
            'has_result': True,
            'result': [
                        {
                            'index': 1,
                            'paragraph': "Adam's apple."
                        },
                        {
                            'index': 3,
                            'paragraph': " He is Adam."
                        },
                    ],
            'total': 2
        }
        actual_result = get_search_results(self.document, self.search_key)
        self.assertEqual(expected_result, actual_result)

    def test_get_search_results_incorrect(self):
        expected_result = {
            'has_result': True,
            'result': [
                        {
                            'index': 3,
                            'paragraph': " he is adam."
                        },
                        {
                            'index': 1,
                            'paragraph': "adam's apple."
                        },
                    ],
            'total': 2
        }
        actual_result = get_search_results(self.document, self.search_key)
        self.assertNotEqual(expected_result, actual_result)
