import string, re

from django import forms
from django.views.generic.edit import FormView

from haystack.query import SearchQuerySet

from .search import syntaxes


class SearchForm(forms.Form):
    q = forms.CharField()

class Search(FormView):
    template_name = 'articles/search.html'
    form_class = SearchForm
    
    def get_form_kwargs(self):
        kwargs = super(Search, self).get_form_kwargs()
        kwargs['data'] = self.request.GET or None
        return kwargs

    def get_context_data(self, **kwargs):
        form = kwargs['form']
        if form.is_valid():
            kwargs['articles'] = search(form.cleaned_data['q'])
        return kwargs

def search(query):
    s = SearchQuerySet()

    for regex, handler in syntaxes.items():
        regex = re.compile(regex, re.I)
        matches = regex.findall(query)
        query = regex.sub('', query)
        if matches:
            s = handler(s, matches)

    # Strip leading and trailing punctuation -- fix for xapian, but shouldn't hurt for other backends
    punct = ''.join(set(string.punctuation) ^ set("'\"-"))
    querystring = ' '.join(word.strip(punct) for word in query.split())

    return s.auto_query(query)
