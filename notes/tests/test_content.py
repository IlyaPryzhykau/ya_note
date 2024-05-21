from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from notes.models import Note

User = get_user_model()


class TestNotesPage(TestCase):
    """
    Тесты для проверки страницы со списком заметок.
    """

    NOTES_LIST = reverse('notes:list')
    NOTES_COUNT_ON_NOTES_LIST = 10

    @classmethod
    def setUpTestData(cls):
        """
        Создание тестовых данных для всех тестов в классе.
        """

        cls.author = User.objects.create(username='Лев Толстой')
        all_notes = [
            Note(
                author=cls.author,
                title=f'Запись {index}',
                text='Текст',
                slug=f'zapis-{index}'
            )
            for index in range(cls.NOTES_COUNT_ON_NOTES_LIST)
        ]
        Note.objects.bulk_create(all_notes)

    def test_notes_count(self):
        """
        Тест: Проверка правильного количества заметок на странице.
        """

        self.client.force_login(self.author)

        response = self.client.get(self.NOTES_LIST)
        notes_count = response.context['object_list'].count()

        self.assertEqual(notes_count, self.NOTES_COUNT_ON_NOTES_LIST)

    def test_notes_order(self):
        """
        Тест: Проверка правильного порядка отображения заметок на странице.
        """

        self.client.force_login(self.author)

        response = self.client.get(self.NOTES_LIST)
        object_list = response.context['object_list']

        all_notes = [note.id for note in object_list]
        sorted_dates = sorted(all_notes)

        self.assertEqual(all_notes, sorted_dates)
