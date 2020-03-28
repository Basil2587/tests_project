from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostForm
from .models import Post, Group, User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


def index(request):
    post_list = Post.objects.order_by("-pub_date").all()
    paginator = Paginator(post_list, 10) # показывать по 10 записей на странице.
    page_number = request.GET.get('page') # переменная в URL с номером запрошенной страницы
    page = paginator.get_page(page_number) # получить записи с нужным смещением
    return render(request, 'index.html', {'page': page, 'paginator': paginator})

def group_posts(request, slug):
    # функция get_object_or_404 позволяет получить объект из базы данных 
    # по заданным критериям или вернуть сообщение об ошибке если объект не найден
    group = get_object_or_404(Group, slug=slug)
    # Метод .filter позволяет ограничить поиск по критериям. Это аналог добавления
    # условия WHERE group_id = {group_id}
    posts = Post.objects.filter(group=group).order_by("-pub_date").all()
    paginator = Paginator(posts, 12) # показывать по 12 записей на странице.
    page_number = request.GET.get('page') # переменная в URL с номером запрошенной страницы
    page = paginator.get_page(page_number)
    return render(request, "group.html", {"group": group, 'page': page, "paginator": paginator})

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('index')
    else:
        form = PostForm()
    return render(request, 'post_edit.html', {'form': form})

def profile(request, username):
    profile = get_object_or_404(User, username=username)
    post_numbers =  Post.objects.filter(author=profile).all().count()
    posts = Post.objects.filter(author=profile).order_by("-pub_date").all()
    paginator = Paginator(posts, 5) # показывать по 5 записей на странице.
    page_number = request.GET.get('page') # переменная в URL с номером запрошенной страницы
    page = paginator.get_page(page_number)
    context = {
        'post_numbers': post_numbers,  
        "profile": profile, 
        'page': page, 
        "paginator": paginator,
        }
    return render(request, "profile.html", context)

def post_view(request, username, post_id):
    profile = get_object_or_404(User, username=username)
    post_numbers =  Post.objects.filter(author=profile).all().count()
    posts = Post.objects.get(id=post_id)
    return render(request, "post.html", {'posts': posts, 'post_numbers': post_numbers, "profile": profile})

def post_edit(request, username, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("post", username, post_id)
    else:
        form = PostForm(instance=post)
    return render(request, "post_edit.html", {'form': form, "post": post})