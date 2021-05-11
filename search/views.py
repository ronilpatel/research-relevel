from django.shortcuts import render

from search.utils import document_pre_processing, \
    create_inverted_index_dict, rank_top_ten_paragraph


def reSearchView(request, ):

    if request.method == 'POST':
        document = request.FILES['input_document'].read().decode("utf-8")
        search_key = request.POST.get('search_key').lower()

        indexed_paragraphs = document_pre_processing(doc=document)

        inverted_index_dict = create_inverted_index_dict(indexed_paras=indexed_paragraphs)

        paragraphs = dict()
        paragraphs['result'] = list()
        paragraphs['has_result'] = True

        if search_key in inverted_index_dict:
            para_index_list = inverted_index_dict[search_key]
            top_ten_paragraph_index = rank_top_ten_paragraph(para_index_list,
                                                             indexed_paragraphs, search_key)

            for para_index in top_ten_paragraph_index:
                temp = dict()
                temp['index'] = para_index
                temp['paragraph'] = indexed_paragraphs[para_index]
                paragraphs['result'].append(temp)
        else:
            paragraphs['has_result'] = False
            paragraphs['message'] = 'No such word found!'

        paragraphs['total'] = len(paragraphs['result'])

        return render(request=request,
                      template_name='searchresult.html',
                      context=paragraphs)

    else:
        return render(request=request,
                      template_name='searchform.html')
