from django import forms
from django.views.generic.edit import FormView

from haystack.query import SearchQuerySet

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
    return SearchQuerySet().auto_query(query)
