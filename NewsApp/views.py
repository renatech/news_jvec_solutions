from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from .models import Category, Post,Comment
from django.contrib.messages.views import SuccessMessageMixin, messages
from .forms import CommentForm

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from rest_framework import generics
from .models import Post
from .serializer import PostSerializer

from .tasks import test_func


def test(request):
    test_func.delay()
    return HttpResponse("Done")

def home(request):
    categories = Category.objects.all()
    selected_category = request.GET.get('category')
    posts = Post.objects.filter(category__name=selected_category) if selected_category else Post.objects.all()

    post_with_highest_views = posts.order_by('-views').first()
    more_posts = posts.exclude(id=post_with_highest_views.id)

    page = request.GET.get('page', 1)
    paginator = Paginator(posts, 11)  # Change 10 to the number of posts per page you desire

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        'categories': categories,
        'selected_category': selected_category,
        'post_with_highest_views': post_with_highest_views,
        'more_posts': posts,
    }

    return render(request, 'index.html', context)


def article_detail(request, post_id,slug):
    post = get_object_or_404(Post, id=post_id, slug=slug)
    post.views += 1
    post.save()
    comment = Comment.objects.filter(post=post).order_by('id')
    if request.method == 'POST':
        comment_form = CommentForm(request.POST or None)
        if comment_form.is_valid():
            content = request.POST.get('comment')
            comments = Comment.objects.create(post=post, name=request.user, comment=content)
            comments.save()
            messages.success(request, 'Your comment has being posted successfully')
            return redirect(post.get_absolute_url())
    else:
        comment_form = CommentForm()

    context = {
        'post': post,
        'comment': comment,
        'comment_form': comment_form,
    }
    return render(request, 'article.html', context)


# API VIEWS
class PostListView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class PostCreateView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
