from django.db import models

class Source(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=300)
    content = models.TextField()
    image = models.URLField(blank=True)
    url = models.URLField()
    published_at = models.DateTimeField()
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title
