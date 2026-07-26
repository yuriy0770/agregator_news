from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Article, Category


def index(request):
    categories = Category.objects.all()
    articles_list = Article.objects.all().order_by('-published_at')

    paginator = Paginator(articles_list, 6)
    page_number = request.GET.get('page')
    articles = paginator.get_page(page_number)

    return render(request, 'main/index.html', {
        'categories': categories,
        'articles': articles,
    })


def category_view(request, slug):
    category = get_object_or_404(Category, slug=slug)
    categories = Category.objects.all()
    articles_list = Article.objects.filter(category=category).order_by('-published_at')

    paginator = Paginator(articles_list, 6)
    page_number = request.GET.get('page')
    articles = paginator.get_page(page_number)

    return render(request, 'main/category.html', {
        'category': category,
        'categories': categories,
        'articles': articles,
    })


def search_view(request):
    query = request.GET.get('q', '')
    categories = Category.objects.all()

    if query:
        articles_list = Article.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        ).order_by('-published_at')
    else:
        articles_list = Article.objects.none()

    paginator = Paginator(articles_list, 6)
    page_number = request.GET.get('page')
    articles = paginator.get_page(page_number)

    return render(request, 'main/search.html', {
        'categories': categories,
        'articles': articles,
        'query': query,
    })