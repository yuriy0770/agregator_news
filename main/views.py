from django.shortcuts import render, get_object_or_404
from .models import Article, Category

def index(request):
    categories = Category.objects.all()
    articles = Article.objects.all().order_by('-published_at')[:12]
    return render(request, 'main/index.html', {
        'categories': categories,
        'articles': articles
    })

def category_view(request, slug):
    category = get_object_or_404(Category, slug=slug)
    categories = Category.objects.all()
    articles = Article.objects.filter(category=category).order_by('-published_at')
    return render(request, 'main/category.html', {
        'category': category,
        'categories': categories,
        'articles': articles
    })