from collections import defaultdict


def document_pre_processing(doc):
    """
    input: string
    output: dict

    Purpose:
        1. Remove trailing & leading spaces
        2. Splits the entire doc into paragraphs
        3. Index the paragraph with a unique number
        4. Create a dict with unique number as key and paragraph as value
    Returns a dictionary of paragraphs indexed by a unique number
    """
    doc_without_trailing_spaces = doc.strip()

    paragraphs = doc_without_trailing_spaces.split('\n\n')

    indexed_paragraphs = {index+1: value.lower() for index, value in enumerate(paragraphs)}
    return indexed_paragraphs


def clean_paragraph_words(paragraph):
    """
    input: String
    output: List
    Purpose:
        1. Replace puntuations in between strings with spaces
        2. Ruturns a list of all the words in the paragraph
    """
    punc = """!()-[]{};:'"\, <>./?@#$%^&*_~"""
    for ele in paragraph:
        if ele in punc:
            paragraph = paragraph.replace(ele, ' ')

    return paragraph.split()


def rank_top_ten_paragraph(paragraph_index_list, indexed_paragraphs_dict, input_word):
    """
    Rank paragraph indexes on the basis of word frequency in those paragraphs
    """
    word_frequency_dict = defaultdict(int)
    for index in paragraph_index_list:
        paragraph = indexed_paragraphs_dict[index]
        word_count = paragraph.count(input_word)
        word_frequency_dict[index] = word_count

    word_frequency_dict = dict(word_frequency_dict)
    frequency_ranked_dict = sorted(word_frequency_dict.items(),
                                   key=lambda kv: kv[1],
                                   reverse=True)
    ranked_index_list = frequency_ranked_dict[:10]

    return [key for key, value in ranked_index_list]


def create_inverted_index_dict(indexed_paras):
    inverted_index_dict_store = defaultdict(list)

    for paragraph_index in indexed_paras:
        words = clean_paragraph_words(indexed_paras[paragraph_index])

        for word in words:
            inverted_index_dict_store[word].append(paragraph_index)
            inverted_index_dict_store[word] = list(set(inverted_index_dict_store[word]))

    inverted_index_dict_store = dict(inverted_index_dict_store)
    return inverted_index_dict_store


def get_paragraph_list(inverted_index_dict, search_key, indexed_paragraphs):
    para_list = list()

    para_index_list = inverted_index_dict[search_key]
    top_ten_paragraph_index = rank_top_ten_paragraph(para_index_list,
                                                     indexed_paragraphs, search_key)

    for para_index in top_ten_paragraph_index:
        para_list.append({
            'index': para_index,
            'paragraph': indexed_paragraphs[para_index]
        })

    return para_list


def get_search_results(document, search_key):
    paragraphs = dict()
    paragraphs['has_result'] = True
    paragraphs['result'] = list()

    indexed_paragraphs = document_pre_processing(doc=document)

    inverted_index_dict = create_inverted_index_dict(indexed_paras=indexed_paragraphs)

    if search_key in inverted_index_dict:
        paragraphs['result'] = get_paragraph_list(inverted_index_dict=inverted_index_dict,
                                                  search_key=search_key,
                                                  indexed_paragraphs=indexed_paragraphs)

    else:
        paragraphs['has_result'] = False
        paragraphs['message'] = 'No such word found!'

    paragraphs['total'] = len(paragraphs['result'])

    return paragraphs
