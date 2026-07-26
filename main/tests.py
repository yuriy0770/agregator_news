from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import Source, Category, Article

User = get_user_model()

class SourceModelTest(TestCase):
    """Тесты для модели Source"""

    def setUp(self):
        self.source = Source.objects.create(
            name='Тестовый источник',
            url='https://test.com/rss',
            is_active=True
        )

    def test_source_creation(self):
        self.assertEqual(self.source.name, 'Тестовый источник')
        self.assertEqual(self.source.url, 'https://test.com/rss')
        self.assertTrue(self.source.is_active)

    def test_source_str(self):
        self.assertEqual(str(self.source), 'Тестовый источник')


class CategoryModelTest(TestCase):
    """Тесты для модели Category"""

    def setUp(self):
        self.category = Category.objects.create(
            name='Технологии',
            slug='technology'
        )

    def test_category_creation(self):
        self.assertEqual(self.category.name, 'Технологии')
        self.assertEqual(self.category.slug, 'technology')

    def test_category_str(self):
        self.assertEqual(str(self.category), 'Технологии')


class ArticleModelTest(TestCase):
    """Тесты для модели Article"""

    def setUp(self):
        self.source = Source.objects.create(
            name='Тестовый источник',
            url='https://test.com/rss',
            is_active=True
        )
        self.category = Category.objects.create(
            name='Технологии',
            slug='technology'
        )
        self.article = Article.objects.create(
            title='Тестовая новость',
            content='Это тестовое содержание новости',
            url='https://test.com/news/1',
            published_at=timezone.now(),
            source=self.source,
            category=self.category
        )

    def test_article_creation(self):
        self.assertEqual(self.article.title, 'Тестовая новость')
        self.assertEqual(self.article.content, 'Это тестовое содержание новости')
        self.assertEqual(self.article.source.name, 'Тестовый источник')
        self.assertEqual(self.article.category.name, 'Технологии')

    def test_article_str(self):
        self.assertEqual(str(self.article), 'Тестовая новость')


class UserModelTest(TestCase):
    """Тесты для модели пользователя"""

    def test_create_user(self):
        user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123'
        )
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@test.com')
        self.assertTrue(user.check_password('testpass123'))


class ViewsTest(TestCase):
    """Тесты для представлений"""

    def setUp(self):
        self.source = Source.objects.create(
            name='Тестовый источник',
            url='https://test.com/rss',
            is_active=True
        )
        self.category = Category.objects.create(
            name='Технологии',
            slug='technology'
        )
        self.article = Article.objects.create(
            title='Тестовая новость',
            content='Тестовое содержание',
            url='https://test.com/news/1',
            published_at=timezone.now(),
            source=self.source,
            category=self.category
        )

    def test_home_page_status(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_category_page_status(self):
        response = self.client.get('/category/technology/')
        self.assertEqual(response.status_code, 200)

    def test_search_page_status(self):
        response = self.client.get('/search/?q=тест')
        self.assertEqual(response.status_code, 200)

    def test_article_created(self):
        articles = Article.objects.all()
        self.assertEqual(articles.count(), 1)


class AdminTest(TestCase):
    """Тесты для админки"""

    def setUp(self):
        self.user = User.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='adminpass123'
        )
        self.client.login(username='admin', password='adminpass123')

    def test_admin_login(self):
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)

    def test_admin_categories(self):
        response = self.client.get('/admin/main/category/')
        self.assertEqual(response.status_code, 200)
