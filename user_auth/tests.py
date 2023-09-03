from rest_framework.test import APITestCase
from django.urls import reverse
from user_auth.models import User
from habits.tests import TEST_CHAT_ID_USER, TEST_USER_PASSWORD

# Create your tests here.


class UserCreateUpdateTest(APITestCase):
    def setUp(self):
        super().setUp()
        self.chat_id = TEST_CHAT_ID_USER
        self.email = "test@example.com"
        self.password = TEST_USER_PASSWORD

        self.user = User.objects.create(
            chat_id=TEST_CHAT_ID_USER,
            first_name='Test',
            last_name='Just User',
            is_active=True,
            is_staff=False,
            is_superuser=False
        )
        self.user.set_password(TEST_USER_PASSWORD)
        self.user.save()
        # self.client.force_authenticate(self.user)
        self.url_token = reverse('token_obtain_pair')
        data = {"chat_id": self.user,
                "password": TEST_USER_PASSWORD
                }
        response = self.client.post(self.url_token, data)
        self.access_token = response.json().get('access')
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

    def test_create_user(self):
        """
        создание пользователя
        """
        number = User.objects.all().count()
        self.chat_id2 = TEST_CHAT_ID_USER+1
        self.email2 = "test2@example.com"
        self.password2 = TEST_USER_PASSWORD+"2"
        # self.client.force_authenticate(user=self.chat_id2)

        url = reverse("user-list")
        data = {"chat_id": self.chat_id2,
                "password": self.password2,
                "email": self.email2
                }

        response = self.client.post(url, data)

        # проверяем статус ответа
        self.assertEqual(response.status_code, 201)
        # проверяем в базе
        self.assertTrue(User.objects.filter(chat_id=self.chat_id2).exists())
        # проверяем, что количество увеличилось на 1
        self.assertTrue(User.objects.all().count(), number + 1)

    def test_update_user(self):
        # создаем пользователя для обновления
        self.chat_id3 = TEST_CHAT_ID_USER + 3
        self.password3 = TEST_USER_PASSWORD + "3"

        self.user3 = User.objects.create(
            chat_id=self.chat_id3,
            first_name='Test3',
            last_name='Just User3',
            is_subscripted=False,
            is_active=True,
            is_staff=False,
            is_superuser=False
        )
        self.user3.set_password(self.password3)
        self.user3.save()

        url = reverse("user-detail", kwargs={"pk": self.user3.pk})
        data = {
            "is_subscripted": True,
        }

        response = self.client.patch(url, data)

        # проверяем статус
        self.assertEqual(response.status_code, 200)

        updated_user = User.objects.get(pk=self.user3.pk)

        # проверяем, что is_subscripted пользователя был обновлен
        self.assertEqual(updated_user.is_subscripted, True)
