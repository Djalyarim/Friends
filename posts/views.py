from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CommentForm, PostForm
from .models import Comment, Follow, Group, Post, User


def index(request):
    post_list = Post.objects.all().order_by('-pub_date')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'index.html',
                  {'page': page})


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = Post.objects.filter(group=group).order_by('-pub_date')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(
        request, 'group.html',
        {'group': group, 'page': page}
    )


@login_required
def new_post(request):
    if request.method != 'POST':
        form = PostForm()
        return render(request, 'post_add.html', {'form': form})
    form = PostForm(request.POST)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('index')
    return render(request, 'post_add.html', {'form': form})


def profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user).order_by('id')\
                                            .order_by('-pub_date')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    if request.user.username != '':
        following = Follow.objects.filter(user=request.user,
                                          author=user).exists()
    else:
        following = False
    follower_count = Follow.objects.filter(user=user).count()
    following_count = Follow.objects.filter(author=user).count()
    return render(
        request,
        'profile.html',
        {
            'profile': user,
            'user': request.user,
            'page': page,
            'posts_count': posts.count,
            'following': following,
            'follower_count': follower_count,
            'following_count': following_count,
        }
    )


def post_view(request, username, post_id):
    user = get_object_or_404(User, username=username)
    post = Post.objects.select_related('author', 'group')\
        .filter(author__username=username, id=post_id)[0]
    posts_count = Post.objects.filter(author__username=username).count
    comments = Comment.objects.filter(post=post)
    form = CommentForm()
    follower_count = Follow.objects.filter(user=user).count()
    following_count = Follow.objects.filter(author=user).count()
    return render(
        request,
        'post.html',
        {
            'post': post,
            'posts_count': posts_count,
            'author': post.author,
            'comments': comments,
            'form': form,
            'follower_count': follower_count,
            'following_count': following_count,
        }
    )


@login_required
def add_comment(request, username, post_id):
    post = get_object_or_404(Post, pk=post_id, author__username=username)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('post', username=username, post_id=post_id)


@login_required
def post_edit(request, username, post_id):
    if request.user.username != username:
        return redirect('post', username=username, post_id=post_id)
    post = get_object_or_404(Post.objects.filter(id=post_id))
    form = PostForm(request.POST or None,
                    files=request.FILES or None, instance=post)
    if not form.is_valid():
        return render(request, 'post_add.html', {'form': form, 'post': post})
    form.save()
    return redirect('post', username=username, post_id=post_id)


@login_required
def follow_index(request):
    follow = Follow.objects.filter(user__id=request.user.id)\
                           .values_list('author__id', flat=True).distinct()
    posts = Post.objects.filter(author__in=follow).order_by('id')\
                                                  .order_by('-pub_date')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'follow.html', {
        'page': page,
        'paginator': paginator})


@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    if Follow.objects.filter(user=request.user,
                             author=author).exists() is False:
        if author != request.user:
            follow = Follow.objects.create(user=request.user, author=author)
            follow.save()
    return redirect('profile', username=username)


@login_required
def profile_unfollow(request, username):
    author = get_object_or_404(User, username=username)
    if Follow.objects.filter(user=request.user, author=author).exists():
        Follow.objects.filter(user=request.user, author=author).delete()
    return redirect('profile', username=username)


def page_not_found(request, exception):
    # Переменная exception содержит отладочную информацию,
    # выводить её в шаблон пользователской страницы 404 мы не станем
    return render(
        request,
        'misc/404.html',
        {'path': request.path},
        status=404
    )


def server_error(request):
    return render(request, 'misc/500.html', status=500)
