from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CommentForm, PostForm, ProfileForm
from .models import Follow, Group, Post, Profile_id, User


def index(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'index.html',
                  {'page': page})


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = Post.objects.filter(group=group)
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
    form = PostForm(request.POST, files=request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('index')
    return render(request, 'post_add.html', {'form': form})
 
# @login_required
# def profile_edit(request, username):

@login_required
def profile_edit(request):
    profile = Profile_id.objects.get_or_create(author=request.user)[0]
    if request.method != 'POST':
        form = ProfileForm()
        return render(request, 'profile_edit.html', {'form': form})
    # __import__('pdb').set_trace()
    form = ProfileForm(request.POST or None, files=request.FILES or None, instance=profile)
    if not form.is_valid:
        return render(request, 'profile_edit.html', {'form': form})
    form.save()
    # if form.is_valid():
    #     profile = form.save(commitç=False)
    #     profile.author = request.user
    #     profile.save()
    #     return redirect('profile', username=request.user.username)
    # return render(request, 'profile_edit.html', {'form': form})
    return redirect('profile', username=request.user.username)
    # form.save()
    # return redirect('profile', username=request.user.username)



def profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user)
    # profile_id = get_object_or_404(Profile_id, author=request.user)
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    if request.user.is_authenticated:
        following = Follow.objects.filter(user=request.user,
                                          author=user).exists()
    else:
        following = False
    return render(
        request,
        'profile.html',
        {
            # 'profile_id': profile_id,
            'profile': user,
            'user': request.user,
            'page': page,
            'following': following,
        }
    )






def post_view(request, username, post_id):
    user = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, author__username=username, pk=post_id)
    form = CommentForm()
    return render(
        request,
        'post.html',
        {
            'profile': user,
            'post': post,
            'comments': post.comments.all(),
            'form': form,
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
    post = get_object_or_404(Post, id=post_id, author__username=username)
    if request.user != post.author:
        return redirect('post', username=username, post_id=post_id)
    form = PostForm(request.POST or None,
                    files=request.FILES or None, instance=post)
    if not form.is_valid():
        return render(request, 'post_add.html', {'form': form, 'post': post})
    form.save()
    return redirect('post', username=username, post_id=post_id)


@login_required
def follow_index(request):
    posts = Post.objects.filter(author__following__user=request.user)
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'follow.html', {
        'page': page,
        'paginator': paginator})


@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    if author != request.user:
        Follow.objects.get_or_create(user=request.user, author=author)
    return redirect('profile', username=username)


@login_required
def profile_unfollow(request, username):
    author = get_object_or_404(User, username=username)
    Follow.objects.filter(user=request.user, author=author).delete()
    return redirect('profile', username=username)


def page_not_found(request, exception):
    return render(
        request,
        'misc/404.html',
        {'path': request.path},
        status=404
    )


def server_error(request):
    return render(request, 'misc/500.html', status=500)
