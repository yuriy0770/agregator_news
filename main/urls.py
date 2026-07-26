from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    path('category/<slug:slug>/', views.category_view, name='category'),
    path('search/', views.search_view, name='search'),  # 👈 ДОБАВЬ ЭТО
]