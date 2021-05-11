from django.views import View
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from search.utils import get_search_results


class ReSearchView(View):

    def post(self, request):

        document = request.FILES['input_document'].read().decode("utf-8")
        search_key = request.POST.get('search_key').lower()

        paragraphs = get_search_results(document, search_key)
        print(f'paragraphs in post is: {paragraphs}')

        # return HttpResponseRedirect(redirect_to='searchresult.html',
        #                             **paragraphs)
        return render(request=request,
                      template_name='searchresult.html',
                      context=paragraphs)

    def get(self, request):
        return render(request=request,
                      template_name='searchform.html',
                      context=dict())
