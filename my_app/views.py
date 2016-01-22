from django.shortcuts import render, get_object_or_404
from blog.models import Blog
 
def index(request):
    # get the blog posts that are published
    posts = Blog.objects.filter(published=True)[:5]

    # now return the rendered template
    return render(request, 'blog/index.html', {'posts': posts})
 
def post(request, slug):
    # get the Blog object
    post = get_object_or_404(Blog, slug=slug)
    # now return the rendered template
    return render(request, 'blog/post.html', {'post': post})
