from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.views.generic import ListView
from taggit.models import Tag


from .models import Post
from .forms import EmailPostForm

from comments.forms import CommentForm

# Create your views here.

def post_share(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    data = {}
    sent = False

    if request.method == "POST":
        form = EmailPostForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            post_url = request.build_absolute_uri(
                post.get_absolute_url())

            subject = '{} ({}) recommends you reading {}'.format(
                data['name'], data['email'], post.title)
            message = 'Read "{}" at {}\n\nComment:\n{}'.format(
                post.title, post_url, data.get('comment', 'No comment'))

            sending = send_mail(subject, message, data['email'], [data['to']],
                                fail_silently=False)

            if sending:
                sent = True

    else:
        form = EmailPostForm()
    
    context = {
        "post": post,
        "form": form,
        "sent" : sent,
        "form_data": data
    }

    return render(request,
                  'blog/post/share_email.html',
                  context)



class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 2
    template_name = 'blog/post/list.html'



def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 2)

    page = request.GET.get('page', 1)

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        'posts': posts,
        'page': page,
        'tag': tag
    }

    return render(request,
                  'blog/post/list.html',
                  context)

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)

    similiar_posts = post.get_similiar_posts()

    comments = post.comments.filter(active=True)

    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        form = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        'form': form,
        'similiar_posts': similiar_posts
    }

    return render(request,
                  'blog/post/detail.html',
                  context)
