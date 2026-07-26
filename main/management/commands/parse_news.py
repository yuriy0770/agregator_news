import requests
from datetime import datetime
from django.core.management.base import BaseCommand
from main.models import Source, Article, Category


class Command(BaseCommand):
    help = 'Парсинг новостей с авто-категоризацией'

    KEYWORDS = {
        'Политика': [
            'путин', 'выборы', 'закон', 'депутат', 'правительство', 'политика',
            'песков', 'кремль', 'госдума', 'президент', 'власть', 'реформа',
            'совет', 'федерация', 'дума', 'собрание',
            'вмф', 'моряк', 'корабль', 'флот', 'адмирал', 'военный', 'армия',
            'минобороны', 'генерал', 'полковник', 'ракета', 'оружие',
            'командующий', 'пограничный', 'стратегический'
        ],
        'Спорт': [
            'футбол', 'хоккей', 'теннис', 'баскетбол', 'олимпиада', 'спорт',
            'матч', 'игра', 'турнир', 'чемпионат', 'команда', 'гол', 'победа',
            'стадион', 'болельщик', 'тренер', 'сборная'
        ],
        'Технологии': [
            'интернет', 'гаджет', 'смартфон', 'ai', 'робот', 'цифра',
            'технологии', 'приложение', 'нейросеть', 'компьютер', 'программа',
            'разработка', 'софт', 'алгоритм', 'аналог'
        ],
        'Экономика': [
            'доллар', 'рубль', 'цена', 'нефть', 'бизнес', 'рынок',
            'акции', 'инвестиции', 'финансы', 'банк', 'кризис',
            'экономика', 'курс', 'валюта', 'торговля', 'производство'
        ],
        'Происшествия': [
            'взрыв', 'пожар', 'авария', 'дтп', 'катастрофа', 'чп',
            'пострадал', 'погиб', 'спасение', 'экстренный',
            'скорая', 'полиция', 'мчс'
        ]
    }

    def get_category(self, text):
        """Определяет категорию по тексту новости"""
        text_lower = text.lower()
        for cat_name, words in self.KEYWORDS.items():
            for word in words:
                if word in text_lower:
                    return cat_name
        return None

    def handle(self, *args, **options):
        sources = Source.objects.filter(is_active=True)

        for source in sources:
            self.stdout.write(f'📡 Парсим {source.name}...')
            try:
                response = requests.get(source.url, timeout=10)
                if response.status_code != 200:
                    self.stdout.write(f'  ❌ Ошибка загрузки {source.name}')
                    continue

                import xml.etree.ElementTree as ET
                root = ET.fromstring(response.content)
                items = root.findall('.//item')

                count = 0
                for item in items[:15]:
                    title = item.find('title').text if item.find('title') is not None else ''
                    link = item.find('link').text if item.find('link') is not None else ''
                    pub_date = item.find('pubDate').text if item.find('pubDate') is not None else ''
                    description = item.find('description').text if item.find('description') is not None else ''

                    try:
                        from email.utils import parsedate_to_datetime
                        published_at = parsedate_to_datetime(pub_date)
                    except:
                        published_at = datetime.now()

                    # Определяем категорию
                    full_text = title + ' ' + description
                    cat_name = self.get_category(full_text)
                    category = None
                    if cat_name:
                        try:
                            category = Category.objects.get(name=cat_name)
                        except Category.DoesNotExist:
                            self.stdout.write(f'  ⚠️ Категория "{cat_name}" не найдена в БД')

                    # Создаём статью
                    article, created = Article.objects.get_or_create(
                        url=link,
                        defaults={
                            'title': title,
                            'content': description,
                            'published_at': published_at,
                            'source': source,
                            'category': category,
                        }
                    )
                    if created:
                        count += 1
                        cat_label = category.name if category else 'Без категории'
                        self.stdout.write(f'  ✅ {title[:40]} → {cat_label}')

                self.stdout.write(f'  📊 Добавлено {count} новостей из {source.name}')

            except Exception as e:
                self.stdout.write(f'  ❌ Ошибка: {e}')