from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def blog_home(request):
    context = {'blogs': BlogModel.objects.all()}
    return render(request, 'home.html', context)


@login_required(login_url='login')
def blog_detail(request, slug):
    context = {}
    try:
        blog_obj = BlogModel.objects.filter(slug=slug).first()
        context['blog_obj'] = blog_obj
    except Exception as e:
        print(e)
    return render(request, 'blog_detail.html', context)

@login_required(login_url='login')
def see_blog(request):
    context = {}
    try:
        blog_objs = BlogModel.objects.filter(user=request.user)
        context['blog_objs'] = blog_objs
    except Exception as e:
        print(e)

    return render(request, 'see_blog.html', context)

@login_required(login_url='login')
def add_blog(request):
    try:
        if request.method == 'POST':
            form = BlogForm(request.POST)
            user = request.user
            title = request.POST.get('title')
            image = request.FILES.get('image')

            if form.is_valid():
                content = form.cleaned_data['content']
                blog_obj = BlogModel.objects.create(
                    user=user, title=title, content=content, image=image
                )
                return redirect('blog')
    except Exception as e:
        print(e)

    return render(request, 'add_blog.html', {'form': BlogForm()})


@login_required(login_url='login')
def blog_update(request, slug):
    try:
        blog_obj = get_object_or_404(BlogModel, slug=slug)

        if blog_obj.user != request.user:
            return redirect('blog')

        if request.method == 'POST':
            form = BlogForm(request.POST, request.FILES, instance=blog_obj)
            title = request.POST.get('title')
            blog_obj.title = title
            
            image = request.FILES.get('image')
            if image:
                blog_obj.image = image

            if form.is_valid():
                form.save()
                return redirect('see_blog')
        else:
            form = BlogForm(instance=blog_obj)
    except Exception as e:
        print(e)

    return render(request, 'update_blog.html', {'blog_obj': blog_obj, 'form': form})

@login_required(login_url='login')
def blog_delete(request, id):
    context = {}
    try:
        blog_obj = BlogModel.objects.get(id=id)

        if request.method == 'POST':
            blog_obj.delete()
            return redirect('see_blog')
        context['blog_obj'] = blog_obj
    except Exception as e:
        print(e)

    return render(request, 'confirm_delete.html', context)