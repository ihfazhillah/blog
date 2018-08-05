from django.shortcuts import render
from haystack.query import SearchQuerySet

from .forms import SearchForm
from blog.models import Post

# Create your views here.
def search_blog_view(request):
    form = SearchForm()
    results = []
    total = 0
    data = []

    if 'q' in request.GET:
        form = SearchForm(request.GET)

        if form.is_valid():
            data = form.cleaned_data

            results = SearchQuerySet().models(Post).highlight()\
                    .filter(content=data['q']).load_all()
            total = results.count()

    context = {
        'form': form,
        'results': results,
        'total': total,
        'data': data
    }

    return render(request,
                  'blog/post/search.html',
                  context)
